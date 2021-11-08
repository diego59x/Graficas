from math import dist
from lib import * 

class Floor(object):
    def __init__(self, xI, xF, y, zI, zF, material):
        self.y = y
        self.xI = xI
        self.xF = xF
        self.zI = zI
        self.zF = zF
        self.material = material 
    def ray_intersect(self, origin, direction):
        
        if (direction.y == 0):
            d = 0
        else:
            d = -(origin.y + self.y) / direction.y
        point = sum(origin, mul(direction, d))

        if d <= 0 or point.x > self.xF or point.x < self.xI or point.z > self.zI or point.z < self.zF:
            return None

        normal = V3(0,1,0)
        return Intersect( distance=d, normal=normal, point=point)
        