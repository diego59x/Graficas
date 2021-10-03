import struct
from obj import Obj, Texture
from lib import *
from NumpyDiego import *
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
    self.light = V3(1,1,1)
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

  def display(self, filename='aiuda.bmp'):
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

    nA = next(self.active_vertex_array)
    nB = next(self.active_vertex_array)
    nC = next(self.active_vertex_array)

    bbox_min, bbox_max = bbox(A, B, C)


    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V3(x, y))
        if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
          continue

        if self.current_texture:
          tx = tA.x * w + tB.x * u + tC.x * v
          ty = tA.y * w + tB.y * u + tC.y * v
          # triangle(A,B,C)
          col = self.active_shader(self, bar=(w,u,v), tex_coords=(tx,ty), varyin_normals=(nA,nB,nC) )
        else:
          col = WHITE * 1

        z = A.z * w + B.z * u + C.z * v
        
        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y, col)
          self.zbuffer[x][y] = z

  def transform(self, vertex):
    # returns a vertex 3, translated and transformed

    augmented_vertex = [
      vertex[0],
      vertex[1],
      vertex[2], 
      1 
    ]
    transformed_vertex = vector_multiply_list([augmented_vertex, self.Model, self.View, self.Projection, self.Viewport])
    
    transformed_vertex = [
      (transformed_vertex[0]/transformed_vertex[3]),
      (transformed_vertex[1]/transformed_vertex[3]),
      (transformed_vertex[2]/transformed_vertex[3])
    ]

    return  V3(*transformed_vertex)

    
  def load(self, filename, translate, scale, rotate):
    self.loadModelMatrix(translate, scale, rotate)
    model = Obj(filename)
    vertex_buffer_object = []

    for face in model.vfaces:
        for v in range(len(face)):
            vertex = self.transform(model.vertices[face[v][0] - 1])
            vertex_buffer_object.append(vertex)

        if self.current_texture:
            for v in range(len(face)):
                tvertex = V3(*model.tvertices[face[v][1] - 1])
                vertex_buffer_object.append(tvertex)

        for v in range(len(face)):
            normal = norm(V3(*model.normals[face[v][2] - 1]))
            vertex_buffer_object.append(normal)

    self.active_vertex_array = iter(vertex_buffer_object)

  def loadModelMatrix(self, translate, scale, rotate=(0,0,0)):
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)

    translation_matrix = createMatrix(4,4,
      [1, 0, 0, translate.x,
      0, 1, 0, translate.y,
      0, 0, 1, translate.z,
      0, 0, 0, 1]
    )

    angle = rotate.x
    rotation_matrix_x = createMatrix(4,4,
      [1, 0, 0, 0,
      0, cos(angle), -sin(angle), 0,
      0, sin(angle), cos(angle), 0,
      0, 0, 0, 1]
    )
    angle = rotate.y
    rotation_matrix_y = createMatrix(4,4,
      [cos(angle), 0, sin(angle), 0,
      0, 1, 0, 0,
      -sin(angle), 0, cos(angle), 0,
      0, 0, 0, 1]
    )
    angle = rotate.z
    rotation_matrix_z = createMatrix(4,4,
      [cos(angle), -sin(angle), 0, 0,
      sin(angle), cos(angle), 0, 0,
      0, 0, 1, 0,
      0, 0, 0, 1]
    )
    
    rotation_matrix = matrix_multiply(rotation_matrix_x, matrix_multiply( rotation_matrix_y , rotation_matrix_z))

    scale_matrix =  createMatrix(4,4,
      [scale.x, 0, 0, 0,
      0, scale.y, 0, 0,
      0, 0, scale.z, 0,
      0, 0, 0, 1]
    )

    self.Model = matrix_multiply(translation_matrix, matrix_multiply( rotation_matrix , scale_matrix))

  def loadViewMatrix(self, x, y, z, center):
    M = createMatrix(4,4,
      [x.x, x.y, x.z, 0,
      y.x, y.y, y.z, 0,
      z.x, z.y, z.z, 0,
      0, 0, 0, 1]
    )

    O = createMatrix(4,4,
      [1, 0, 0, -center.x,
      0, 1, 0, -center.y,
      0, 0, 1, -center.z,
      0, 0, 0, 1]
    )

    self.View = matrix_multiply(M ,O)
  def loadProjectionMatrix(self, coeff):
    # coeff para hacer pequeños a los objectos que estan lejos
    self.Projection = createMatrix(4,4,
      [1, 0, 0, 0,
      0, 1, 0, 0,
      0, 0, 1, 0,
      0, 0, coeff, 1]
    )

  def loadViewportMatrix(self, x = 0, y = 0):
    self.Viewport = createMatrix(4,4,
      [self.width/2, 0, 0, x + self.width/2,
      0, self.height/2, 0, y + self.height/2,
      0, 0, 1, 0,
      0, 0, 0, 1]
    )

  def lookAt(self, eye, center, up):
    #up es orientacion de la camara
    z = norm(sub(eye, center))
    x = norm(cross(up,z))
    y = norm(cross(z,x))


    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix(-1/length(sub(eye,center)))
    self.loadViewportMatrix(0,0)

  def draw_arrays(self, polygon):
    if polygon == 'TRIANGLES':
      try:
        while True:
          self.triangle()
      except StopIteration:
          print('Done')

