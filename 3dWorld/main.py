import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from GraphicsEngine import Engine
from Scene import Scene

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RETURN_ACTION_CONTINUE = 0
RETURN_ACTION_END = 1

def initialize_glfw():

    glfw.init()
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, 
        GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
    )
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, 
        GLFW_CONSTANTS.GLFW_TRUE
    )
    glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)

    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "3dWorld", None, None)
    glfw.make_context_current(window)
    glfw.set_input_mode(
        window, 
        GLFW_CONSTANTS.GLFW_CURSOR, 
        GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN
    )

    return window


#Program that will be run
class Program:

    #Constructor
    def __init__(self, window):
        
        self.movespeed = 0.1

        self.window = window
        self.renderer = Engine()
        self.scene = Scene()

        self.lastTime = glfw.get_time()
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0

        self.walk_offset_lookup = {
            1: 0,
            2: 90,
            3: 45,
            4: 180,
            6: 135,
            7: 90,
            8: 270,
            9: 315,
            11: 0,
            12: 225,
            13: 270,
            14: 180
        }
        
        self.mainLoop()

    

    #Run the Engine
    def mainLoop(self):
        running = True
        while (running):
            #check events
            
            if glfw.window_should_close(self.window) \
                or glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:

                running = False
            
            self.handleKeys()
            self.handleMouse()
            
            glfw.poll_events()

            self.scene.update(self.frameTime / 16.7)

            self.renderer.render(self.scene)

            #timing
            self.calculateFramerate()
        self.quit()

    def handleKeys(self):

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
        combo = 0
        directionModifier = 0

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 1
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 2
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 4
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 8
        
        if combo in self.walk_offset_lookup:
            directionModifier = self.walk_offset_lookup[combo]
            dPos = [
                self.movespeed * self.frameTime / 16.7 * np.cos(np.deg2rad(self.scene.player.theta + directionModifier)),
                self.movespeed * self.frameTime / 16.7 * np.sin(np.deg2rad(self.scene.player.theta + directionModifier)),
                0
            ]
            self.scene.move_player(dPos)

    def handleMouse(self):

        (x,y) = glfw.get_cursor_pos(self.window)
        rate = self.frameTime / 16.7
        theta_increment = rate * ((SCREEN_WIDTH/2) - x)
        phi_increment = rate * ((SCREEN_HEIGHT/2) - y)
        self.scene.spin_player(theta_increment, phi_increment)
        glfw.set_cursor_pos(self.window, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def calculateFramerate(self):

        self.currentTime = glfw.get_time()
        delta = self.currentTime - self.lastTime
        if (delta >= 1):
            framerate = max(1, int(self.numFrames / delta))
            glfw.set_window_title(self.window, f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.numFrames = -1
            self.frameTime = float(1000.0/max(1,framerate))
        self.numFrames += 1

    def quit(self):
        self.renderer.quit()



#If set as Start-up File, Start Engine
if __name__ == '__main__':
    window = initialize_glfw()
    world = Program(window)