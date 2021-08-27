import struct
from obj import Obj

def char(c):
  # char
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  # short
  return struct.pack('=h', w)

def dword(w):
  # long
  return struct.pack('=l', w)


def glClearColor(r, g, b):
  color = bytes([b, g, r])
  return color 

BLACK = glClearColor(0,0,0)

WHITE = glClearColor(255,255,255)


class Renderer(object):
  # glinit? mas pinta asi: 
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.widthView = 0
    self.heightView = 0
    self.yHeight = 0
    self.xWidth = 0
    self.current_color = BLACK
    self.color_point = WHITE
    self.glCreateWindow()

  # No es necesario que esta funcion reciba W y H
  # Ya que se setean su valor desde el constructor
  def glCreateWindow(self):
    self.framebuffer = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]

  def glClear(self):
    self.framebuffer = [
      [self.current_color for x in range(self.width)]
      for y in range(self.height)
    ]
  
  def write(self, filename):
    f = open(filename, 'bw')

    # file header 14
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + 3*(self.width*self.height)))
    f.write(dword(0))
    f.write(dword(14 + 40))

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
    self.write('image.bmp')


  def line(self, x0, y0, x1, y1):
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    steep = dy > dx

    if steep:
      x0, y0 = y0, x0
      x1, y1 = y1, x1

      dy = abs(y1 - y0)
      dx = abs(x1 - x0)

    offset = 0 * 2 * dx
    threshold = 0.5 * 2 * dx
    
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

      offset += (dy/dx) * 2 * dx
      if offset >= threshold:
        y += 1 if y0 < y1 else -1
        threshold += 1 * 2 * dx

    for point in points:
      r.glVertex(*point)
      
  def glViewPort(self,xCord,yCord,heightInput,widthInput):

    if (heightInput < self.height and widthInput < self.width):
      self.yHeight = xCord
      self.xWidth = yCord
      self.widthView = widthInput
      self.heightView = heightInput
    else:
      print("Los valores del viewport deben ser menores al de la imagen")
  
  def glVertex(self, x, y, color = None):
    try:
      self.framebuffer[y][x] = color or self.color_point
    except IndexError:
      print("Estas fuera del limite de la imagen o viewport") 
  def load(self, filename, translate, scale):
      model = Obj(filename)
      for face in model.faces:
          vcount = len(face)
          for j in range(vcount):
              f1 = face[j][0]
              f2 = face[ (j + 1 ) % vcount ][0]

              v1 = model.vertices[f1 - 1]
              v2 = model.vertices[f2 - 1]


              x1 = round((v1[0] + translate[0]) * scale[0]) 
              y1 = round((v1[1] + translate[1]) * scale[1])

              x2 = round((v2[0] + translate[0]) * scale[0])
              y2 = round((v2[1] + translate[1]) * scale[1])
              
              self.line(x1,y1,x2,y2)

print("Bienvenido al generador de imagenes")

# size = True

# while(size):
#   heightInput = int(input("Ingrese la altura de su archivo: "))
#   widthInput = int(input("Ingrese el ancho de su archivo: "))
#   if (heightInput > 0 and widthInput > 0):
#     size = False
#   else:
#     print("Ingrese valores positivos")


r = Renderer(5000, 5000)
r.load('./Clase_4/Models/bears.obj', [6,-12], [350,350])
r.glFinish()
# menu = True

# while(menu):
#   print(" 1. Pintar un pixel en la pantalla  \n 2. Cambiar el color de fondo \n 3. Definir el area en la que se pinta \n 4. Cambiar el color con el que se pinta un pixel (el de opcion 1)\n 5. Generar imagen \n 6. salir\n")
#   option = input(" ")
#   if (option == "1"):
#     xCord = float(input("Ingrese coordenada en x: "))
#     yCord = float(input("Ingrese coordenada en y: "))
#     if (r.widthView > 0 and r.heightView > 0):
#       if ((xCord <= 1 and xCord >= -1) and (yCord <= 1 and yCord >= -1)):
#         r.glVertex(int(xCord*r.widthView),int(yCord*r.heightView))
#       else:
#         print("Las coordenadas deben estar entre 0 y 1")
#     else:
#       print("Defina el viewport primero (opcion 3) ")
#   elif (option == "2"):
#     ra = float(input("R: "))
#     g = float(input("G: "))
#     b = float(input("B: "))
#     if ((ra <= 1 and ra >= 0) and (g <= 1 and g >= 0) and (b <= 1 and b >= 0) ):
#       r.current_color = glClearColor(int(ra*255),int(g*255),int(b*255))
#       r.glClear()
#     else:
#       print("Ingresa valores entre 0 y 1")
#   elif (option == "3"):
    
#     size = True
#     while(size):
#       xCord = int(input("Ingrese coordenada en x del viewport: "))
#       yCord = int(input("Ingrese coordenada en y del viewport: "))
#       widthInput = int(input("Ingrese el ancho del viewport: "))
#       heightInput = int(input("Ingrese la altura del viewport: "))
#       if (widthInput > 0 and heightInput > 0 and xCord > 0 and yCord > 0):
#         size = False
#         r.glViewPort(xCord,yCord,heightInput,widthInput)
#       else:
#         print("Ingrese valores positivos")
    
#   elif (option == "4"):
#     ra = float(input("R: "))
#     g = float(input("G: "))
#     b = float(input("B: "))
#     if ((ra <= 1 and ra >= 0) and (g <= 1 and g >= 0) and (b <= 1 and b >= 0) ):
#       r.color_point = glClearColor(int(ra*255),int(g*255),int(b*255))
#       r.glClear()
#     else:
#       print("Ingresa valores entre 0 y 1")
#   elif (option == "5"):
#     print(" Archivo generado 'image.bmp' ")
#     r.glFinish()
#   elif (option == "6"):
#     print("Buena onda oralex")
#     menu = False
#   else:
#     print("Ingrese una opcion existente")


