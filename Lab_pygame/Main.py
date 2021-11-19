# import sys 
# sys.path.insert(0, "C:\Python39\Lib\site - packages")
# import site

# print(site.getsitepackages())
import pygame 
import time
import random
from lib import color
timeout = time.time()  +  120 # Active for two minutes

BLACK = color(0,0,0).toBytes()
WHITE = color(255,255,255).toBytes()

class Life(object):
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
        self.actualCells = []

    def copy(self):
        # pygame.surfarray
        self.prev_turn = pygame.surfarray.array2d(self.screen)

    def pixel(self, x, y, color = WHITE):
        self.screen.set_at((x, y), color)

    def initValues(self):
        self.toad()
        self.strange()
        self.cross()
        self.sun()

    def cross(self):
        for i in range(0, 80):
            centerX = random.randint(10, 490)
            centerY = random.randint(10, 490)

            self.pixel(centerX + 1, centerY)
            self.pixel(centerX + 1, centerY + 1)

            self.pixel(centerX,     centerY + 2)
            self.pixel(centerX + 2, centerY + 2)

            self.pixel(centerX + 1, centerY + 3)
            self.pixel(centerX + 1, centerY + 4)
            self.pixel(centerX + 1, centerY + 5)
            self.pixel(centerX + 1, centerY + 6)

            self.pixel(centerX,     centerY + 7)
            self.pixel(centerX + 2, centerY + 7)

            self.pixel(centerX + 1, centerY + 8)
            self.pixel(centerX + 1, centerY + 9)

    def sun(self):
        for i in range(0, 40):
            centerX = random.randint(10, 490)
            centerY = random.randint(10, 490)

            self.pixel(centerX + 2,  centerY)
            self.pixel(centerX + 3,  centerY)
            self.pixel(centerX + 4,  centerY)
            self.pixel(centerX + 8,  centerY)
            self.pixel(centerX + 9,  centerY)
            self.pixel(centerX + 10, centerY)

            self.pixel(centerX,      centerY + 2)
            self.pixel(centerX + 5,  centerY + 2)
            self.pixel(centerX + 7,  centerY + 2)
            self.pixel(centerX + 12, centerY + 2)

            self.pixel(centerX,      centerY + 3)
            self.pixel(centerX + 5,  centerY + 3)
            self.pixel(centerX + 7,  centerY + 3)
            self.pixel(centerX + 12, centerY + 3)

            self.pixel(centerX,      centerY + 4)
            self.pixel(centerX + 5,  centerY + 4)
            self.pixel(centerX + 7,  centerY + 4)
            self.pixel(centerX + 12, centerY + 4)
            
            self.pixel(centerX + 2,  centerY + 5)
            self.pixel(centerX + 3,  centerY + 5)
            self.pixel(centerX + 4,  centerY + 5)
            self.pixel(centerX + 8,  centerY + 5)
            self.pixel(centerX + 9,  centerY + 5)
            self.pixel(centerX + 10, centerY + 5)

            self.pixel(centerX + 2,  centerY + 7)
            self.pixel(centerX + 3,  centerY + 7)
            self.pixel(centerX + 4,  centerY + 7)
            self.pixel(centerX + 8,  centerY + 7)
            self.pixel(centerX + 9,  centerY + 7)
            self.pixel(centerX + 10, centerY + 7)

            self.pixel(centerX,      centerY + 8)
            self.pixel(centerX + 5,  centerY + 8)
            self.pixel(centerX + 7,  centerY + 8)
            self.pixel(centerX + 12, centerY + 8)

            self.pixel(centerX,      centerY + 9)
            self.pixel(centerX + 5,  centerY + 9)
            self.pixel(centerX + 7,  centerY + 9)
            self.pixel(centerX + 12, centerY + 9)

            self.pixel(centerX,      centerY + 10)
            self.pixel(centerX + 5,  centerY + 10)
            self.pixel(centerX + 7,  centerY + 10)
            self.pixel(centerX + 12, centerY + 10)

    def toad(self):
        for i in range(0, 100):
            centerX = random.randint(10, 490)
            centerY = random.randint(10, 490)

            self.pixel(centerX, centerY)
            self.pixel(centerX + 1, centerY - 1)
            self.pixel(centerX + 2, centerY - 1)
            self.pixel(centerX - 1, centerY - 1)
            self.pixel(centerX, centerY - 1)
            self.pixel(centerX + 1, centerY)
            self.pixel(centerX + 2, centerY)

    def strange(self):
        for i in range(0, 50):
            centerX = random.randint(10, 490)
            centerY = random.randint(10, 490)

            self.pixel(centerX, centerY)
            self.pixel(centerX - 1, centerY)
            self.pixel(centerX + 1, centerY)

            self.pixel(centerX - 1, centerY - 1)
            self.pixel(centerX + 1, centerY - 1)

            self.pixel(centerX, centerY - 2)
            self.pixel(centerX - 1, centerY - 2)
            self.pixel(centerX + 1, centerY - 2)

            self.pixel(centerX, centerY - 3)
            self.pixel(centerX - 1, centerY - 3)
            self.pixel(centerX + 1, centerY - 3)

            self.pixel(centerX, centerY - 4)
            self.pixel(centerX - 1, centerY - 4)
            self.pixel(centerX + 1, centerY - 4)

            self.pixel(centerX, centerY - 5)
            self.pixel(centerX - 1, centerY - 5)
            self.pixel(centerX + 1, centerY - 5)

            self.pixel(centerX  +  1, centerY  -  6)
            self.pixel(centerX  +  1, centerY  -  6)

            self.pixel(centerX, centerY  -  7)
            self.pixel(centerX  -  1, centerY  -  7)
            self.pixel(centerX  +  1, centerY  -  7)

    def checkNewShape(self):
        for x in range(10, self.width  -  10):
            for y in range(10, self.height  -  10):
                
                cellAside = 0

                if self.prev_turn[x][y + 1] == 16777215:
                    cellAside += 1
                if self.prev_turn[x][y - 1] == 16777215:
                    cellAside += 1
                if self.prev_turn[x + 1][y] == 16777215:
                    cellAside += 1
                if self.prev_turn[x - 1][y] == 16777215:
                    cellAside += 1
                if self.prev_turn[x + 1][y + 1] == 16777215:
                    cellAside += 1
                if self.prev_turn[x - 1][y - 1] == 16777215:
                    cellAside += 1
                if self.prev_turn[x - 1][y + 1] == 16777215:
                    cellAside += 1
                if self.prev_turn[x + 1][y - 1] == 16777215:
                    cellAside += 1
                if self.prev_turn[x][y] == 16777215:   
                    if cellAside < 2:
                        self.pixel(x, y, BLACK)
                    if cellAside == 2 or cellAside == 3:
                        self.pixel(x, y, WHITE)
                    if cellAside > 3:
                        self.pixel(x, y, BLACK)                            
                else:
                    if cellAside == 3:
                        self.pixel(x, y)

pygame.init()
screen = pygame.display.set_mode((500,500)) 

r = Life(screen)

r.initValues()

flag = True

while flag:
    if time.time() > timeout:
        flag = False

    pygame.time.delay(1)
    r.copy()

    r.checkNewShape()

    pygame.display.flip()
