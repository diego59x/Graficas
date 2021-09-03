import struct
from obj import Obj, Texture
from lib import *
from collections import namedtuple

# ===============================================================
# Math
# ===============================================================


class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.current_texture = None
    self.light = V3(0,0,1)
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

  def display(self, filename='out.bmp'):
    self.write(filename)

  def set_color(self, color):
    self.current_color = color

  def point(self, x, y, color = None):
    # 0,0 was intentionally left in the bottom left corner to mimic opengl
    try:
      self.pixels[y][x] = color or self.current_color
    except:
      # To avoid index out of range exceptions
      pass

  def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)

    if self.current_texture:
        tA = next(self.active_vertex_array)
        tB = next(self.active_vertex_array)
        tC = next(self.active_vertex_array)

    bbox_min, bbox_max = bbox(A, B, C)

    normal = norm(cross(sub(B, A), sub(C, A)))
    intensity = dot(normal, self.light)

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V3(x, y))
        if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
          continue
        
        if self.current_texture:
          tx = tA.x * w + tB.x * v + tC.x * u
          ty = tA.y * w + tB.y * v + tC.y * u
          
          fcolor = self.current_texture.get_color(tx,ty)
          col = fcolor * intensity
        else:
          col = WHITE * intensity

        z = A.z * w + B.z * v + C.z * u

        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y, col)
          self.zbuffer[x][y] = z

  def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    # returns a vertex 3, translated and transformed
    return V3(
      round((vertex[0] + translate[0]) * scale[0]),
      round((vertex[1] + translate[1]) * scale[1]),
      round((vertex[2] + translate[2]) * scale[2])
    )
    
  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1)):
    model = Obj(filename)
    vertex_buffer_object = []

    for face in model.vfaces:
        for v in range(len(face)):
            vertex = self.transform(model.vertices[face[v][0] - 1], translate, scale)
            vertex_buffer_object.append(vertex)

        if self.current_texture:
            for v in range(len(face)):
                tvertex = V3(*model.tvertices[face[v][1] - 1])
                vertex_buffer_object.append(tvertex)

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


# r = Renderer(800,600)
# r.current_texture = Texture('./VertexBuffer/models/earth.bmp')
# r.load('./VertexBuffer/models/earth.obj',(1, 1, 1), (300, 300, 300))
# r.draw_arrays('TRIANGLES')
# r.display()