import struct

def try_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueeRROR:
        return val


class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()

    self.vertices = []
    self.tvertices = []
    self.faces = []
    self.read()

  def read(self):
    for line in self.lines:
      if line:
        prefix, value = line.split(' ', 1)

        if prefix == 'v':
          self.vertices.append(
            list(map(float, value.split(' ')))
          )
        elif prefix == 'vt':
          self.tvertices.append(
            list(map(float, value.split(' ')))
          )
        elif prefix == 'f':
          self.faces.append(
            [list(map(int, face.split('/'))) for face in value.split(' ')]
          )