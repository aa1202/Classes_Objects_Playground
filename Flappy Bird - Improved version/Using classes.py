import pygame
import sys
import random

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
    #Constructor
    def __init__(self, start_position_x, pipe_height_constant):
        global pipe_positions
        self.x = start_position_x
        self.width = 30
        self.height = pipe_height_constant
        self.pipe_speed = 3

        pipe_positions = random.choice([(100, -400), (150, -350), (200, -300), (250, -250), (300, -200), (350, -150),(400, -100)])

    def left_collide(self):
        if self.x >= display_width or self.x < 0:
            self.x = display_width

    def move(self):
        self.x -= self.pipe_speed

    def draw(self):
        pygame.draw.rect(gameDisplay, green, [self.x, 0, self.width, pipe_positions[0]]) #TOP
        pygame.draw.rect(gameDisplay, green, [self.x, display_height, self.width, pipe_positions[1]]) #BOT





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
    pipe = Pipe(pipe_positions[i], 200)
    pipes.append(pipe)
player = Bird(img_file, display_height/2, 3, 5)


while True:
    gameDisplay.fill(blue)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # DESCRIPTION redraw the bird
    player.handle_keys()
    player.move()
    player.draw(gameDisplay)

    # DESCRIPTION redraws the pipes, one by one in the list
    for pipe in pipes:
        pipe.move()
        pipe.draw()
        pipe.left_collide()

        if pipe.x == 0:
            pipes.remove(pipe)
            pipe = Pipe(display_width, 200)
            pipes.append(pipe)

    pygame.display.update()
    clock.tick(60)



