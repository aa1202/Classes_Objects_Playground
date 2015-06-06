__author__ = 'Andreas'

import pygame
import random
import sys

pygame.init()
size = display_width, display_height = [900, 600]
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
direction = None
img_file = pygame.image.load("flappy.jpg")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

block_list = pygame.sprite.Sprite()
all_sprites_list = pygame.sprite.Group

#Define the pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

#Define the bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        self.original_image = pygame.image.load("flappy.jpg").convert()
        self.image = self.original_image
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def handle_keys(self):
        if event.type == pygame.KEYDOWN:
            self.direction = "up"
        if event.type == pygame.KEYUP:
            self.direction = "down"

    def move(self):
        if self.direction == "up":
            self.rect.y -= 2
        elif self.direction == "down":
            self.rect.y += 2

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

pipe_positions = [display_width/2, display_width]
for i in range(50):
    pipe = Pipe(red, 20, 15)

    # Sets the rect x and y position of the block, by default it is in x = 0 and y = 0
    pipe.rect.x = random.randrange(display_width - 20)
    pipe.rect.y = random.randrange(display_height - 15)

    block_list.add(pipe)
    all_sprites_list.add(pipe)

player = Bird(red, 20, 20)
all_sprites_list.append(player)

while True:
    gameDisplay.fill(blue)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    player.handle_keys()
    player.move()
    player.draw(gameDisplay)

    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
    all_sprites_list.draw(gameDisplay)

    pygame.display.update()
    clock.tick(60)