import pygame
import sys
from random import choice

pygame.init()
size = display_width, display_height = [900, 600]
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
direction = None
img_file = pygame.image.load("flappy.jpg")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Pipe():
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.width = 30
        self.height = height
        self.pipe_speed = 3

    def properties(self):
        pass
        # Assign random pipe gaps here

    def move(self):
        self.x -= self.pipe_speed

    def left_collide(self):
        if self.x >= display_width or self.x < 0:
            self.x = display_width

    def draw(self):
        pygame.draw.rect(gameDisplay, green, [self.x, 0, self.width, self.height]) #TOP
        pygame.draw.rect(gameDisplay, green, [self.x, self.y, self.width, self.height]) #BOT



class Bird(pygame.sprite.Sprite):
    def __init__(self, image, y_pos, gravity, force):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy.png")
        #self.rect = self.image.get_rect()
        #self.rect.left, self.rect.top = location
        #self.speed = speed
        self.direction = "down"
        self.y_pos = y_pos
        self.x_pos = 10
        self.gravity = gravity
        self.force = force



    def handle_keys(self):
        if event.type == pygame.KEYDOWN:
            self.direction = "up"
        if event.type == pygame.KEYUP:
            self.direction = "down"

    def collision_detect(self):
        pass
        # self.rect = self.rect.move(self.speed)
        # if self.rect.top <= 0 or self.rect.bottom >= display_height:
        #     self.speed[1] = -self.speed[1]

    def move(self):
        if self.direction == "down":
            self.y_pos += self.gravity
        if self.direction == "up":
            self.y_pos -= self.force

    def draw(self, surface):
        surface.blit(self.image, (self.x_pos, self.y_pos))

# Defines the spawn positions of each pipe - Add more unique spawn positions if you want more pipes
pipe_positions = [display_width/2, display_width]
pipes = []
for i in range(2):
    pipe = Pipe(pipe_positions[i], display_height/2 + 50, display_height/2 - 50)
    pipes.append(pipe)


birds = []
for i in range(1):
    location = (10, display_height/2)
    player = Bird(img_file, display_height/2, 3, 5)
    birds.append(player)

while True:
    gameDisplay.fill(blue)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # DESCRIPTION redraw the bird(s). Since a list is used, multiple birds should work, same as multiple pipes.
    # although it will not make sense gameplay wise
    for bird in birds:
        bird.handle_keys()
        bird.move()
        bird.draw(gameDisplay)

    # DESCRIPTION redraws the pipes, one by one in the list
    for pipe in pipes:
        pipe.move()
        pipe.draw()
        pipe.left_collide()

        if pipe.x == 0:
            pipes.remove(pipe)
            pipe = Pipe(display_width, display_height/2 + 50, display_height/2 - 50)
            pipes.append(pipe)

    pygame.display.update()
    clock.tick(60)



