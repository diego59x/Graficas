
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

class ModelConstants():

    def __init__(self):
        self.i = glm.mat4(1)
        self.translate = glm.translate(self.i, glm.vec3(0, 0, 0))
        self.scale = glm.scale(self.i, glm.vec3(10, 10, 10))
        self.rotate = glm.rotate(self.i, glm.radians(0), glm.vec3(0, 1, 0))
        self.view = glm.lookAt(glm.vec3(0, 0, 20), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        self.projection = glm.perspective(glm.radians(45), 1.667, 0.1, 1000.0) 
   
    def rotationCamera(self, rotate):
        self.rotate = glm.rotate(self.i, glm.radians(rotate), glm.vec3(0, 1, 0))
    
    # def scaleCamera(self, zoomInCamera) 
    #    if (zoomInCamera < 2 and zoomInCamera > 0.1):
    #      self.scaleCamera = glm.scale(i, zoomInCamera * glm.vec3(10, 10, 10))
    def zoomCamera(self, zoomRate):
        # Idk why you have to multiply the angle to make a zoom in or zoom out of the camera
        self.projection = glm.perspective(glm.radians(zoomRate * 45), 1.667, 0.1, 1000.0) 

class shadersConstants():
    def __init__(self) -> None:
        self.vertex_shader_circles = """
            #version 460
            void main() 
            {
                gl_FragCoord = vec4(0.2, 0.3, 0.1, 1.0);
            }
            """
        self.fragment_shader_circles = """
            #version 460
            #ifdef GL_ES
            precision lowp float;
            #endif
            uniform vec4 gl_FragCoord;

            uniform vec2 u_resolution;

            float circle_shape(float radius, vec2 position) {
                float value = distance(position, vec2(0.5));
                return step(radius, value);
            }

            void main() {
                vec2 coord = gl_FragCoord.xy / u_resolution;
                float circleWidth = 8.2;
                float circle = circle_shape(circlewidth, coord);
                vec3 color = vec3(circle);

                gl_FragColor = vec4(color, 1.0);
            }
            """
        self.vertex_shader = """
            #version 460

            layout (location = 0) in vec3 position;
            layout (location = 1) in vec3 ccolor;

            uniform mat4 CameraMatrix;

            out vec3 mycolor;

            void main() 
            {
            gl_Position = CameraMatrix * vec4(position.x, position.y, position.z, 1);
            mycolor = ccolor;
            }
            """

        self.fragment_shader = """
            #version 460
            layout(location = 0) out vec4 fragColor;

            uniform int clock;
            in vec3 mycolor;

            void main()
            {
            if (mod(clock/10, 2) == 0) {
                fragColor = vec4(mycolor.xyz, 1.0f);
            } else {
                fragColor = vec4(mycolor.zxy, 1.0f);
            }
            }
            """

    def shader_Circles(self):
        cvsC = compileShader(self.vertex_shader_circles, GL_VERTEX_SHADER)
        cfsC = compileShader(self.fragment_shader_circles, GL_FRAGMENT_SHADER)
        return cvsC, cfsC

    def shader_normal(self):
        cvs = compileShader(self.vertex_shader, GL_VERTEX_SHADER)
        cfs = compileShader(self.fragment_shader, GL_FRAGMENT_SHADER)
        return cvs, cfs

