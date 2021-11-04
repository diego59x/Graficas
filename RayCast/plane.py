from math import dist
from lib import * 

epsilon = 1e-6
class Plane(object):
    def __init__(self, corner1, corner2, corner3, corner4, ztotal, material):
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4
        self.ztotal = ztotal
        self.material = material
        # self.lineDown = sub(self.corner3, self.corner4)
        # self.lineUp = sub(self.corner1, self.corner2)
        # self.lineLeft = sub(self.corner1, self.corner4)
        # self.lineRight = sub(self.corner3, self.corner2)
        self.p0 = V3((self.corner1.x + self.corner4.x)/2, (self.corner2.y + self.corner3.y)/2, self.ztotal)
        self.line1 = sub(self.corner4, self.corner2)
        self.line2 = sub(self.corner1, self.corner3)
        self.n = norm(cross(self.line1, self.line2))
    def ray_intersect(self, origin, direction):

        # print("lineDown", self.lineDown)
        # print("lineup", self.lineUp)
        # print("lineLeft", self.lineLeft)
        # print("lineRight", self.lineRight)

        denom = dot(self.n, direction)
        if (abs(denom) > epsilon):
            p0l0 = sub(origin, self.p0)
            t = -dot(self.n, p0l0) / denom

            point = sum(origin, mul(direction, t))

            if (t >= 0): # Hacer las lineas de los cuadrados y validarlo aca  and
                if ( point.y <= -point.x + 2 and point.y >= -point.x/4 - 1.75 and point.x > self.corner1.x and point.x < self.corner4.x):
                    return Intersect(distance=t, normal=self.n, point=point)
                else:
                    return None
            else:
                return None

        # point.x > self.lineLeft.x and point.y < self.lineUp.y and point.x < self.lineRight.x and point.y > self.lineDown.y:
        # if d <= 0 or (point.x > self.xmax and point.y > self.ymax ) or (point.x < self.xmin and point.y < self.ymin): 
        #     return None
        #print(point)
        