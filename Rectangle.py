import pygame
import random
import sys

red = (255, 0, 0)
green = (0, 255, 0)
colorList = [red, green]

class Rectangle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    def draw(self):
        pygame.draw.rect(gameDisplay, random.choice(colorList), [self.x, self.y, self.height, self.width])

pygame.init()
size = [300,300]
gameDisplay = pygame.display.set_mode(size)
clock = pygame.time.Clock()
myObject = Rectangle()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for i in range(200):
        gameDisplay.fill((0, 0, 0))
        myObject = Rectangle(random.randint(1,300), random.randint(1,300), random.randint(1,50), random.randint(1,50))
        myObject.draw()
        myObject = Rectangle(random.randint(1,300), random.randint(1,300), random.randint(1,50), random.randint(1,50))
        myObject.draw()

        pygame.display.update()
        clock.tick(60)
    break

