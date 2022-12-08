import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
from Triangle import *
from Material import *
from Cube import *
from Mesh import *
import numpy as np
import pyrr

#The Graphics Engine that will Render Objects using the OpenGL API
class Engine:

    #Constructor
    def __init__(self):

        #Initialize Pygame
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        #Initialize OpenGL
        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = self.createShader("Shaders/Vertex.txt", "Shaders/Fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        self.cube = Cube(position=[0,0,-5], eulers=[0,0,0])
        #self.cube_mesh = CubeMesh()
        self.mesh = Mesh('Models/Cube.obj')

        #Define Textures that are going to be used
        self.barbatos_texture = Material("Images/Barbatos.png")
        self.dallas_texture = Material("Images/DallasSkyLine.png")

        #Transformations
        projection_transform = pyrr.matrix44.create_perspective_projection(fovy=45, aspect=640/480, near=0.1, far=10, dtype=np.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection_transform)
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

        self.mainLoop()

    #Create the Shader that will be used for the Engine
    def createShader(self, vertexFilePath, fragmentFilePath):

        with open(vertexFilePath, 'r') as f:
            vertex_sc = f.readlines()

        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_sc,GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader

    #Run the Engine
    def mainLoop(self):
        run = True
        while run:

            #Check if GIANT RED "X" BUTTON has been pressed
            for event in pg.event.get():
                if(event.type == pg.quit):
                    run = False

            #Calclate Cube Rotation
            self.cube.eulers[2] += 0.2
            if (self.cube.eulers[2] > 360):
                self.cube.eulers[2] -= 360

            #Refresh the Screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            #Apply Texture to Shape
            glUseProgram(self.shader)
            self.barbatos_texture.use()

            #Create Model Transform
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

            '''
            Rotate then Move, if you wanna keep it on same origin-Axis
            '''

            #Rotate Cube 
            model_transform = pyrr.matrix44.multiply(m1=model_transform, m2=pyrr.matrix44.create_from_eulers(eulers=np.radians(self.cube.eulers), dtype=np.float32))
            
            #Set Cube to it Position
            model_transform = pyrr.matrix44.multiply(m1=model_transform, m2=pyrr.matrix44.create_from_translation(vec=self.cube.position,dtype=np.float32))
            
            #Upload Cube's Transform
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)

            glBindVertexArray(self.mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.mesh.vertex_count)

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()

    #Kill the Engine
    def quit(self):
        self.mesh.destroy()
        self.barbatos_texture.destory()
        glDeleteProgram(self.shader)
        pg.quit()

#If set as Start-up File, Start Engine
if __name__ == '__main__':
    world = Engine()