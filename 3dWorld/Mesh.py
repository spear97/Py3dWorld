from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import ctypes

#The Mesh that rendered from an .obj file
class Mesh:

    #Constructor
    def __init__(self, filename):

        # Load Vertices that will be loaded in the format of:
        # x, y, z, s, t, nx, ny, nz
        self.vertices = self.loadMesh(filename)

        #Set Vertex Count as the length of vertices divided by the number of columns for the vertices
        self.vertex_count = len(self.vertices) // 8

        #Convert the Vertices into an array
        self.vertices = np.array(self.vertices, dtype=np.float32)

        #Initialize a Vertex Array Object for the Mesh 
        self.vao = glGenVertexArrays(1)

        #Create a Vertex Array Object for the Mesh 
        glBindVertexArray(self.vao)

        #Create a Vertex Buffer Object
        self.vbo = glGenBuffers(1)

        #Initialize a Vertex Buffer Object for the Mesh 
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        #Initialize the 3D Model
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        #position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        #texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    
    def loadMesh(self, filename):

        #raw, unassembled data
        v = []
        vt = []
        vn = []
        
        #final, assembled and packed result
        vertices = []

        #open the obj file and read the data
        with open(filename,'r') as f:

            #The Content of the .obj File
            line = f.readline()

            #Read through the content of the .obj
            while line:

                #Get the Firest Space of the current line
                firstSpace = line.find(" ")
                flag = line[0:firstSpace]

                #If the flag is "v", treat data on line as a Vertex-Location for the .obj File
                if flag=="v":
                    line = line.replace("v ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    v.append(l)

                #If the flag is "vt", treat data on line as a Texture-Coordinate for the .obj File
                elif flag=="vt":
                    line = line.replace("vt ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vt.append(l)

                #If the flag is "vt", treat data on line as a Normal-Vector for the .obj File
                elif flag=="vn":
                    line = line.replace("vn ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vn.append(l)

                #If the flag is "f", treat data on line as a Face for the .obj File
                elif flag=="f":

                    #face, three or more vertices in v/vt/vn form
                    line = line.replace("f ","")
                    line = line.replace("\n","")

                    #get the individual vertices for each line
                    line = line.split(" ")
                    faceVertices = []
                    faceTextures = []
                    faceNormals = []
                    for vertex in line:

                        #break out into [v,vt,vn],
                        #correct for 0 based indexing.
                        l = vertex.split("/")
                        position = int(l[0]) - 1
                        faceVertices.append(v[position])
                        texture = int(l[1]) - 1
                        faceTextures.append(vt[texture])
                        normal = int(l[2]) - 1
                        faceNormals.append(vn[normal])

                    # obj file uses triangle fan format for each face individually.
                    # unpack each face
                    triangles_in_face = len(line) - 2

                    vertex_order = []
                    """
                        eg. 0,1,2,3 unpacks to vertices: [0,1,2,0,2,3]
                    """

                    for i in range(triangles_in_face):
                        vertex_order.append(0)
                        vertex_order.append(i+1)
                        vertex_order.append(i+2)

                    for i in vertex_order:

                        for x in faceVertices[i]:
                            vertices.append(x)

                        for x in faceTextures[i]:
                            vertices.append(x)

                        for x in faceNormals[i]:
                            vertices.append(x)

                #Get Next Line of the Content
                line = f.readline()

        return vertices
    
    #Destroy the Mesh's Vertex Array Object and Vertex Buffer Object
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1,(self.vbo,))