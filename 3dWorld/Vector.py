import math

class Vector3d:

    #**********Constructor**********#
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    #**********Overloading**********#

    #Addition
    def __add__(self, other):
        return Vector3d(self.x+other.x, self.y+other.y, self.z+other.z)

    #Self-Addition
    def __iadd__(self, other):
        return Vector3d(self.x+other.x, self.y+other.y, self.z+other.z)

    #Subtraction
    def __sub__(self, other):
        return Vector3d(self.x-other.x, self.y-other.y, self.z-other.z)

    #Self-Subtraction
    def __isub__(self, other):
        return Vector3d(self.x-other.x, self.y-other.y, self.z-other.z)

    #Scalar Multiplication
    def __mul__(self, b:float):
        return Vector3d(self.x*b, self.y*b, self.z*b)

    #Self-Scalar Multiplication
    def __imul__(self, other:float):
        return Vector3d(self.x*b, self.y*b, self.z*b)

    #Dot Product
    def __mul__(self, other):
        return Vector3d(self.x*other.x)+(self.y*other.y)+(self.z*other.z)

    #Self-Dot Product
    def __imul__(self, other):
        return Vector3d(self.x*other.x)+(self.y*other.y)+(self.z*other.z)

    #Scalar Division
    def __div__(self, b:float):
        return Vector3d(self.x/b, self.y/b, self.z/b)

    #Self-Scalar Division
    def __idiv__(self, b:float):
        return Vector3d(self.x/b, self.y/b, self.z/b)

     #**********Methods**********#

    #Get the Unit Vector of the Vector
    def unit(self):
        return self /self.mag()

    #Get the Magnitude of the Vector
    def mag(self):
        return math.sqrt(self.x+self.y+self.z)

    #Convert Vector3d to List
    def toList(self):
        return [self.x, self.y, self.z]

    #Convert Vector3d to Tuple
    def toTuple(self):
        return (self.x, self.y, self.z)

    #RotateX
    def RotX(self, x:float):
        return Vector3d(self.x, self.y*math.cos(x)-self.z*math.sin(x), self.y*math.sin(x)+self.z*math.cos(x))

    #RotateY
    def RotY(self, x:float):
        return Vector3d(self.x*math.cos(x)+self.z*math.sin(x), self.y, -self.x*math.sin(x)+self.z*math.cos(x))

    #RotateZ
    def RotZ(self, x:float):
        return Vector3d(self.x*math.cos(x)-self.y*math.sin(x), self.x*math.sin(x)+self.y*math.cos(x), self.z)