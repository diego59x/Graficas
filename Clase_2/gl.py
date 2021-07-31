import struct
from typing import Tuple

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
      self.framebuffer[y+int(self.width/2)][x+int(self.height/2)] = color or self.color_point
    except IndexError:
      print("Estas fuera del limite de la imagen o viewport") 


print("Bienvenido al generador de imagenes")

size = True

while(size):
  heightInput = int(input("Ingrese la altura de su archivo: "))
  widthInput = int(input("Ingrese el ancho de su archivo: "))
  if (heightInput > 0 and widthInput > 0):
    size = False
  else:
    print("Ingrese valores positivos")
r = Renderer(heightInput, widthInput)

menu = True

while(menu):
  print(" 1. Pintar un pixel en la pantalla  \n 2. Cambiar el color de fondo \n 3. Definir el area en la que se pinta \n 4. Cambiar el color con el que se pinta un pixel (el de opcion 1)\n 5. Generar imagen \n 6. salir\n")
  option = input(" ")
  if (option == "1"):
    xCord = float(input("Ingrese coordenada en x: "))
    yCord = float(input("Ingrese coordenada en y: "))
    if (r.widthView > 0 and r.heightView > 0):
      if ((xCord <= 1 and xCord >= -1) and (yCord <= 1 and yCord >= -1)):
        r.glVertex(int(xCord*(r.widthView/2)),int(yCord*(r.heightView/2)))
      else:
        print("Las coordenadas deben estar entre 0 y 1")
    else:
      print("Defina el viewport primero (opcion 3) ")
  elif (option == "2"):
    ra = float(input("R: "))
    g = float(input("G: "))
    b = float(input("B: "))
    if ((ra <= 1 and ra >= 0) and (g <= 1 and g >= 0) and (b <= 1 and b >= 0) ):
      r.current_color = glClearColor(int(ra*255),int(g*255),int(b*255))
      r.glClear()
    else:
      print("Ingresa valores entre 0 y 1")
  elif (option == "3"):
    
    size = True
    while(size):
      xCord = int(input("Ingrese coordenada en x del viewport: "))
      yCord = int(input("Ingrese coordenada en y del viewport: "))
      widthInput = int(input("Ingrese el ancho del viewport: "))
      heightInput = int(input("Ingrese la altura del viewport: "))
      if (widthInput > 0 and heightInput > 0 and xCord > 0 and yCord > 0):
        size = False
        r.glViewPort(xCord,yCord,heightInput,widthInput)
      else:
        print("Ingrese valores positivos")
    
  elif (option == "4"):
    ra = float(input("R: "))
    g = float(input("G: "))
    b = float(input("B: "))
    if ((ra <= 1 and ra >= 0) and (g <= 1 and g >= 0) and (b <= 1 and b >= 0) ):
      r.color_point = glClearColor(int(ra*255),int(g*255),int(b*255))
      r.glClear()
    else:
      print("Ingresa valores entre 0 y 1")
  elif (option == "5"):
    print(" Archivo generado 'image.bmp' ")
    r.glFinish()
  elif (option == "6"):
    print("Buena onda oralex")
    menu = False
  else:
    print("Ingrese una opcion existente")


