import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from GraphicsEngine import Engine
from Scene import Scene

#Window Parameters
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

#Initialize OpenGL to Create Window
def initialize_glfw():

    #Initialize OpenGL
    glfw.init()

    #Specify the Maximum Size of the Window
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)

    #Specify the Minimum Size of the Window
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)

    #Initialize the OpenGL Version for it to be compatile with the System the Program is running on
    #Mac and Windows
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, 
        GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
    )
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, 
        GLFW_CONSTANTS.GLFW_TRUE
    )

    #Disable DoubleBuffer for OpenGL
    #Do NOT provide two comple color buffers for rendering 3d Objects in the Environment
    glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)

    #Create the Window that will be rendered for the Program
    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "3dWorld", None, None)

    #Render the Created Window for the Window
    glfw.make_context_current(window)

    #Set the Input Mode for the window
    glfw.set_input_mode(
        window, 
        GLFW_CONSTANTS.GLFW_CURSOR, 
        GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN
    )

    #Return the Created Window
    return window

#Program that will be run
class Program:

    #Constructor
    def __init__(self, window):
        
        #The Speed at which the Player will move at
        self.movespeed = 0.1

        #The window that the 3d Environment will render on
        self.window = window

        #The 3d Graphics Engine that 3d Objects will render in
        self.renderer = Engine()

        #The Environement that will contain the 3d Objects
        self.scene = Scene()

        #Get the Current Tick of the Program upon initialization of the program
        self.lastTime = glfw.get_time()

        #The Current Time for the 3d Environment, used to calculate FPS (Frames Per Second)
        self.currentTime = 0

        #Number of frames that have gone by
        self.numFrames = 0

        #The current Frame that the program is one
        self.frameTime = 0
        
        #Run the Program
        self.mainLoop()

    #Run the Program
    def mainLoop(self):

        #Run the Program Infinitly
        while True:
            
            #Close the Window by pressing the Escape Key
            if glfw.window_should_close(self.window) \
                or glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                    break
            
            #Handle User Input from the Keyboard
            self.handleKeys()

            #Handle User Input from Mouse
            self.handleMouse()
            
            #Process all inputs inputted from User
            glfw.poll_events()

            #Update all Objects in the Environment
            self.scene.update(self.frameTime / 16.7)

            #Render all 3d Objects in the Environment
            self.renderer.render(self.scene)

            #Calculate the FPS for the 3D Environment
            self.calculateFramerate()

        #Kill the Program
        self.quit()

    def handleKeys(self):

        combo = 0
        directionModifier = 0
        """
        w: 1 -> 0 degrees
        a: 2 -> 90 degrees
        w & a: 3 -> 45 degrees
        s: 4 -> 180 degrees
        w & s: 5 -> x
        a & s: 6 -> 135 degrees
        w & a & s: 7 -> 90 degrees
        d: 8 -> 270 degrees
        w & d: 9 -> 315 degrees
        a & d: 10 -> x
        w & a & d: 11 -> 0 degrees
        s & d: 12 -> 225 degrees
        w & s & d: 13 -> 270 degrees
        a & s & d: 14 -> 180 degrees
        w & a & s & d: 15 -> x
        """

        #Caclute the Combo that will determine the direction the Player will move towards
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 1
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 2
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 4
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 8
        
        #Move towards calculated direction, assuming that Combo is a number that is greater than 0
        if combo > 0:
            if combo == 3:
                directionModifier = 45
            elif combo == 2 or combo == 7:
                directionModifier = 90
            elif combo == 6:
                directionModifier = 135
            elif combo == 4 or combo == 14:
                directionModifier = 180
            elif combo == 12:
                directionModifier = 225
            elif combo == 8 or combo == 13:
                directionModifier = 270
            elif combo == 9:
                directionModifier = 315
            
            #Calculate the Position that Player will move to 
            dPos = [
                self.frameTime * 0.025 * np.cos(np.deg2rad(self.scene.player.theta + directionModifier)),
                self.frameTime * 0.025 * np.sin(np.deg2rad(self.scene.player.theta + directionModifier)),
                0
            ]

            #Move Player
            self.scene.move_player(dPos)

    #Get the Mouse Input of the Player
    def handleMouse(self):

        #The X,Y Coordinates of that the Mouse Cursosr is at
        (x,y) = glfw.get_cursor_pos(self.window)

        #The rate that the Player's Camera will rotate at
        rate = self.frameTime / 16.7

        #The Horizontal Incremental Rate that the Player will rotate at 
        theta_increment = rate * ((SCREEN_WIDTH/2) - x)

        #The Vertical Incremental Rate that the Plaer will rotate at
        phi_increment = rate * ((SCREEN_HEIGHT/2) - y)

        #Rotate the Player for the caculated Horizontal and Vertical Rates
        self.scene.spin_player(theta_increment, phi_increment)

        #Lock the Cursor Position of the Mouse to remaind at the Center of the Screen
        glfw.set_cursor_pos(self.window, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    #Calculate the Current Frame Rate of the Program
    def calculateFramerate(self):

        #Get the Current Tick of the Program
        self.currentTime = glfw.get_time()

        #Calculate the delta between the Current Tick and that last Tick Performed
        delta = self.currentTime - self.lastTime

        #If the delta is at or exceeds 1
        if (delta >= 1):

            #Cap at the current Number of Frames of the Calculated Delta
            framerate = max(1, int(self.numFrames / delta))

            #Update the last Tick to the Current Tick
            self.lastTime = self.currentTime

            #Reset the Number of Frames
            self.numFrames = -1

            #Caculate the FPS (Frames Per Second) for the Program
            self.frameTime = float(1000.0/max(1,framerate))

        #Increment the Current Frame Number
        self.numFrames += 1

    #Kill the Program
    def quit(self):
        self.renderer.quit()

#If set as Start-up File, Start Engine
if __name__ == '__main__':

    #Initizlalize the Window for the Program
    window = initialize_glfw()

    #Intialize the Program that will be ran
    world = Program(window)