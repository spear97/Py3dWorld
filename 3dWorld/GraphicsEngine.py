from Mesh import Mesh
from Material import Material
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import pygame as pg
import numpy as np

#Engine that will handle the Rendering of 3d Object in the 3d Environment
class Engine:

    #Constructor for Engine
    def __init__(self):

        #Initialize and set the gundam Texture as the Barbados Image (from Gundam Iron Blooded Orphans)
        self.gundam_texture = Material("Images/Barbatos.png")

        #Initialize cube_Mesh as a Cube that was created using Blender
        self.cube_mesh = Mesh("Models/Cube.obj")

        #The Backgroudn Color of the Program that being rendered
        glClearColor(0.0, 0.0, 0.0, 1)

        #Intialize Shader that will be used for the Graphics Engine for the Program
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")

        #Set to use the Shader use for OpenGL
        glUseProgram(self.shader)

        #Set to make Shader uniform according to the ImageTexture as specified by the Texture
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        #Perform a Depth Test for the Environment
        glEnable(GL_DEPTH_TEST)

        #The Projection Matrix that will act as the "Eyes" of the Player
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480, 
            near = 0.1, far = 10, dtype=np.float32
        )

        #Make the Projection Matrix Created and stored in projection_transform uniform
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader,"projection"),
            1, GL_FALSE, projection_transform
        )

        #Make modelMatrixLocation Uniform
        self.modelMatrixLocation = glGetUniformLocation(self.shader,"model")

        #Make viewlMatrixLocation Uniform
        self.viewMatrixLocation = glGetUniformLocation(self.shader,"view")

        #Make the LIght used by the Graphics Engine Uniform
        self.lightLocation = {
            "position": [
                glGetUniformLocation(self.shader, f"Lights[{i}].position")
                for i in range(8)
            ],
            "color": [
                glGetUniformLocation(self.shader, f"Lights[{i}].color")
                for i in range(8)
            ],
            "strength": [
                glGetUniformLocation(self.shader, f"Lights[{i}].strength")
                for i in range(8)
            ]
        }
        self.cameraPosLoc = glGetUniformLocation(self.shader, "cameraPostion")

    #Create the Shader that will be used for the Engine
    def createShader(self, vertexFilepath, fragmentFilepath):

        #Open the Vertex Shader and scrape the Data from it
        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        #Open the Fragment Shader and scrape the Data from it
        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        #Set and Initialize the shader and compile it from the DataSets that were scraped
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        #Return the Shader
        return shader

    #Render 3D Objects in the Environment
    def render(self, scene):

        #refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Set the Shader that will be used
        glUseProgram(self.shader)

        #The View Transform that the Render will use to Render 3d Objects in
        view_transform = pyrr.matrix44.create_look_at(
            eye = scene.player.position,
            target = scene.player.position + scene.player.forwards,
            up = scene.player.up, dtype=np.float32
        )

        #Make the viewMatrixLocation Uniform
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        #Enumerate through all lights that exist in the scene
        for i,light in enumerate(scene.lights):
            glUniform3fv(self.lightLocation["position"][i], 1, light.position)
            glUniform3fv(self.lightLocation["color"][i], 1, light.color)
            glUniform1f(self.lightLocation["strength"][i], light.strength)

        #Make the cameraPosLocation Uniform
        glUniform3fv(self.cameraPosLoc, 1, scene.player.position)

        #Render all Objects that exist in the environment
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
            self.gundam_texture.use()
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            glFlush()

    #Kill the Engine
    def quit(self):
        
        #Destroy the Cube
        self.cube_mesh.destroy()

        #Destory the Gundam Texture
        self.gundam_texture.destroy()

        #Destroy the Shader
        glDeleteProgram(self.shader)