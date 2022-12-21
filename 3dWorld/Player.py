import numpy as np

#Basically acts as the Eyes of the User for the 3d Environment
class Player:

    #Constructor
    def __init__(self, position):

        #The position that the Player will be Spawned at
        self.position = np.array(position, dtype = np.float32)

        #The Theta(Horizontal) Value of the Player, will be at 0 by default
        self.theta = 0

        #The Phi(Vertical) Value of the Player, will be at 0 by default
        self.phi = 0

        #Calculate the Up, Forward, and Right Vectors of the Player upon Construction
        self.update_vectors()
    
    #Calculate the Up, Forward, and Right Vectors
    def update_vectors(self):

        #Set and Intialize the forward vector of the Player
        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ]
        )

        #Set and Initialize the Global Up Location of the Player Character 
        globalUp = np.array([0,0,1], dtype = np.float32)

        #Calcuate the right Vector for the Player
        self.right = np.cross(self.forwards, globalUp)

        #Calucate the Up Vector for the Player
        self.up = np.cross(self.right, self.forwards)
