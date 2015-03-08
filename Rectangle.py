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

class Pipe():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    def draw(self):
        pygame.draw.rect(gameDisplay, green, [self.x, self.y, self.height, self.width])
        pygame.draw.rect(gameDisplay, green, [self.x, 0, self.height, self.width])

class Player():
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
    def draw(self):
        pygame.draw.circle(gameDisplay, red, (self.x, self.y), self.width)

while True:
    gameDisplay.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            direction = "up"
        if event.type == pygame.KEYUP:
            direction = "down"

    if direction == "up":
        player_position -= 2
    if direction == "down":
        player_position += 2

    player = Player(30, player_position, 20)
    player.draw()

    #Pipe position update
    first_pipe_pos -= 3
    second_pipe_pos -= 3

    pipe = Pipe(second_pipe_pos, display_height/2 + 50, display_height/2 - 50, 30)
    pipe.draw()
    pipe = Pipe(first_pipe_pos, display_height/2 + 50, display_height/2 - 50, 30)
    pipe.draw()

    #Chekcs if one of the pipes has crossed the left border, and assigns a new position
    if first_pipe_pos >= display_width or first_pipe_pos < 0:
        first_pipe_pos = display_width
    if second_pipe_pos >= display_width or second_pipe_pos < 0:
        second_pipe_pos = display_width

    pygame.display.update()
    clock.tick(60)


