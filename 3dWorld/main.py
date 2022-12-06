import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
from Triangle import Triangle

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
        self.shader = self.createShader("Shaders/Vertex.txt", "Shaders/fragment.txt")
        glUseProgram(self.shader)
        self.triangle = Triangle()
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
        run = 1
        while run:

            #Check if GIANT RED "X" BUTTON has been pressed
            for event in pg.event.get():
                if(event.type == pg.quit):
                    run = 0

            #Refresh the Screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()

    #Kill the Engine
    def quit(self):
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

#If set as Start-up File, Start Engine
if __name__ == '__main__':
    world = Engine()