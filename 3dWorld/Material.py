from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

#Will Determine the Image that will applied to a given 3d/2d Object
#Determine it's color and look based on the texture's color and look
class Material:

    #Constructor
    def __init__(self, filepath):

        #Set Texture as a Texture from the Shader
        self.texture = glGenTextures(1)

        #Created a named Texture
        glBindTexture(GL_TEXTURE_2D, self.texture)

        #The Horizontal Position of the Texture's Pixel projectied on the 3d Object
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)

        #The Vertical Position of the Texture's Pixel projected on the 3d Object
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        #Get the Minimum Scale of the 3d Object's Texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)

        #Get the Maximum Scale of the 3d Object's Texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #Scrape the Data from the 3d Object
        with Image.open(filepath, mode = "r") as image:

            #Get the Height and Width Value from the Image
            image_width,image_height = image.size

            #Set the Object to Read Pixel as: Red, Blue, Green, and Alpha(Transparent) Values
            image = image.convert("RGBA")

            #Compress the Image into bytes
            img_data = bytes(image.tobytes())

            #Calculate the Projected Texture Map to the 3d Object
            glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

        #Genetate the MipMap for the 3d Object
        glGenerateMipmap(GL_TEXTURE_2D)

    #Set the Texture to be used as a shader for the 3d Object
    def use(self):

        #Set the Teture as Active
        glActiveTexture(GL_TEXTURE0)

        #Bind the Texture to a 3d Object
        glBindTexture(GL_TEXTURE_2D,self.texture)

    #Destory the Texture for the 3d Object
    def destroy(self):
        glDeleteTextures(1, (self.texture,))

