import struct

class V3(object):
    def __init__(self,x,y,z = None):
        self.x = x
        self.y = y 
        self.z = z

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
    
    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

def ccolor(v):
    return max(0, min(255, int(v)))

class color(object):
    def __init__(self,r,g,b = None):
        self.r = r
        self.g = g 
        self.b = b

    def __repr__(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)
        return "color(%s, %s, %s)" % (r, g, b)

    def __add__(self, other):
        b = ccolor(self.b + other.b)
        g = ccolor(self.g + other.g)
        r = ccolor(self.r + other.r)
        return color(r,g,b)

    def __mul__(self, other):
        b = ccolor(self.b * other)
        g = ccolor(self.g * other)
        r = ccolor(self.r * other)
        return color(r,g,b)

    def toBytes(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)
        return bytes([b,g,r])

class Material(object):
  def __init__(self, diffuse, albedo, specular):
    self.albedo = albedo
    self.diffuse = diffuse
    self.specular = specular

  def __repr__(self):
    return 'Diffuse: ' + self.diffuse

class Intersect(object):
  def __init__(self, distance, point, normal):
    self.point = point
    self.normal = normal
    self.distance = distance

class Light(object):
  def __init__(self, position, intensity, color):
    self.position = position
    self.intensity = intensity
    self.color = color

def reflect(I,N):
  return norm(sub(I, mul(N, 2 * (dot(I, N)))))

def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
   
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
    
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
   
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
   
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]
  xs.sort()
  ys.sort()

  return V3(round(xs[0]), round(ys[0])), V3(round(xs[-1]), round(ys[-1]))

def barycentric(A, B, C, P):
  
  vectors = cross( 
    V3(B.x - A.x, C.x - A.x, A.x - P.x ),
    V3(B.y - A.y, C.y - A.y, A.y - P.y )
  )
  
  cx, cy, cz = vectors.__getitem__(0), vectors.__getitem__(1), vectors.__getitem__(2)

  if abs(cz) < 1:
    return -1, -1, -1

  u = cx / cz 
  v = cy / cz
  w = 1 - (cx + cy) / cz 

  return w, v, u

def writeBMP(filename, width, height, pixels):
    f = open(filename, 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(54 + width * height * 3))
    f.write(dword(0))
    f.write(dword(54))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(width))
    f.write(dword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(width * height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Pixel data (width x height x 3 pixels)
    for x in range(height):
      for y in range(width):
        f.write(pixels[x][y].toBytes())

    f.close()


# ===============================================================
# Utils
# ===============================================================


def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
