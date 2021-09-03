import struct
from obj import Obj
from collections import namedtuple

def char(c):
  # char
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  # short
  return struct.pack('=h', w)

def dword(w):
  # long
  return struct.pack('=l', w)

def color(r, g, b):
    return bytes([b, g, r])

def minBox(A, B ,C):
  xmins = [A.x, B.x, C.x]
  xmins.sort()
  ymins = [A.y, B.y, C.y]
  ymins.sort()
  return xmins[0], xmins[-1], ymins[0], ymins[-1]

def glClearColor(r, g, b):
  color = bytes([b, g, r])
  return color 


def cross(v0, v1):
  cx = v0.y * v1.z - v0.z * v1.y
  cy = v0.z * v1.x - v0.x * v1.z
  cz = v0.x * v1.y - v0.y * v1.x

  return V3(cx, cy, cz)

def barycentric(A, B, C, P):
  cx, cy, cz = cross( 
    V3(B.x - A.x, C.x - A.x, A.x - P.x ),
    V3(B.y - A.y, C.y - A.y, A.y - P.y )
  )
  
  if abs(cz) < 1:
    return -1, -1, -1

  u = cx / cz 
  v = cy / cz
  w = 1 - (cx + cy) / cz 

  return w, v, u

def sub(v0,v1):

  return V3(
    v0.x - v1.x,
    v0.y - v1.y,
    v0.z - v1.z,
  )

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2) ** 0.5

def norm(v0):
  l = length(v0)
  if l == 0:
    return V3(0,0,0)
  return V3(
    v0.x / l,
    v0.y / l,
    v0.z / l
  )

def dot(v0,v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

BLACK = glClearColor(0,0,0)

WHITE = glClearColor(255,255,255)
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])


class Renderer(object):
  # glinit? mas pinta asi: 
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = BLACK
    self.color_point = WHITE
    self.light = V3(0, 0, 1)
    self.glClear()

  def glClear(self):
    self.framebuffer = [
      [self.current_color for x in range(self.width)]
      for y in range(self.height)
    ]
    self.zbuffer = [
      [-99999 for x in range(self.width)]
      for y in range(self.height)
    ]
  
  def write(self, filename):
    f = open(filename, 'bw')

    # file header 14
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(54 + 3*(self.width*self.height)))
    f.write(dword(0))
    f.write(dword(54))

    # info header 40
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(3*(self.width*self.height)))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    
    # bitmap
    for y in range(self.height):
      for x in range(self.width):
        f.write(self.framebuffer[y][x])

    f.close()
  
  def glFinish(self):
    self.write(b'image.bmp')

  def glVertex(self, x, y, color=None):
    #print("coordenadas ", x, y)
    self.framebuffer[y][x] = color or self.color_point

  def triangle(self, A, B, C, color=None):
    xmin, xmax, ymin, ymax = minBox(A,B,C)

    for x in range(xmin, xmax + 1):
      for y in range(ymin, ymax + 1):
        P = V2(x,y)
        w, v, u = barycentric(A, B , C, P)
        if w < 0 or v < 0 or u < 0:
          continue
        z = A.z * w + B.z * v + C.z * u 
        try:
          if z > self.zbuffer[x][y]:
            self.glVertex(x,y,color)
            self.zbuffer[x][y] = z
        except:
          pass
  def transform(self, vertex, translate, scale):
    return V3( 
      round((vertex[0] * scale[0] + translate[0])),
      round((vertex[1] * scale[1] + translate[1])),
      round((vertex[2] * scale[2] + translate[2]))
    )
  def load(self, filename, translate, scale):

    model = Obj(filename)

    for face in model.vfaces:
      vcount = len(face)

      if vcount == 3:
        face1 = face[0][0] - 1
        face2 = face[1][0] - 1
        face3 = face[2][0] - 1

        v1 = model.vertices[face1]
        v2 = model.vertices[face2]
        v3 = model.vertices[face3]

        a = self.transform(v1,translate, scale)
        b = self.transform(v2,translate, scale)
        c = self.transform(v3,translate, scale)
     
        normal = cross(sub(b, a), sub(c, a))
        intensity = dot(norm(normal), norm(self.light))
        grey = round(255 * intensity)
        if grey < 0:
          continue

        intensity_color = color(grey, grey, grey)
        self.triangle(a, b, c, intensity_color)
      else:
          face1 = face[0][0] - 1
          face2 = face[1][0] - 1
          face3 = face[2][0] - 1
          face4 = face[3][0] - 1

          v1 = model.vertices[face1]
          v2 = model.vertices[face2]
          v3 = model.vertices[face3]
          v4 = model.vertices[face4]

          a = self.transform(v1,translate, scale)
          b = self.transform(v2,translate, scale)
          c = self.transform(v3,translate, scale)
          d = self.transform(v4,translate, scale)

          normal = cross(sub(b, a), sub(c, a))

          intensity = dot(norm(normal), norm(self.light))
          grey = round(255 * intensity)
          if grey < 0:
            continue

          intensity_color = color(grey, grey, grey)

          self.triangle(a, b, c, intensity_color)
          self.triangle(a, c, d, intensity_color)



print("Bienvenido al generador de imagenes")

r = Renderer(800,600)
r.load('./SR4_FlatShading/models/porsche.obj',(400, 300, 1), (200, 200, 200))
r.glFinish()
