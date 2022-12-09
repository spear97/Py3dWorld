from Cube import Cube
from Player import Player
import numpy as np

class Scene:

    def __init__(self):

        self.cubes = [
            Cube(
                position = [6,0,0],
                eulers = [0,0,0]
            )
        ]

        self.player = Player(position = [0,0,2])
    
    def update(self, rate):

        for cube in self.cubes:
            cube.eulers[1] += 0.25 * rate
            if cube.eulers[1] > 360:
                cube.eulers[1] -= 360
    
    def move_player(self, dPos):

        dPos = np.array(dPos, dtype = np.float32)
        self.player.position += dPos
    
    def spin_player(self, dTheta, dPhi):

        self.player.theta += dTheta
        if self.player.theta > 360:
            self.player.theta -= 360
        elif self.player.theta < 0:
            self.player.theta += 360
        
        self.player.phi = min(
            89, max(-89, self.player.phi + dPhi)
        )

        self.player.update_vectors()

