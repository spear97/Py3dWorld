from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from Mesh import Mesh
from Material import Material

#Stores Location, Rotation, Mesh to be used, and Material to be used for that Mesh
class Parameters:

    #Constructor
    def __init__(self, position, rotation, mesh_filename, img_filename):

        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation, dtype=np.float32)
        self.mesh = Mesh(mesh_filename)
        self.texture = Material(img_filename)

