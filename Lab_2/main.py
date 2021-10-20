import struct
from obj import Obj, Texture
from lib import *
import random
from collections import namedtuple

class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.current_texture = None
    self.light = V3(0,0,3)
    self.clear()

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)] 
      for y in range(self.height)
    ]
    self.zbuffer = [
      [-99999 for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    f = open(filename, 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(54 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(54))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Pixel data (width x height x 3 pixels)
    for x in range(self.height):
      for y in range(self.width):
        f.write(self.pixels[x][y].toBytes())

    f.close()

  def display(self, filename='planet.bmp'):
    self.write(filename)

  def set_color(self, color):
    self.current_color = color

  def line(self, x0, y0, x1, y1, color=None):
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    steep = dy > dx

    if steep:
      x0, y0 = y0, x0
      x1, y1 = y1, x1

      dy = abs(y1 - y0)
      dx = abs(x1 - x0)

    offset = 0
    threshold = 2.5 * dx
    
    # y = mx + b
    if x1 < x0:
      y = y1
      x0, x1 = x1, x0
      y0, y1 = y1, y0
    else:
      y = y0
    points = []
    for x in range(int(x0), int(x1)):
      if steep:
        points.append((y, x))
      else:
        points.append((x, y))

      offset += dy * 2 
      if offset >= threshold:
        y += 1 if y0 < y1 else -1
        threshold += 2 * dx

    for point in points:
      r.point(*point,color)

  def point(self, x, y, color = None):
    try:
      self.pixels[y][x] = color or self.current_color
    except:
      pass

  def shader(self,x,y):
    x_center , y_center = 405, 310
    radius = 200
    x_centerDown , y_centerDown = 450, 200
    radiusDown = 10
    radiusPoint = 8
    # Circulo de derecha abajo 
    if (x - x_centerDown )**2 + (y  - y_centerDown )**2   < (radiusDown**2 ):
      if (x - x_centerDown )**2 + (y  - y_centerDown )**2   < (radiusPoint**2 ):
          self.point(x,y,color(27,23,21))
          return color(27,23,21)
      self.line(x_centerDown,y_centerDown,(x_centerDown+random.randint(-40,30)),y_centerDown+random.randint(-40,90),color(255,255,255))
      return color(255,255,255)
    # Elipse
    if (self.elipse(x_center, y_center + 40, x , y * random.randint(0,3) ,180,130) < 1):
      self.point(x, y, color(120,74,38))
      return color(120,74,38)
    if (x - 300 )**2 + (y  - 300 )**2   < (20**2 ):
      self.line(x,y,(300+random.randint(-40,30)),300+random.randint(-40,90),color(120,74,38))
      return color(120,74,38)
    # Lineas 
    if (x > 590):
      lineX, lineY = self.square(595,580,340,320)
      self.line(lineX, lineY,x_center,y_center, color(120,74,38))
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
    if (x < 590 and x > 400):
      lineX, lineY = self.square(505,488,420,442)
      self.line(lineX, lineY,x_center,y_center, color(120,74,38))
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
    if (x < 540 and x > 400):
      lineX, lineY = self.square(402,260,401,502)
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
    if x < x_center and y > y_center:
      lineX, lineY = self.square(212, 347, 209, 348)
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
      lineX, lineY = self.square(230, 401, 229, 402)
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
      lineX, lineY = self.square(211, 347, 211, 349)
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
      lineX, lineY = self.square(228, 398, 226, 395)
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
      lineX, lineY = self.square(227, 395, 227, 398)
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))
      lineX, lineY = self.square(209, 347, 235, 413)
      self.line(lineX, lineY,x_centerDown,y_centerDown, color(120,74,38))

    if (x * random.randint(0,3) - x_center )**2 + (y * random.randint(0,3)< - y_center )**2   > (radius**2 ):
      self.point(x,y ,color(200,200,200))
      
      return color(200,200,200)

    
    #print(A.x,A.y,A.z)
    return color(255,255,255)

  def square(self,refXM,refXL,refYM,refYL):
    centerX = ((refXM-refXL)/2) + refXL
    centerY = ((refYM-refYL)/2) + refYL
    return int(centerX), int(centerY)

  def elipse(self,h,k,x,y,a,b):
    inside = ((((x - h)**2) / a ** 2) + ((y - k)** 2 / b**2))
    return inside

  def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)
    x_center , y_center = 405, 310
    radiusPoint = 180
    bbox_min, bbox_max = bbox(A, B, C)

    normal = norm(cross(sub(B, A), sub(C, A)))
    intensity = dot(normal, self.light)

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V3(x, y))
        if w < 0 or v < 0 or u < 0: 
          continue
        
        if (x - x_center )**2 + (y  - y_center )**2 > (radiusPoint**2 ):
          col = self.shader(x,y) * intensity
        else:
          col = self.shader(x,y)

        z = A.z * w + B.z * v + C.z * u

        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y, col)
          self.zbuffer[x][y] = z

  def transform(self, vertex, translate, scale):
    # returns a vertex 3, translated and transformed
    return V3(
      round((vertex[0] * scale[0] + translate[0])),
      round((vertex[1] * scale[1] + translate[1])),
      round((vertex[2] * scale[2] + translate[2]))
    )
    
  def load(self, filename, translate, scale):
    model = Obj(filename)
    vertex_buffer_object = []

    for face in model.vfaces:
        for v in range(len(face)):
            vertex = self.transform(model.vertices[face[v][0] - 1], translate, scale)
            vertex_buffer_object.append(vertex)

    self.active_vertex_array = iter(vertex_buffer_object)


  def draw_arrays(self, polygon):
    if polygon == 'WIREFRAME':
      pass
    elif polygon == 'TRIANGLES':
      try:
        while True:
          self.triangle()
      except StopIteration:
          print('Done')


r = Renderer(800,600)
r.load('./Lab_2/models/esfera.obj',(400, 300, 1), (400, 400, 400))
r.draw_arrays('TRIANGLES')
r.display()