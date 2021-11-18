import pygame
import numpy
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm

pygame.init()

screen = pygame.display.set_mode((500,500), pygame.OPENGL | pygame.DOUBLEBUF) 
clock = pygame.time.Clock()
glClearColor(0.5, 0.2, 0.5, 1.0)

vertex_shader = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor;

uniform float flip; 
uniform mat4 theMatrix;

out vec3 mycolor; 

void main()
{
    gl_Position = theMatrix * vec4(position.x, position.y * flip, position.z, 1);
    mycolor = ccolor;
}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;
in vec3 mycolor;

void main()
{
    fragColor = vec4(mycolor, 1.0f);
}
"""

cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)

vertex_data = numpy.array([
  0.5,   0.5,   0, 1.0, 0.0, 0.0,
  0.5,  -0.5,  0, 0.0, 1.0, 0.0,
  -0.5, -0.5, 0, 0.0, 0.0, 1.0,
  -0.5,  0.5,  0, 1.0, 0.0, 1.0

], dtype=numpy.float32)

index_data = numpy.array([
    1, 2, 3,
    0, 1, 3
], dtype=numpy.uint32)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)


vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
    0, # location
    3, # size
    GL_FLOAT, # type
    GL_FALSE, # normalize
    24, # stride
    ctypes.c_void_p(0)
)

glEnableVertexAttribArray(0)

glVertexAttribPointer(
    1, # location
    3, # size
    GL_FLOAT, # type
    GL_FALSE, # normalize
    24, # stride
    ctypes.c_void_p(12)
)

glEnableVertexAttribArray(1)

glUseProgram(shader)

def render(a):
    i = glm.mat4(1)

    translate = glm.translate(i, glm.vec3(0))
    rotate  = glm.rotate(i, a, glm.vec3(0,1,0)) 
    scale = glm.scale(i, glm.vec3(1,1,1))

    model = translate * rotate * scale 
    view = glm.lookAt(glm.vec3(0,0,5), glm.vec3(0,0,0), glm.vec3(0,1,0))

    projection = glm.perspective(glm.radians(a), 1200/720, 0.1, 1000.0)

    theMatrix = projection * view * model


    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'theMatrix'), 
        1,
        GL_FALSE,
        glm.value_ptr(theMatrix)
    )

glViewport(0,0,1200,720)

flipside = 1.0
a = 0
running = True
while True:
    glClear(GL_COLOR_BUFFER_BIT)


    glUniform1f(
        glGetUniformLocation(shader, 'flip'), 
        flipside
    )

    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 3)
    render(a)
    a += 1
    
    pygame.display.flip()
    clock.tick(30)
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_a:
                flipside *= -1.0
        