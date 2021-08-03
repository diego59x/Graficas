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
  
  def glFinish(self, filename):
    self.write(filename)

  def line(self, x0, y0, x1, y1):
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

      # Tomando todos los puntos de los bordes de la figura
      self.pointsFigure.append([x,y])
      self.framebuffer[int(y)][int(x)] = color or self.color_point
    except IndexError:
      print("Estas fuera del limite de la imagen o viewport") 


  def glPoligon(self, coordinates):
    # Dibujando unicamente lo bordes
    for coor in range(len(coordinates) - 1):
      r.line(coordinates[coor][0], coordinates[coor][1], coordinates[coor+1][0], coordinates[coor+1][1])
      if coor == len(coordinates) - 2:
        final = len(coordinates) - 2
        r.line(coordinates[final+1][0], coordinates[final+1][1], coordinates[0][0], coordinates[0][1])

    # Calculando el punto central de la figura
    centerX = ((r.refXM-r.refXL)/2) + r.refXL
    centerY = ((r.refYM-r.refYL)/2) + r.refYL
    points = r.pointsFigure
    # Rellenano la imagen a traves del centro la figura
    for point in range(len(points)):
      r.line(centerX,centerY,points[point][0],points[point][1])
      r.line(centerX+12,centerY+12,points[point][0],points[point][1])
      r.line(centerX,centerY-12,points[point][0],points[point][1])
      r.line(centerX-12,centerY-12,points[point][0],points[point][1])
      r.line(centerX-12,centerY,points[point][0],points[point][1])
    

poligono1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
poligono2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
poligono3 = [(377, 249), (411, 197), (436, 249)]
poligono4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)]
poligono5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

print(".-.-.-.-.-.-.-.-.-.-.-.-. Bienvenido al generador de imagenes .-.-.-.-.-.-.-.-.-.-.-.-.")
size = True

while (size):
  print(".-.-.-.-.-.-.-.-.-.-.-.-. Usa 800x800 como recomendacion .-.-.-.-.-.-.-.-.-.-.-.-.")
  heightInput = int(input("Ingrese la altura de su archivo: "))
  widthInput = int(input("Ingrese el ancho de su archivo: "))
  if (heightInput > 0 and widthInput > 0):
    size = False
  else:
    print("Ingrese valores positivos")

menu = True
while (menu):
  opcion = input("Que imagen desea rendereizar ?\n 1. Estrella \n 2. Rombo \n 3. Triangulo \n 4. Tetera \n 5. Poligono \n 6. Salir \n")

  if opcion == "1":
    r = Renderer(heightInput, widthInput)
    r.glPoligon(poligono1)
    r.glFinish('render1.bmp')
  elif opcion == "2":
    r = Renderer(heightInput, widthInput)
    r.glPoligon(poligono2)
    r.glFinish('render2.bmp')
  elif opcion == "3":
    r = Renderer(heightInput, widthInput)
    r.glPoligon(poligono3)
    r.glFinish('render3.bmp')
  elif opcion == "4":
    r = Renderer(heightInput, widthInput)
    r.glPoligon(poligono4)
    # Cambiar color a negro para pintar el agujero
    # Setear de nuevo todo a cero para la segunda figura
    r.color_point = glClearColor(0,0,0)
    r.refXM = 0
    r.refXL = 0
    r.refYM = 0
    r.refYL = 0
    r.pointsFigure = []
    r.cont = 0 
    r.glPoligon(poligono5)
    r.glFinish('render4.bmp')
  elif opcion == "5":
    r = Renderer(heightInput, widthInput)
    r.glPoligon(poligono5)
    r.glFinish('render5.bmp')
  elif opcion == "6":
    print("Orale ")
    menu = False
  else:
    print("Opcion invalida")
