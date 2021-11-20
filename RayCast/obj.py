from _typeshed import Self
from os import fdopen
import struct
from lib import *
from math import pi, acos, atan2

def try_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val


class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices = []
        self.normals = []
        self.vfaces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
              try: 
                  prefix, value = line.split(' ', 1)
              except:
                  prefix = ''
              if prefix == 'v':
                  self.vertices.append(list(map(float, value.split(' '))))
              if prefix == 'vt':
                  self.tvertices.append(list(map(float, value.split(' '))))    
              if prefix == 'vn':
                  self.normals.append(list(map(float, value.split(' '))))    
              elif prefix == 'f':
                  self.vfaces.append([list(map(try_int, face.split('/'))) for face in value.split(' ')])

class Texture(object):
    def __init__(self,path):
      self.path = path
      self.pixels = []
      self.pixelsColors = []
      self.lenPixels = 0

      self.read()

    def read(self):
      image = open(self.path, 'rb')
      image.seek(10)
      
      header_size = struct.unpack('=l',image.read(4))[0]

      image.seek(18)
      self.width = struct.unpack('=l', image.read(4))[0]
      self.height = struct.unpack('=l', image.read(4))[0]

      image.seek(header_size)

      for y in range(self.height):
        self.pixels.append([])
        for x in range(self.width):
            b = ord(image.read(1))
            g = ord(image.read(1))
            r = ord(image.read(1))
            self.pixels[y].append(color(r,g,b))
            self.pixelsColors.append(color(r,g,b))
      self.lenPixels = len(self.pixelsColors)

      image.close()
      return self.pixels

    def get_color(self, direX, direY, direZ):

      x = int((atan2(direZ, direX) / (2 * pi) + 0.5) * self.width)
      y = int(acos(-direY) / pi * self.height)
      index = (y * self.width + x) % self.lenPixels
    
      return self.pixelsColors[index]
