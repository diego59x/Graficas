

import glm

class ModelConstants():

    def __init__(self):
        self.i = glm.mat4(1)
        self.translate = glm.translate(self.i, glm.vec3(0, 0, 0))
        self.scale = glm.scale(self.i, glm.vec3(10, 10, 10))
        self.rotate = glm.rotate(self.i, glm.radians(0), glm.vec3(0, 1, 0))
        self.view = glm.lookAt(glm.vec3(0, 0, 20), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        self.projection = glm.perspective(glm.radians(45), 1.667, 0.1, 1000.0) 
   
    def rotationCamera(self, rotate):
        self.rotate = glm.rotate(self.i, glm.radians(rotate), glm.vec3(0, 1, 0))
    
    # def scaleCamera(self, zoomInCamera) 
    #    if (zoomInCamera < 2 and zoomInCamera > 0.1):
    #      self.scaleCamera = glm.scale(i, zoomInCamera * glm.vec3(10, 10, 10))
    def zoomCamera(self, zoomRate):
        # Idk why you have to multiply the angle to make a zoom in or zoom out of the camera
        self.projection = glm.perspective(glm.radians(zoomRate * 45), 1.667, 0.1, 1000.0) 