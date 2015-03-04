__author__ = 'Andreas'
import pygame, sys
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))

class MyPaddleClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface([100,20])
        image_surface.fill[(0, 0, 0)]
        self.image = image_surface.convert()
        self.rect = self.rect.image.get_rect()
        self.rect.left, self.rect.top = location

paddle = MyPaddleClass([270, 400])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


    gameDisplay.fill((255,255,255))
    pygame.display.update()