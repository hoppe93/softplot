
import h5py
import numpy as np
from Orbit import Orbit

class Orbits:
    
    def __init__(self, filename=None):
        self.NORBITS  = 0
        self.NT       = 0
        self.ORBITS   = []
        self.P        = None
        self.SOLUTION = None
        self.T        = None
        self.R        = None
        self.XYZ      = None
        self.Z        = None

        if filename is not None:
            self.load(filename)

    def load(self, filename):
        with h5py.File(filename) as f:
            self.T        = f['t'][:,:]
            self.NORBITS  = self.T.shape[0]
            self.NT       = self.T.shape[1]

            self.P        = f['p'][:,:]
            self.SOLUTION = f['solution'][:,:]
            self.XYZ      = f['x'][:,:]

        for i in range(0, self.NORBITS):
            self.ORBITS.append(Orbit(self.NT, self.T[i,:], self.XYZ[i,:], self.P[i,:], self.SOLUTION[i,:]))

    def orbits(self):
        return self.ORBITS
        
    def __getitem__(self, oindex):
        return self.getOrbitByIndex(oindex=oindex)

    def getOrbitByIndex(self, oindex=0):
        if oindex >= self.NORBITS:
            raise IndexError('Requested orbit index is >= number of orbits')

        return Orbit(self.NT, self.T[oindex,:], self.XYZ[oindex,:], self.P[oindex,:], self.SOLUTION[oindex,:])

    def getTXYZ(self):
        X, Y, Z = [], [], []
        for i in range(0, self.NORBITS):
            _, x, y, z = self.ORBITS[i].getTXYZ()
            X.append(x)
            Y.append(y)
            Z.append(z)

        return self.T, np.array(X), np.array(Y), np.array(Z)

    def getPoloidalOrbit(self, oindex=0):
        if oindex >= self.NORBITS:
            raise IndexError('Requested orbit index is >= number of orbits')

        xyz = np.reshape(self.XYZ[oindex,:], (self.NT, 3))

        R = np.sqrt(xyz[:,0]**2 + xyz[:,1]**2)
        Z = xyz[:,2]

        return R, Z

