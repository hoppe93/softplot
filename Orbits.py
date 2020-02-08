
import h5py
import numpy as np
from Orbit import Orbit

class Orbits:
    
    def __init__(self, filename=None):
        self.NORBITS  = 0
        self.NT       = 0
        self.ORBITS   = []
        self.P        = None
        self.P2       = None
        self.PPAR     = None
        self.PPERP    = None
        self.SOLUTION = None
        self.T        = None
        self.R        = None
        self.XYZ      = None
        self.Z        = None
        self.CLASSIFICATION = None

        self.B = None
        self.BABS = None
        self.BHAT = None
        self.WALL = None
        self.SEPARATRIX = None
        
        self._radius     = None
        self._param1     = None
        self._param2     = None
        self._param1name = None
        self._param2name = None

        self.CLASS_UNKNOWN    = 0
        self.CLASS_COLLIDED   = 1
        self.CLASS_STAGNATION = 2
        self.CLASS_PASSING    = 3
        self.CLASS_TRAPPED    = 4
        self.CLASS_DISCARDED  = 5

        if filename is not None:
            self.load(filename)

    def load(self, filename):
        # Convert array to string (MAT-files store strings as
        # arrays with 2 bytes per character)
        if filename.endswith('.mat'):
            tos = lambda v : "".join(map(chr, v[:,:][:,0].tolist()))
        else:
            tos = lambda v : v[:].tostring().decode('utf-8')

        with h5py.File(filename, 'r') as f:
            self.T        = f['t'][:,:]
            self.NORBITS  = self.T.shape[0]
            self.NT       = self.T.shape[1]

            self.P        = f['p'][:,:]
            self.P2       = f['p2'][:,:]
            self.SOLUTION = f['solution'][:,:]
            self.XYZ      = f['x'][:,:]
            self.PPAR     = f['ppar'][:]
            self.PPERP    = f['pperp'][:]

            self.B        = f['B'][:]
            self.BABS     = f['Babs'][:]
            self.BHAT     = f['bhat'][:]

            self.CLASSIFICATION = f['classification'][:]

            try: self.WALL     = f['wall'][:]
            except: self.WALL  = None

            try: self.SEPARATRIX    = f['separatrix'][:]
            except: self.SEPARATRIX = None

            try:
                self._radius     = f['r'][:]
                self._param1name = tos(f['param1name'][:])
                self._param2name = tos(f['param2name'][:])
                self._param1     = f['param1'][:]
                self._param2     = f['param2'][:]

                self._nr = self._radius.size
                self._n1 = self._param1.size
                self._n2 = self._param2.size
            except:
                # Grid parameters not found...
                self._r = None
                self._param1name = None
                self._param2name = None
                self._param1 = None
                self._param2 = None


        for i in range(0, self.NORBITS):
            if self.CLASSIFICATION[i] != self.CLASS_DISCARDED:
                self.ORBITS.append(Orbit(self.NT, self.T[i,:], self.XYZ[i,:], self.P[i,:], self.SOLUTION[i,:], self.PPAR[i,:], self.PPERP[i,:], self.P2[i,:], self.B[i,:], self.BABS[i,:], self.BHAT[i,:], self.CLASSIFICATION[i], wall=self.WALL))
            else:
                self.ORBITS.append(None)

    def orbits(self):
        return self.ORBITS
        
    def __getitem__(self, oindex):
        return self.getOrbitByIndex(oindex=oindex)

    def getOrbitByIndex(self, oindex=0):
        if oindex >= self.NORBITS:
            raise IndexError('Requested orbit index is >= number of orbits')

        #self.ORBITS.append(Orbit(self.NT, self.T[i,:], self.XYZ[i,:], self.P[i,:], self.SOLUTION[i,:], self.P2[i,:], self.B[i,:], self.BABS[i,:], self.BHAT[i,:], self.CLASSIFICATION[i]))
        #return Orbit(self.NT, self.T[oindex,:], self.XYZ[oindex,:], self.P[oindex,:], self.SOLUTION[oindex,:], self.CLASSIFICATION[oindex])
        return self.ORBITS[oindex]

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

