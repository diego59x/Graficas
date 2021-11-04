# import sys 
# sys.path.insert(0, "C:\Python39\Lib\site-packages")
# import site

# print(site.getsitepackages())
import pygame 
import random

class Life(object):
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
    def clear(self):
        self.screen.fill((0,0,0))

    def primaty_points(self):
        for i in range(0,1000):
            self.pixel(random.randint(0,500), random.randint(0,500))
    def copy(self):
        # pygame.surfarray
        self.prev_turn = self.screen.copy()
    
    def pixel(self, x, y):
        self.screen.set_at((x, y), (255,255,255))
    def render(self):
        self.primaty_points()


pygame.init()
screen = pygame.display.set_mode((500,500), pygame.HWSURFACE | pygame.DOUBLEBUF) 

r = Life(screen)

r.pixel(100,100)

while True:
    pygame.time.delay(100)
    r.copy()
    # r.clear() pygame.event.pump()
    r.render()
    pygame.display.flip()