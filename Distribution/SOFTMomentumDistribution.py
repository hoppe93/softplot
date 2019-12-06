# SOFT momentum-space distribution function.
# This class is primarily designed to work together with the
# SOFTDistribution class, and _NOT_ be used separately.

from Distribution.MomentumSpaceDistribution import MomentumSpaceDistribution
import h5py
import numpy as np
import numpy.matlib
import scipy.interpolate
import scipy.interpolate.dfitpack


class SOFTMomentumDistribution(MomentumSpaceDistribution):
    
    def __init__(self, f=None, p=None, xi=None):
        super().__init__()

        self._f  = None
        self._p  = None
        self._xi = None
        self._averageF = None
        self._current = None

        if f is not None or p is not None or xi is not None:
            if f is None or p is None or xi is None:
                raise ValueError("Both the distribution function and grid must given at the same time to the constructor.")
            else:
                self.setVariables(f, p, xi)


    def _load_internal(self, f, path=''):
        """
        Load the SOFT momentum space distribution function
        pointed to by the h5py file handle 'f'.
        """
        df = f[path+'/f'][:]
        p  = f[path+'/p'][:]
        xi = f[path+'/xi'][:]

        self.setVariables(df, p, xi)


    def _save_internal(self, f):
        """
        Save this SOFT momentum space distribution function
        using the given h5py file handle.
        """
        if len(self._xi.shape) != 1 or len(self._p.shape) != 1:
            ValueError("The grid variables 'xi' and 'p' must be vectors.")
        if self._f.shape != (self._xi.size, self._p.size):
            raise ValueError("The distribution function 'f' must have dimensions (nxi, np).")

        f.create_dataset('f', self._f.shape, data=self._f)
        f.create_dataset('p', self._p.shape, data=self._p)
        f.create_dataset('xi', self._xi.shape, data=self._xi)


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
        if P is None and XI is None:
            P, XI = np.meshgrid(self._p, self._xi)
        elif P is None:
            P, XI = np.meshgrid(self._p, XI)
        elif XI is None:
            P, XI = np.meshgrid(P, self._xi)

        # This code is required since we expect 'P' and 'XI'
        # to be meshgrids, while scipy does not naturally allow this
        F = (scipy.interpolate.dfitpack.bispeu(self._interpf.tck[0], self._interpf.tck[1], 
            self._interpf.tck[2], self._interpf.tck[3], self._interpf.tck[4],
            P.ravel(), XI.ravel())[0]).reshape(P.shape)
            
        return P, XI, F


    def getAngleAveragedDistribution(self, r, p=None):
        """
        Returns the angle-averaged momentum distribution f(p).
        """
        if p is None:
            return self._p, self._averageF
        else:
            return p, np.interp(p, self._p, self._averageF)


    def getCurrentDensity(self, r, p=None):
        """
        Returns the current density of the distribution function.
        This is the e*vpar moment of f.
        """
        c = 299792458.0
        e = 1.602e-19

        if p is None:
            return self._p, self._current
        else:
            return p, np.interp(p, self._p, self._current)


    def getMomentum(self):
        """
        Returns the 'default' momentum grid.
        """
        return self._p


    def getNmomentum(self):
        """
        Returns the number of points in the 'default'
        momentum grid.
        """
        return self._p.size


    def setVariables(self, f, p, xi):
        """
        Sets the distribution function and grid parameters
        in a way that keeps the distribution function consistent.
        """
        if len(xi.shape) != 1 or len(p.shape) != 1:
            ValueError("The grid variables 'xi' and 'p' must be vectors.")
        if f.shape != (xi.size, p.size):
            raise ValueError("The distribution function 'f' must have dimensions (nxi, np).")

        self._f  = f
        self._p  = p
        self._xi = xi

        self.maxp = np.amax(p)

        dxi        = np.zeros((self._xi.size, 1))
        dxi[:-1,0] = np.diff(self._xi)
        dxi[-1,0]  = dxi[0]

        P, XI  = np.meshgrid(p, xi)
        DXI = np.matlib.repmat(dxi, 1, self._p.size)

        c = 299792458.0
        e = 1.602e-19

        eV = e * P / np.sqrt(P**2 + 1)

        # Angle-averaged distribution function
        self._averageF = np.sum(self._f * DXI, axis=0)
        # Current density
        self._current = np.sum(self._f * eV*XI * DXI, axis=0)

        self._interpf = scipy.interpolate.interp2d(p, xi, f, kind='linear', copy=False)


