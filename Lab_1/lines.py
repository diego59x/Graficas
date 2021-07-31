import struct

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
    self.yHeight = 0
    self.xWidth = 0
    self.current_color = BLACK
    self.color_point = WHITE
    self.pointsFigure = []
    self.cont = 0
    self.refXM = 0
    self.refYM = 0
    self.refXL = 0
    self.refYL = 0
    self.glCreateWindow()

  # No es necesario que esta funcion reciba W y H
  # Ya que se setean su valor desde el constructor
  def glCreateWindow(self):
    self.framebuffer = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]
  # Pintar de un solo color toda la imagen
  def glClear(self):
    self.framebuffer = [
      [self.current_color for x in range(self.width)]
      for y in range(self.height)
    ]
  # Crear el archibo bmp
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
  # Hacer un punto en la pantalla
  def glVertex(self, x, y, color = None):
    self.cont += 1
    try:
      if self.cont == 1:
        self.refXM, self.refXL = x, x
        self.refYM, self.refYL = y, y
      if x > self.refXM: # Mayor en X
        self.refXM = x
      if y > self.refYM: # Mayor en Y
        self.refYM = y
      if x < self.refXL: # Menor en X
        self.refXL = x
      if y < self.refYL: # Menor en Y
        self.refYL = y

      self.pointsFigure.append((x,y))
      self.framebuffer[int(y)][int(x)] = color or self.color_point
    except IndexError:
      print("Estas fuera del limite de la imagen o viewport") 
    
print(".-.-.-.-.-.-.-.-.-.-.-.-. Bienvenido al generador de imagenes .-.-.-.-.-.-.-.-.-.-.-.-.")

size = True

while (size):
  heightInput = int(input("Ingrese la altura de su archivo: "))
  widthInput = int(input("Ingrese el ancho de su archivo: "))
  if (heightInput > 0 and widthInput > 0):
    size = False
  else:
    print("Ingrese valores positivos")

r = Renderer(heightInput, widthInput)


a = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330),
     (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]

for i in range(len(a) - 1):
    r.line(a[i][0], a[i][1], a[i+1][0], a[i+1][1])
    if i == len(a) - 2:
        last_item = len(a) - 2
        r.line(a[last_item+1][0], a[last_item+1][1], a[0][0], a[0][1])


r.glFinish()
print(r.refXM, r.refYM)
print(r.refXL, r.refYL)
area = (r.refXL-r.refXM)*(r.refYL-r.refYM)
print("el area es : ", area)
menu = True

while(menu):
  print(" 1. Pintar un pixel en la pantalla  \n 2. Cambiar el color de fondo \n 3. Cambiar el color con el que se pinta un pixel (el de opcion 1)\n 4. Crear Lineas \n 5. Generar imagen \n 6. salir\n")
  option = input(" ")
  if (option == "1"):
    xCord = float(input("Ingrese coordenada en x: "))
    yCord = float(input("Ingrese coordenada en y: "))
    r.glVertex(round(xCord),round(yCord))
  elif (option == "2"):
    ra = float(input("R: "))
    g = float(input("G: "))
    b = float(input("B: "))
    if ((ra <= 1 and ra >= 0) and (g <= 1 and g >= 0) and (b <= 1 and b >= 0) ):
      r.current_color = glClearColor(round(ra*255),round(g*255),round(b*255))
      r.glClear()
    else:
      print("Ingresa valores entre 0 y 1")
  elif (option == "3"):
    ra = float(input("R: "))
    g = float(input("G: "))
    b = float(input("B: "))
    if ((ra <= 1 and ra >= 0) and (g <= 1 and g >= 0) and (b <= 1 and b >= 0) ):
      r.color_point = glClearColor(round(ra*255),round(g*255),round(b*255))
      r.glClear()
    else:
      print("Ingresa valores entre 0 y 1")

  elif (option == "4"):
    print(".-.-.-.-.-.-. Inicio de linea .-.-.-.-.-.-.")
    xCordS = float(input("Ingrese coordenada en x: "))
    yCordS = float(input("Ingrese coordenada en y: "))
    print(".-.-.-.-.-.-. Fin de linea .-.-.-.-.-.-.")
    xCordE = float(input("Ingrese coordenada en x: "))
    yCordE = float(input("Ingrese coordenada en y: "))
    r.line(xCordS,yCordS,xCordE,yCordE)

  elif (option == "5"):
    print(" Archivo generado 'image.bmp' ")
    r.glFinish()
  elif (option == "6"):
    print("Buena onda oralex")
    menu = False
  else:
    print("Ingrese una opcion existente")
