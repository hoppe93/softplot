# Implementation of a CODE distribution function

import h5py
import numpy as np
import scipy.interpolate

from Distribution.MomentumSpaceDistribution import MomentumSpaceDistribution


class CODEDistribution(MomentumSpaceDistribution):
    
    def __init__(self, filename=None, nleg=100):
        """
        Initialize this CODE distribution function object.

        filename: Name of file to load distribution function from.
        nleg:     Number of Legendre modes to use when computing
                  the distribution function.
        """
        super().__init__()

        self._nleg = nleg

        self._codef   = None
        self._codeP   = None
        self._codeNp  = 0
        self._codeNxi = 0
        self._codeInterpf = None

        if filename is not None:
            self.load(filename)
        

    def _evalCODEf(self, codef, xi):
        """
        Build Legendre polynomials to use when evaluating
        the distribution function.
        """
        return np.polynomial.legendre.legval(xi, codef, tensor=False)


    def eval_mom(self, P, XI):
        """
        Evaluate the distribution function at the given radius,
        on the given P/XI grid.

        r:  Radius at which to evaluate the distribution function.
        P:  Momentum grid on which to evaluate the distribution
            (vector if XI=None, otherwise meshgrid).
        XI: Pitch grid on which to evaluate the distribution function
            (vector if P=None, otherwise meshgrid).

        If P or XI is None, the corresponding default grid is used (i.e.
        the one on which the distribution function is defined).
        """
        nxi = 150
        if P is None and XI is None:
            P, XI = np.meshgrid(self._codeP, np.linspace(-1, 1, nxi))
        elif P is None:
            P, XI = np.meshgrid(self._codeP, XI)
        elif XI is None:
            P, XI = np.meshgrid(P, np.linspace(-1, 1, nxi))
            
        return P, XI, self._evalCODEf(self._codeInterpf(P), XI)


    def getAngleAveragedDistribution(self, r, p=None):
        """
        Returns the angle-averaged momentum distribution f(p).
        """
        fp = self._codef[0,:]
        
        if p is None:
            return self._codeP, fp
        else:
            return p, np.interp(p, self._codeP, fp)


    def getCurrentDensity(self, r, p=None):
        """
        Returns the current density of the distribution function.
        This is the vpar moment of f, corresponding to the first
        Legendre mode times p/sqrt(1+p^2).
        """
        fp = self._codef[1,:]
        c  = 299792458.0
        e  = 1.602e-19

        if p is None:
            v = e*c*self._codeP / np.sqrt(self._codeP**2 + 1)
            return self._codeP, fp*v
        else:
            v = e*c*p / np.sqrt(p**2 + 1)
            return p, np.interp(p, self._codeP, fp) * v


    def load(self, filename, path=''):
        """
        Load the CODE distribution function that is
        stored in the file with the given name.

        filename: Name of file to load CODE distribution
                  function from.
        """
        with h5py.File(filename, 'r') as f:
            self._load_internal(f, path)
    

    def _load_internal(self, f, path=''):
        """
        Load the CODE distribution function pointed to
        by the h5py file handle 'f'.
        """
        self._codef   = f[path+'/f'][:]
        self._codeNxi = int(f[path+'/Nxi'][:])

        y     = f[path+'/y'][:][:,0]
        delta = f[path+'/delta'][:][0]
        Tref  = f[path+'/Tref'][:][0][0]
        nref  = f[path+'/nref'][:][0][0]

        me = 9.10938356e-31
        self._codeP = y*delta
        self._codeNp    = y.size

        eV2K = 1.602e-19
        norm_div = 2*np.pi*me*(eV2K*Tref)
        self._codef = self._codef * nref / (np.sqrt(norm_div) * norm_div)

        self._codef = np.reshape(self._codef, (self._codeNxi, self._codeNp))
        self._codeInterpf = scipy.interpolate.interp1d(self._codeP, self._codef, bounds_error=False, fill_value=(0.0, 0.0))

        self.nr   = 1
        self.nmom = (self._nleg, self._codeNp)
        self.maxp = np.amax(self._codeP)
        self.r    = [0.0]


