import pygame
from OpenGL.GL import *

pygame.init()

screen = pygame.display.set_mode((500,500))

x = 100
y = 100

while True:
    screen.set_at((x,y), (255,255,255))

    pygame.display.flip()

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_w):
                y += 1
            if (event.key == pygame.K_a):
                x -= 1
            if (event.key == pygame.K_s):
                y -= 1
            if (event.key == pygame.K_d):
                x += 1