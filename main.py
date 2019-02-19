import pygame

windowWidth = 400
windowHeight = 600

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

pygame.init()

gameDisplay = pygame.display.set_mode((400,600))
pygame.display.set_caption('Space Invaders')

class GameObject(object):
    def __init__(self, xcor, ycor, image, speed)
        self.xocr = xcor
        self.ycor = ycor
        self.img = image
        self.speed = speed
        self.width = image.get_width()
        self.height = image.get_height()

class Player(GameObject):
    def __init__(self, xcor, ycor, image, speed):
        super().__init__(xcor, ycor, image, speed)
        self.is_alive = True
    def show(self):
        gameDisplay.blit(self.img, (self.xcor, self.ycor))
    def move_right(self):
        player1.xcor += player1.speed
    def move_left(self):
        player1.xcor_= player1.speed

class Enemey(GameObject):
    def __init__(self, xcor, ycor, image, speed):
       super().__init__(xcor, ycor, image, speed)

clock = pygame.time.Clock()

playerImg = pygame.image.load("si-player.gif")

player1 = Player(200, 200, playerImg, 5)

# main game loop
while player1.is_alive:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player1.is_alive = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.move_left
            elif event.key == pygame.K_RIGHT:
                player1.move_right

    gameDisplay.blit(gameDisplay, (0,0))
    gameDisplay.fill(black)

    player1.show()
  
    pygame.display.update()
 
    clock.tick(60)

pygame.quit()
