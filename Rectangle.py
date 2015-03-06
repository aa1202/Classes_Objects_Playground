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

class Circle():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    def draw(self):
        pygame.draw.circle(gameDisplay, random.choice(colorList), (self.x, self.y), self.radius)

pygame.init()
size = [300,300]
gameDisplay = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                myRect = Rectangle(random.randint(1,300), random.randint(1,300), random.randint(1,50), random.randint(1,50))
                myRect.draw()
            if event.key == pygame.K_c:
                myCircle = Circle(random.randint(1,300), random.randint(1,300), random.randint(1,20))
                myCircle.draw()

        pygame.display.update()
        clock.tick(60)


