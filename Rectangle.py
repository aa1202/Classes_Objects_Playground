import pygame
import sys

pygame.init()
display_width = 900
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

first_pipe_pos = int(display_width)
second_pipe_pos = int(display_width/2)
player_position = int(display_height/2)
direction = None

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Pipe():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    def draw(self, x):
        self.x = x
        #TOP
        pygame.draw.rect(gameDisplay, green, [self.x, 0, self.height, self.width])
        #BOT
        pygame.draw.rect(gameDisplay, green, [self.x, self.y, self.height, self.width])

class Player():
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
    def draw(self, y):
        self.y = y
        pygame.draw.circle(gameDisplay, red, (self.x, self.y), self.width)


#Initializes the player and the pipes
player = Player(30, player_position, 20)
first_pipe = Pipe(first_pipe_pos, display_height/2 + 50, display_height/2 - 50, 30)
second_pipe = Pipe(second_pipe_pos, display_height/2 + 50, display_height/2 - 50, 30)

while True:
    gameDisplay.fill(blue)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:

            direction = "up"
        if event.type == pygame.KEYUP:
            direction = "down"

    if direction == "up":
        player_position -= 2
    elif direction == "down":
        player_position += 2

    first_pipe_pos -= 3
    second_pipe_pos -= 3

    player.draw(player_position)
    first_pipe.draw(first_pipe_pos)
    second_pipe.draw(second_pipe_pos)

    #Chekcs if one of the pipes has crossed the left border, and assigns a new position
    if first_pipe_pos >= display_width or first_pipe_pos < 0:
        first_pipe_pos = display_width
    if second_pipe_pos >= display_width or second_pipe_pos < 0:
        second_pipe_pos = display_width

    pygame.display.update()
    clock.tick(60)




