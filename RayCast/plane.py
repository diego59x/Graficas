from math import dist
from lib import * 

epsilon = 1e-6
class Plane(object):
    def __init__(self, corner1, corner2, corner3, corner4, ztotal, material, nOptional = None):
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4
        self.ztotal = ztotal
        self.material = material
        self.nOptional = nOptional
        self.CaclculateConstants()
    def ray_intersect(self, origin, direction):

        denom = dot(self.n, direction)
        if (abs(denom) > epsilon):
            p0l0 = sub(origin, self.p0)
            t = -dot(self.n, p0l0) / denom

            point = sum(origin, mul(direction, t))

            if (t >= 0):
                if (self.lineDown(point) == True and self.lineUp(point) == True and self.lineLeft(point) == True and self.lineRight(point) == True):
                    return Intersect(distance=t, normal=self.n, point=point)
                else:
                    return None
            else:
                return None
    def CaclculateConstants(self): 
        self.p0 = V3((self.corner1.x + self.corner4.x)/2, (self.corner2.y + self.corner3.y)/2, self.ztotal)

        if (self.nOptional != None):
            self.n = self.nOptional
        else:
            line1 = sub(self.corner3, self.corner1)
            line2 = sub(self.corner4, self.corner2)
            self.n = norm(cross(line1, line2))

        self.mLeft = 0
        self.mRight = 0
        self.mUp = 0
        self.mDown = 0
        self.bUp = 0
        self.bDown = 0

        if (self.corner2.x - self.corner1.x != 0):
            self.mLeft = (self.corner2.y - self.corner1.y)/(self.corner2.x - self.corner1.x)
        
        if (self.corner3.x - self.corner4.x != 0):
            self.mRight = (self.corner3.y - self.corner4.y)/(self.corner3.x - self.corner4.x)
        
        if (self.corner4.x - self.corner1.x != 0):
            self.mUp = (self.corner4.y - self.corner1.y)/(self.corner4.x - self.corner1.x)

        if (self.corner3.x - self.corner2.x != 0):
            self.mDown = (self.corner3.y - self.corner2.y)/(self.corner3.x - self.corner2.x)
        
        self.bUp = self.corner4.y - self.mUp*self.corner4.x 
        self.bDown = self.corner3.y - self.mDown*self.corner3.x 

        if (self.mRight == 0):
            self.bRight = self.corner3.x
        else:
            self.bRight = self.corner3.y - self.mRight*self.corner3.x 
        if (self.mLeft == 0):
            self.bLeft = self.corner2.x
        else:
            self.bLeft = self.corner2.y - self.mLeft*self.corner2.x 

    def lineRight(self, point):
        if (self.mRight == 0):
            if (point.x >= - self.bRight ):
                return True
            else:
                return False
        else:
            if (point.y >= -point.x*self.mRight - self.bRight ):
                return True
            else:
                return False

    def lineLeft(self, point):
        if (self.mLeft == 0):
            if (point.x <= - self.bLeft ):
                return True
            else:
                return False
        else:
            if (point.y <= -point.x*self.mLeft - self.bLeft ):
                return True
            else:
                return False

    def lineUp(self, point):

        if (point.y >= -point.x*self.mUp - self.bUp):
            return True
        else:
            return False

    def lineDown(self, point):
    
        if (point.y <= -point.x*self.mDown - self.bDown):
            return True
        else:
            return False