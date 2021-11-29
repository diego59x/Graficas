from ctypes import pythonapi
import pygame
import numpy
from obj import *
from modelC import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

MODEL = ModelConstants()

pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption('Rendering Objects')

glClearColor(0.1, 0.2, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()

shaders = shadersConstants()
# option = input("\nChoose your shader \n 1. Normals\n 2. Circles\n 3. Dots\n")

# if (option == "1"):
#   cvs, cfs = shaders.shader_normal()
#   shader = compileProgram(cvs, cfs)
# elif (option == "2"):
#   cvsC, cfsC = shaders.shader_Circles()
#   shader = compileProgram(cvsC, cfsC)
# elif (option == "3"):
#   cvsC, cfsC = shaders.shader_Circles()
#   shader = compileProgram(cvsC, cfsC)
# else:
#   cvs, cfs = shaders.shader_normal()
#   shader = compileProgram(cvs, cfs)

cvsC, cfsC = shaders.shader_Circles()
shader = compileProgram(cvsC, cfsC)

mesh = Obj('./Proyect3/models/jarron.obj')

vertex_data = numpy.hstack((
  numpy.array(mesh.vertices, dtype=numpy.float32),
  numpy.array(mesh.normals, dtype=numpy.float32),
)).flatten()

index_data = numpy.array([[vertex[0] - 1 for vertex in face] for face in mesh.vfaces], dtype=numpy.uint32).flatten()


vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(
  0, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  24, # stride
  ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)

element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(
  1, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  24, # stride
  ctypes.c_void_p(12)
)
glEnableVertexAttribArray(1)

glUseProgram(shader)

def render(roteView, zoomInCamera):
  MODEL.rotationCamera(roteView)
  MODEL.zoomCamera(zoomInCamera)

  model = MODEL.translate * MODEL.scale
  CameraMatrix = MODEL.projection * MODEL.view * MODEL.rotate * model

  glUniformMatrix4fv(
    glGetUniformLocation(shader, 'CameraMatrix'),
    1,
    GL_FALSE,
    glm.value_ptr(CameraMatrix)
  )

glViewport(0, 0, 1200, 720)
roteView  = 0
zoomInCamera = 1
running = True
FLAG_RENDER_ONE_TIME = True

# Render first time 
render(roteView, zoomInCamera)

while running:
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  if (zoomInCamera >= 2):
    zoomInCamera = 1
  if (zoomInCamera <= 0.1):
    zoomInCamera = 1

  # Render only if necesary 
  if (zoomInCamera != 1 or roteView != 0):
    render(roteView, zoomInCamera)
  
  glGetUniformLocation(shader, 'clock')

  glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

  pygame.display.flip()
  clock.tick(15)

  keys = pygame.key.get_pressed() 
  if keys[pygame.K_a]: 
    roteView += 5

  if keys[pygame.K_d]: 
    roteView -= 5

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      # render(roteView, zoomInCamera) render only if necesary
      if event.key == pygame.K_w:
        zoomInCamera -= 0.1
      if event.key == pygame.K_s:
        zoomInCamera += 0.1
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # to use normals
