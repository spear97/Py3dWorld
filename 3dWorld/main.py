import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Vector import Vector3d
from math import *


def main():

    #Create a Window
    pygame.init()
    display = (800,600)
    win = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    w, h = win.get_size()
    ratio =  w * 1.0 / h
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, ratio, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    #Create Environment Lighting
    glLight(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

    #Enable Depth Test for 3D Environent 
    glEnable(GL_DEPTH_TEST)

    #Camera Positional and Rotational Data
    player_pos, player_rot = Vector3d(), Vector3d()
    UP, DOWN, LEFT, RIGHT = Vector3d(0.0, 0.0, 0.1), Vector3d(0.0, 0.0, -0.1), Vector3d(0.1, 0.0, 0.0), Vector3d(-0.1, 0.0, 0.0)
    

    #Simulation Loop
    while True:

        #Perform input event performed by the User
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #Set and Intialize the keys variables that stores all keys
        keys = pygame.key.get_pressed()

        #Kill Program if ESCAPE or Q Buttons are pressed
        if keys[K_ESCAPE] or keys[K_q]:
            pygame.quit()
            quit()

        #Move Left
        if keys[K_LEFT]:
            player_pos += LEFT
            glTranslate(LEFT.getX(), LEFT.getY(), LEFT.getZ())

        #Move Right
        if keys[K_RIGHT]:
            player_pos += RIGHT
            glTranslate(RIGHT.getX(), RIGHT.getY(), RIGHT.getZ())

        #Move Up
        if keys[K_UP]:
            player_pos += UP
            glTranslate(UP.getX(), UP.getY(), UP.getZ())

        #Move Down
        if keys[K_DOWN]:
            player_pos += DOWN
            glTranslate(DOWN.getX(), DOWN.getY(), DOWN.getZ())

        #Rotate Left
        if keys[K_a]:
            glRotate(-1, 0, 1, 0)
        
        #Rotate Right
        if keys[K_d]:
            glRotate(1, 0, 1, 0)

        #Set Simulation Background
        glClearColor(1, 1, 1, 1)

        #Render the Environment
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )

        #Scene Geometry

        #Disable Lighting
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)

        #Tick Environment
        pygame.display.flip()
        pygame.time.wait(10)


main()