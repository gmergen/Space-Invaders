import pygame
from game_object import GameObject
from player import Player
from enemy import Enemy
from bullet import Bullet
from level import Level

windowWidth = 400
windowHeight = 600
game_side_margin = 10
game_top_margin = 40
game_bottom_margin = game_top_margin
game_border_width = 3

wall_top = game_top_margin + game_border_width
wall_left = game_side_margin + game_border_width
wall_right = windowWidth - game_side_margin - game_border_width
wall_bottom = windowHeight - game_bottom_margin - game_border_width

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)

pygame.init()

# load game images
playerImg = pygame.image.load("media/si-player.gif") # was play.gif, switched to ship
enemyImg = pygame.image.load("media/si-enemy.gif")
bulletImg = pygame.image.load("media/si-bullet.gif")
backgroundImg = pygame.image.load("media/si-background.gif")

# load sounds
laser_sound = pygame.mixer.Sound('media/si-laser.wav')
# explosion_sound = pygame.mixer.Sound('media/si-explode.wav')
oof_sound = pygame.mixer.Sound('media/si-oof.wav') 
pygame.mixer.music.load('media/Bohemian.mp3')
pygame.mixer.music.play(-1)

title_font = pygame.font.SysFont('Arial', 40, True)
score_font = pygame.font.SysFont('Arial', 26, True)

gameDisplay = pygame.display.set_mode((400,600))
pygame.display.set_caption('Space Invaders')

        
clock = pygame.time.Clock()

player1 = Player(wall_left + (wall_right - wall_left) / 2 - playerImg.get_width() / 2,
    wall_bottom - playerImg.get_height() - 1, playerImg, 5)

bullets = []
levels = []

levels.append(Level(3, 5, 2, 1, enemyImg, wall_left, wall_top))
levels.append(Level(4, 5, 2, 2, enemyImg, wall_left, wall_top))
levels.append(Level(4, 7, 3, 3, enemyImg, wall_left, wall_top))
levels.append(Level(5, 7, 3, 4, enemyImg, wall_left, wall_top))
levels.append(Level(6, 8, 4, 5, enemyImg, wall_left, wall_top))

current_level_number = 1

# main game loop
while player1.is_alive:

    enemies = levels[current_level_number - 1].enemies

    if len(enemies) == 0:
        current_level_number += 1
        if current_level_number < len(levels):
            enemies = levels[current_level_number - 1].enemies
        else:
            player1.is_alive = False
    
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player1.is_alive = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.move_left()
            elif event.key == pygame.K_RIGHT:
                player1.move_right()
            elif event.key == pygame.K_SPACE:
                player1.shoot(bullets, bulletImg, laser_sound)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1.stop_moving()

    gameDisplay.blit(gameDisplay, (0,0))
    gameDisplay.fill(black) 
    title_text = title_font.render('SPACE INVADERS', False, red)
    gameDisplay.blit(title_text, (windowWidth / 2 - title_text.get_width() / 2, 5))
    score_text = score_font.render('SCORE: ' + str(player1.score), False, blue)
    gameDisplay.blit(score_text, (wall_left, wall_bottom + game_border_width))
    pygame.draw.rect(gameDisplay, white, (game_side_margin, game_top_margin, windowWidth - game_side_margin * 2, windowHeight - game_top_margin - game_bottom_margin))
    gameDisplay.blit(backgroundImg, (wall_left, wall_top), (0,0, wall_right - wall_left, wall_bottom - wall_top))
    
    for bullet in bullets:
        if bullet.ycor < wall_top:
            bullets.remove(bullet)
            continue

        # check if this bullet has hit any enemies
        for enemy in enemies:
            # if the bullet collieds with an enemy, remove both from their arrays
            if bullet.colliedes_with(enemy):
                oof_sound.play()
                enemies.remove(enemy)
                bullets.remove(bullet)
                player1.change_score(150)
                break
        
        if bullet.ycor < wall_top:
            bullets.remove(bullet)


    # check all enemies to see if one has reached a wall
    for enemy in enemies:
        if enemy.xcor <= wall_left or enemy.xcor >= wall_right - enemy.width:
            # since one enemy has reached a wall, change all enemies directions
            for e in enemies:
                e.change_direction()
                e.move_down()
            # since one enemy has reached a wall, then stop checking the other enemies
            break

        if enemy.colliedes_with(player1):
            player1.is_alive = False

    player1.show(gameDisplay, wall_left, wall_right)

     # move and show all enemies
    for enemy in enemies:
        enemy.move_over()
        enemy.show(gameDisplay)

    # move and show all bullets
    for bullet in bullets:
        bullet.move_up()
        bullet.show(gameDisplay)
       
  
    pygame.display.update()
    clock.tick(60)

show_final_screen = True
while show_final_screen:
    score_text = score_font.render('SCORE: ' + str(player1.score), False, blue)
    gameDisplay.blit(score_text, (windowWidth / 2 - score_text.get_width() / 2, windowHeight / 2))

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_final_screen = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_final_screen = False


pygame.quit()
