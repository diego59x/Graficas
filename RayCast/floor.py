from math import dist
from lib import * 

class Floor(object):
    def __init__(self, x, y, material):
        self.y = y
        self.x = x
        self.material = material 
    def ray_intersect(self, origin, direction):
        
        d = -(origin.y + self.y) / direction.y
        point = sum(origin, mul(direction, d))

        if d <= 0 or abs(point.x) > 7 or point.z > -5 or point.z < -10:
            return None

        normal = V3(0,1,0)
        return Intersect( distance=d, normal=normal, point=point)
        