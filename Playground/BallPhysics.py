__author__ = 'Andreas'
import os
import sys
import math
import pygame
import random


white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
green = (0, 155, 0)
light_green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 200, 200)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

colors = [black, red, green, yellow, blue]

inital_velocity = 20

pygame.init()
display_width = 800
display_height = 600
game_display = pygame.display.set_mode([display_width, display_height])
clock = pygame.time.Clock()

class MyCircle:
    def __init__(self, position, size, color = (255,255,255), velocity = pygame.math.Vector2(0,0), width = 1):
        self.position = position
        self.color = color
        self.width = width
        self.size = size
        self.velocity = velocity

    def display(self):
        rx,ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(game_display, self.color, (rx, ry), self.size, self.width)

    def move(self):
        self.position += self.velocity * dtime

    def change_velocity(self, velocity):
        self.velocity = velocity

def get_random_velocity():
    new_angle = random.uniform(0, math.pi*2)
    new_x = math.sin(new_angle)
    new_y = math.cos(new_angle)
    new_vector = pygame.math.Vector2(new_x, new_y)
    new_vector.normalize()
    new_vector *= inital_velocity
    return new_vector

fps_limit = 60
run_me = True

numbers_of_circles = 10
my_circles = []

for n in range(numbers_of_circles):
    size = random.randint(10, 20)
    x = random.randint(size, display_width-size)
    y = random.randint(size, display_height-size)
    color = random.choice(colors)
    velocity = get_random_velocity()
    my_circles.append(MyCircle(pygame.math.Vector2(x,y), size, color, velocity))


direction_tick = 0.0

while run_me:
    clock.tick(fps_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False

    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms/1000.0

    direction_tick += dtime
    if direction_tick > 1.0:
        direction_tick = 0.0
        random_circle = random.choice(my_circles)
        new_veloity = get_random_velocity()
        random_circle.change_velocity(new_veloity)

    game_display.lock()
    game_display.fill(white)

    for n in my_circles:
        n.move()
        n.display()

    pygame.display.update()

pygame.quit()
sys.exit()