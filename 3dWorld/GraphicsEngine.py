from Mesh import Mesh
from Material import Material
from Cube import Cube
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import pygame as pg
import numpy as np

#Engine that will handle the Rendering of 3d Object in the 3d Environment
class Engine:
    def __init__(self):

        self.wood_texture = Material("Images/Barbatos.png")
        self.cube_mesh = Mesh("Models/Cube.obj")

        #initialise opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        glEnable(GL_DEPTH_TEST)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480, 
            near = 0.1, far = 10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader,"projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.shader,"model")
        self.viewMatrixLocation = glGetUniformLocation(self.shader,"view")

    #Create the Shader that will be used for the Engine
    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader

    #Render 3D Objects in the Environment
    def render(self, scene):

        #refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)

        view_transform = pyrr.matrix44.create_look_at(
            eye = scene.player.position,
            target = scene.player.position + scene.player.forwards,
            up = scene.player.up, dtype=np.float32
        )
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        self.wood_texture.use()
        glBindVertexArray(self.cube_mesh.vao)
        for cube in scene.cubes:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(cube.eulers), dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(cube.position),dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

        glFlush()

    #Kill the Engine
    def quit(self):
        self.cube_mesh.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
