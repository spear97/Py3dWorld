from Parameters import Parameters
from Player import Player
from Light import Light
import numpy as np

#The 3d Environemtn where 3d Objects will be rendered
class Scene:

    #The Constructor for 3d Environments
    def __init__(self):

        #The Positions where 3d Objects will be Spawn with which Rotation
        self.instances = [
            Parameters(position = [6,0,0], rotation = [0,0,0], mesh_filename='Models/Cube.obj', img_filename='Images/Barbatos.png')
        ]

        #The Lights that will illuminate the Environment
        self.lights = [
            Light( position = [4, 0, 2], color = [1, 1, 1], strength=3)
        ]

        #The Player that will navigate the environment
        self.player = Player(position = [0,0,2])
    
    #Update all Objects that exist in the Environment
    def update(self, rate):

        '''
        #Rotate each object that exists in the environment
        for cube in self.cubes:

            #Calcualte the Objects Yaw Rotation-Rate
            cube.eulers[1] += 0.25 * rate

            #If Yaw exceed 360, then reset it back to 0
            if cube.eulers[1] > 360:
                cube.eulers[1] -= 360
        '''
        pass
    
    #Move the Player towards a given Vector Position in the Environment
    def move_player(self, dPos):

        dPos = np.array(dPos, dtype = np.float32)
        self.player.position += dPos
    
    #Rotate the Player at a given Horizontal (denoted by Theta) and Vertical (denoted by Phi) rate
    def spin_player(self, dTheta, dPhi):

        #Calucate player's theta value
        self.player.theta += dTheta

        #If player's theta exceed above 360, then decrement it by 360
        if self.player.theta > 360:
            self.player.theta -= 360

        #If player's theta exceed below 0, then increment by 360
        elif self.player.theta < 0:
            self.player.theta += 360
        
        #Cap how Player can look up and down
        self.player.phi = min(
            89, max(-89, self.player.phi + dPhi)
        )

        #Update the Up, Right, and Forward Vectors of the Player
        self.player.update_vectors()

