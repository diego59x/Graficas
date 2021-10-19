from lib import * 
from sphere import *
from random import random
from math import pi, tan

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.light = None
        self.clear()
        self.background_color = BLACK

    def clear(self):
        self.pixels = [
            [BLACK for _ in range(self.width)] 
            for _ in range(self.height)
        ]
    def write(self, filename):
        writeBMP(filename, self.width, self.height, self.pixels)

    def point(self, x, y, col):
        self.pixels[y][x] = col
    def cast_ray(self, origin, direction, recursion = 0):
        material, intersect = self.scene_intersect(origin, direction)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            return self.background_color

        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))
        shadow_intesity = 0
        offset_normal = mul(intersect.normal, 0.1) # shadow bias
        shadow_orig = sum(intersect.point, offset_normal) \
                    if dot(light_dir, intersect.normal) >= 0 else sub(intersect.point, offset_normal)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir) 

        
        if shadow_material is None or length(sub(shadow_intersect.point, shadow_orig)) > light_distance:
            shadow_intensity = 0
        else:
            shadow_intesity = 0.9

        if material.albedo[2] > 0:
            reverse_direction = mul(direction, -1)
            reflect_direction = reflect(reverse_direction, intersect.normal )
            reflect_origin = sum(intersect.point, offset_normal) \
                    if dot(reflect_direction, intersect.normal) >= 0 else sub(intersect.point, offset_normal)
            
            reflect_color = self.cast_ray(reflect_origin, reflect_direction, recursion + 1)  
        else: 
            reflect_color = color(0,0,0)



        if material.albedo[3] > 0:
            refract_direction = refract(direction, intersect.normal, material.refractive_index)
            
            if refract_direction is None: 
                refract_color = color(0,0,0)
            else:     
                refract_origin = sum(intersect.point, offset_normal) \
                        if dot(refract_direction, intersect.normal) >= 0 else sub(intersect.point, offset_normal)
                
                refract_color = self.cast_ray(refract_origin, refract_direction, recursion + 1)  
        else: 
            refract_color = color(0,0,0)
        

        diffuse_intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) \
            * (1 - shadow_intesity)

        if shadow_intesity > 0:
            specular_intensity = 0
        else:
            specular_reflection = reflect(light_dir, intersect.normal)
            specular_intensity = self.light.intensity * (max(0, dot(specular_reflection, direction)) ** material.specular)

        diffuse = material.diffuse * diffuse_intensity * material.albedo[0]
        specular = self.light.color* specular_intensity * material.albedo[1]
        reflection = reflect_color * material.albedo[2]
        refraction = refract_color * material.albedo[3]



        c = diffuse + specular + reflection + refraction

        return c

    def scene_intersect(self, origin, direction):

        zbuffer = float('inf')
        intersect = None
        material = None
        
        for obj in self.scene:
            r_intersect = obj.ray_intersect(origin, direction)

            if r_intersect:
                if r_intersect.distance < zbuffer:
                    zbuffer = r_intersect.distance
                    material = obj.material
                    intersect = r_intersect

        return material, intersect

    def render(self):
        fov = pi/2
        aspectRatio = self.width/self.height
        for x in range(self.height):
            for y in range(self.width):
                if random() > 0:
                    i = (2 * ((x + 0.5) / self.width) - 1) * aspectRatio * tan(fov / 2)
                    j = 1 - 2 * ((y + 0.5) / self.height) * tan(fov / 2)
                    direction = norm(V3(i,j,-1))
                    col = self.cast_ray(V3(0,0,0), direction)
                    self.point(x,y,col)

r = Raytracer(1000, 1000)

r.light = Light(position=V3(10, 10, 20), intensity=2, color = color(255,255,200))

ivory = Material(diffuse=color(100,100,100), albedo=[0.6, 0.3, 0.1, 0], specular=50)
rubber = Material(diffuse=color(80,0,0), albedo=[0.9, 0.1, 0.0, 0], specular=10)
mirror = Material(diffuse=color(255,255,255), albedo=[0, 10, 0.8, 0], specular=1500)
glass = Material(diffuse=color(255,255,255), albedo=[0, 0.5, 0.1, 0.8], specular=150, refractive_index  = 1.5)


r.scene = [ 
    Sphere(V3(0, -1.5, -10), 1.5, ivory),
    Sphere(V3(-2, 1, -5), 10, glass),
    Sphere(V3(1, 1, -8), 1.7, rubber),
    Sphere(V3(0, 5, -20), 5, mirror),
]


r.render()
r.write("r.bmp")
