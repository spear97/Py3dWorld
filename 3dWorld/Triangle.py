from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import ctypes


#Render a Triangle in OpenGL
class Triangle:
    def __init__(self):
        
        #Vertices that will make up the Triangle
        #Categorized by: x, y, z, r, g, b
        self.verticies = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0
            )

        #Converting verticies from a tuple to an array using numpy
        self.verticies = np.array(self.verticies, dtype=np.float32)

        #Initializing and Set the vertex count variable for the Triangle as 3
        self.vertex_count = 3

        #Initialize and Set Triangle's VAO (Vertex Array Object)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao) #Bind the VAO to the Graphics Card

        #Initialize and Set Triangle's VAO (Vertex Buffer Object)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #Bind the VBO to the Graphics Card

        #Load in verticies to the Graphics
        glBufferData(GL_ARRAY_BUFFER, self.verticies.nbytes, self.verticies, GL_STATIC_DRAW)

        #Enable and Load Fragment Shaders
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))



    #Destructor for the Triangle - for data to be removed from Graphics Card
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao))
        glDeleteBuffers(1, (self.vbo))