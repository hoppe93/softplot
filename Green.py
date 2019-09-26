"""
SOFT Green's function object
"""

import h5py
import numpy as np

class Green:
    
    def __init__(self, filename=None):
        """
        Constructor.

        filename: Name of file containing Green's function.
        """
        self._func        = None
        self._param1      = None
        self._param2      = None
        self._param1name  = None
        self._param2name  = None
        self._pixels      = None
        self._r           = None
        self._wavelengths = None

        self.n1 = 0
        self.n2 = 0
        self.ni = 0
        self.nj = 0
        self.nr = 0
        self.nw = 0

        self.format = None
        self.stokesparams = False

        self.GAMMA  = np.array([])
        self.P      = np.array([])
        self.XI     = np.array([])
        self.THETAP = np.array([])
        self.PPAR   = np.array([])
        self.PPERP  = np.array([])
        # Jacobian
        self.J      = 1

        if filename is not None:
            self.load(filename)


    def load(self, filename):
        """
        Load a Green's function from the given file.

        filename: Name of file to load.
        """
        # Convert array to string (MAT-files store strings as
        # arrays with 2 bytes per character)
        if filename.endswith('.mat'):
            tos = lambda v : "".join(map(chr, v[:,:][:,0].tolist()))
        else:
            tos = lambda v : v[:].tostring().decode('utf-8')

        with h5py.File(filename, 'r') as f:
            self._func        = f['func'][:]
            self._param1      = f['param1'][:]
            self._param2      = f['param2'][:]
            self._param1name  = tos(f['param1name'])
            self._param2name  = tos(f['param2name'])
            self._r           = f['r'][:]
            self.format       = tos(f['type'])
            self._wavelengths = f['wavelengths'][:]

            self.stokesparams = True if f['stokesparams'][0]==1 else False

            rowpixels, colpixels = 0, 0
            try:
                if len(f['rowpixels'][:].shape) == 1:
                    rowpixels = int(f['rowpixels'][:][0])
                    colpixels = int(f['colpixels'][:][0])
                else:
                    rowpixels = int(f['rowpixels'][:][0,0])
                    colpixels = int(f['colpixels'][:][0,0])
            except:
                rowpixels, colpixels = 0, 0

            self._pixels = (rowpixels, colpixels)

        self.n1 = self._param1.size
        self.n2 = self._param2.size
        self.ni = int(self._pixels[0])
        self.nj = int(self._pixels[1])
        self.nr = self._r.size
        self.nw = self._wavelengths.size

        # Reshape function
        dim = self.getDimensions()
        self.FUNC = np.reshape(self._func, dim)

        self._setupMomentumGrid()


    def getDimensions(self):
        """
        Returns a tuple with the dimensions of the
        Green's function.
        """
        dim = ()

        if self.stokesparams:
            dim = (4,)

        for c in self.format:
            if c == '1':   dim = dim + (self.n1,)
            elif c == '2': dim = dim + (self.n2,)
            elif c == 'i': dim = dim + (self.ni,)
            elif c == 'j': dim = dim + (self.nj,)
            elif c == 'r': dim = dim + (self.nr,)
            elif c == 'w': dim = dim + (self.nw,)
            else:
                raise Exception("Unrecognized format indicator of Green's function: '{0}'. Format: '{1}'.".format(c, self.format))

        return dim


    def getParameterName(self, designation):
        """
        The parameter 'designation' may be any of the valid
        function format specifiers, '1', '2', 'i', 'j', 'r' or 'w'.
        """

        if designation == '1':   return self._param1name
        elif designation == '2': return self._param2name
        elif designation == 'i': return 'i'
        elif designation == 'j': return 'j'
        elif designation == 'r': return 'r'
        elif designation == 'w': return 'w'
        else: raise Exception("Unrecognized format specifier: '{0}'.".format(designation))


    def getFormat(self): return self.format
    def getJacobian(self): return self.J

    def _setupMomentumGrid(self):
        """
        Initializes the momentum grid of this object, from
        the '_param1' and '_param2' properties, which come
        directly from the SOFT output file.
        """
        if self._param1name == 'gamma':
            if self._param2name == 'ppar': self._gammaPpar(self._param1, self._param2)
            elif self._param2name == 'thetap': self._gammaThetap(self._param1, self._param2)
            elif self._param2name == 'ithetap': self._gammaThetap(self._param1, self._param2)
            elif self._param2name == 'xi': self._gammaXi(self._param1, self._param2)
            else: raise Exception("Invalid combination of momentum-space parameters: '{0}' and '{1}'.".format(self._param1name, self._param2name))
        elif self._param1name == 'p':
            if self._param2name == 'ppar': self._pPpar(self._param1, self._param2)
            elif self._param2name == 'thetap': self._pThetap(self._param1, self._param2)
            elif self._param2name == 'ithetap': self._pThetap(self._param1, self._param2)
            elif self._param2name == 'xi': self._pXi(self._param1, self._param2)
            else: raise Exception("Invalid combination of momentum-space parameters: '{0}' and '{1}'.".format(self._param1name, self._param2name))
        elif self._param1name == 'ppar':
            if self._param2name == 'gamma': self._gammaPpar(self._param2, self._param1)
            elif self._param2name == 'p': self._pPpar(self._param2, self._param1)
            elif self._param2name == 'pperp': self._pparPperp(self._param1, self._param2)
            elif self._param2name == 'thetap': self._pparThetap(self._param1, self._param2)
            elif self._param2name == 'ithetap': self._pparThetap(self._param1, self._param2)
            elif self._param2name == 'xi': self._pparXi(self._param1, self._param2)
            else: raise Exception("Invalid combination of momentum-space parameters: '{0}' and '{1}'.".format(self._param1name, self._param2name))
        elif self._param1name == 'pperp':
            if self._param2name == 'ppar': self._pparPperp(self._param2, self._param1)
            elif self._param2name == 'thetap': self._pperpThetap(self._param1, self._param2)
            elif self._param2name == 'ithetap': self._pperpThetap(self._param1, self._param2)
            elif self._param2name == 'xi': self._pperpXi(self._param1, self._param2)
            else: raise Exception("Invalid combination of momentum-space parameters: '{0}' and '{1}'.".format(self._param1name, self._param2name))
        elif self._param1name == 'thetap' or self._param2name == 'ithetap':
            if self._param2name == 'gamma': self._gammaThetap(self._param2, self._param1)
            elif self._param2name == 'p': self._pThetap(self._param2, self._param1)
            elif self._param2name == 'ppar': self._pparThetap(self._param2, self._param1)
            elif self._param2name == 'pperp': self._pperpThetap(self._param2, self._param1)
            else: raise Exception("Invalid combination of momentum-space parameters: '{0}' and '{1}'.".format(self._param1name, self._param2name))
        elif self._param1name == 'xi':
            if self._param2name == 'gamma': self._gammaXi(self._param2, self._param1)
            elif self._param2name == 'p': self._pXi(self._param2, self._param1)
            elif self._param2name == 'ppar': self._pparXi(self._param2, self._param1)
            elif self._param2name == 'pperp': self._pperpXi(self._param2, self._param1)
            else: raise Exception("Invalid combination of momentum-space parameters: '{0}' and '{1}'.".format(self._param1name, self._param2name))
        else: raise Exception("Unrecognized momentum-space parameter: '{0}'.".format(self._param1name))


    def __getitem__(self, index):
        """
        Overload indexing operator ([])

        index: Index of element to select
        """
        return self.FUNC[index]

    ##############################################
    ##############################################
    ## MOMENTUM GRID SETUP ROUTINES             ##
    ##############################################
    ##############################################
    def _gammaPpar(self, gamma, ppar):
        self.GAMMA, self.PPAR = np.meshgrid(gamma, ppar)

        self.P = np.sqrt(self.GAMMA**2 - 1)
        self.PPERP = np.sqrt(self.P**2 - self.PPAR**2)
        self.XI = self.PPAR / self.P
        self.THETAP = np.arccos(self.XI)

        self.J = self.GAMMA

    def _gammaThetap(self, gamma, thetap):
        self.GAMMA, self.THETAP = np.meshgrid(gamma, thetap)

        self.P = np.sqrt(self.GAMMA**2 - 1)
        self.XI = np.cos(self.THETAP)
        self.PPAR = self.P * self.XI
        self.PPERP = self.P * np.sqrt(1 - self.XI**2)

        self.J = self.GAMMA*self.PPERP

    def _gammaXi(self, gamma, xi):
        self.GAMMA, self.XI = np.meshgrid(gamma, xi)

        self.P = np.sqrt(self.GAMMA**2 - 1)
        self.THETAP = np.arccos(self.XI)
        self.PPAR = self.P * self.XI
        self.PPERP = self.P * np.sqrt(1 - self.XI**2)

        self.J = self.GAMMA * self.P

    def _pPpar(self, p, ppar):
        self.P, self.PPAR = np.meshgrid(p, ppar)

        self.GAMMA = np.sqrt(self.P**2 + 1)
        self.PPERP = np.sqrt(self.P**2 - self.PPAR**2)
        self.XI = self.PPAR / self.P
        self.THETAP = np.arccos(self.XI)

        self.J = self.P

    def _pThetap(self, p, thetap):
        self.P, self.THETAP = np.meshgrid(p, thetap)

        self.GAMMA = np.sqrt(self.P**2 + 1)
        self.XI = np.cos(self.THETAP)
        self.PPAR = self.P * self.XI
        self.PPERP = self.P * np.sqrt(1 - self.XI**2)

        self.J = self.P * self.PPERP

    def _pXi(self, p, xi):
        self.P, self.XI = np.meshgrid(p, xi)

        self.GAMMA = np.sqrt(self.P**2 + 1)
        self.THETAP = np.arccos(self.XI)
        self.PPAR = self.P * self.XI
        self.PPERP = self.P * np.sqrt(1 - self.XI**2)

        self.J = self.P**2

    def _pparPperp(self, ppar, pperp):
        self.PPAR, self.PPERP = np.meshgrid(ppar, pperp)

        self.P = np.sqrt(self.PPAR**2 + self.PPERP**2)
        self.GAMMA = np.sqrt(self.P**2 + 1)
        self.XI = self.PPAR / self.P
        self.THETAP = np.arccos(self.XI)

        self.J = self.PPERP

    def _pparThetap(self, ppar, thetap):
        self.PPAR, self.THETAP = np.meshgrid(ppar, thetap)

        self.XI = self.cos(self.THETAP)
        self.P = self.PPAR / self.XI
        self.PPERP = np.sqrt(self.P**2 - self.PPAR**2)
        self.GAMMA = np.sqrt(self.P**2 + 1)

        self.J = self.P * self.PPERP / self.XI

    def _pparXi(self, ppar, xi):
        self.PPAR, self.XI = np.meshgrid(ppar, xi)

        self.THETAP = self.arccos(self.XI)
        self.P = self.PPAR / self.XI
        self.PPERP = np.sqrt(self.P**2 - self.PPAR**2)
        self.GAMMA = np.sqrt(self.P**2 + 1)

        self.J = self.P / self.XI

    def _pperpThetap(self, pperp, thetap):
        self.PPERP, self.THETAP = np.meshgrid(pperp, thetap)

        self.XI = self.cos(THETAP)
        self.P = self.PPERP / np.sqrt(1 - self.XI**2)
        self.PPAR = self.P * self.XI
        self.GAMMA = np.sqrt(self.P**2 + 1)

        self.J = self.P**2

    def _pperpXi(self, pperp, xi):
        self.PPERP, self.XI = np.meshgrid(pperp, xi)

        self.THETAP = np.arccos(self.XI)
        self.P = self.PPERP / np.sqrt(1 - self.XI**2)
        self.PPAR = self.P * self.XI
        self.GAMMA = np.sqrt(self.P**2 + 1)

        self.J = self.P**2 / np.sqrt(1 - self.XI**2)


