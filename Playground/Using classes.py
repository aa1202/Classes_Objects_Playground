import pygame
import sys

pygame.init()
display_width = 900
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
direction = None

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Pipe():
    def __init__(self, x, y, width, height, pipe_speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.pipe_speed = pipe_speed

    def move(self):
        self.x -= self.pipe_speed

    def draw(self):
        pygame.draw.rect(gameDisplay, green, [self.x, 0, self.height, self.width]) #TOP
        pygame.draw.rect(gameDisplay, green, [self.x, self.y, self.height, self.width]) #BOT

    def left_collide(self):
        if self.x >= display_width or self.x < 0:
            self.x = display_width


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, gravity, force):
        self.image = pygame.image.load("flappy.png")
        self.x = x
        self.y = y
        self.direction = "none"
        self.gravity = gravity
        self.force = force

    def direction_controller(self):
        if self.direction == "down":
            self.y += self.gravity
        if self.direction == "up":
            self.y -= self.force

    def handle_keys(self):
        if event.type == pygame.KEYDOWN:
            self.direction = "up"
        if event.type == pygame.KEYUP:
            self.direction = "down"

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

#Initializes the player and the pipes
first_pipe = Pipe(display_width, display_height/2 + 50, display_height/2 - 50, 30, 3)
second_pipe = Pipe(display_width/2, display_height/2 + 50, display_height/2 - 50, 30, 3)


bird = Bird(10, display_height/2, 5, 3)

while True:
    gameDisplay.fill(blue)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # DESCRIPTION controls the birds movement
    bird.handle_keys()
    bird.direction_controller()

    # DESCRIPTION blits the player to the screen
    bird.draw(gameDisplay)

    # DESCRIPTION redraws the pipes
    first_pipe.move()
    first_pipe.draw()
    second_pipe.move()
    second_pipe.draw()


    # DESCRIPTION check if one of the pipe classes has crossed the left edge
    first_pipe.left_collide()
    second_pipe.left_collide()

    pygame.display.update()
    clock.tick(60)




