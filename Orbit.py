
import numpy as np

class Orbit:
    
    def __init__(self, nt, t, xyz, p, solution, classification):
        self.NT  = nt
        self.T   = t
        self.XYZ = np.reshape(xyz, (nt, 3))
        self.P   = np.reshape(p,   (nt, 3))
        self.SOLUTION = np.reshape(solution, (nt, 6))

        self.classification = classification

        self.R   = np.sqrt(self.XYZ[:,0]**2 + self.XYZ[:,1]**2)
        self.Z   = self.XYZ[:,2]

    def getRZ(self):
        return self.R, self.Z

    def getTXYZ(self):
        T = self.getTime()
        X, Y, Z = self.getXYZ()

        return T, X, Y, Z

    def getXYZ(self):
        return self.XYZ[:,0], self.XYZ[:,1], self.XYZ[:,2]

    def getSolution(self):
        return self.SOLUTION
    
    def getTime(self):
        return self.T

    def getTransitTime(self):
        return self.T[-1]

