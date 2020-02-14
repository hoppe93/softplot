# Implementation of a CODE distribution function

import h5py
import numpy as np
import scipy.interpolate
import scipy.optimize

from Distribution.MomentumSpaceDistribution import MomentumSpaceDistribution


class CODEDistribution(MomentumSpaceDistribution):
    
    def __init__(self, filename=None, f=None, p=None, TRef=1, nRef=1, delta=1):
        """
        Initialize this CODE distribution function object.

        filename: Name of file to load distribution function from.
        """
        super().__init__()

        self._codef   = None
        self._codeP   = None
        self._codeNp  = 0
        self._codeNxi = 0
        self._codeInterpf = None

        self._delta = None
        self._TRef = None
        self._nRef = None

        if filename is not None:
            self.load(filename)
        elif (f is not None) and (p is not None):
            self._delta = delta
            self._TRef = TRef
            self._nRef = nRef
            self._setf_internal(f, p)
        

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
        This is the e*vpar moment of f, corresponding to the first
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


    def getMomentum(self):
        """
        Returns the 'default' momentum grid.
        """
        return self._codeP


    def getNormalizationFactor(self):
        me = 9.10938356e-31
        eV2K = 1.602e-19
        norm_div = 2*np.pi*me*(eV2K*self._TRef)
        fac = self._nRef / (np.sqrt(norm_div) * norm_div)

        return fac


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
        codef   = f[path+'/f'][:]
        Nxi = int(f[path+'/Nxi'][:])

        def formatScalar(s):
            if type(s) is not float:
                if len(s.shape) == 2:
                    return s[0][0]
                else:
                    return s[0]
            else:
                return s

        y     = f[path+'/y'][:]
        self._delta = formatScalar(f[path+'/delta'][:])
        self._TRef  = formatScalar(f[path+'/TRef'][:])
        self._nRef  = formatScalar(f[path+'/nRef'][:])

        if len(y.shape) == 2:
            y = y[:,0]

        p = y*self._delta
        codef = codef * self.getNormalizationFactor()
        codef = np.reshape(codef, (Nxi, p.size))

        self._setf_internal(codef, p)


    def _setf_internal(self, f, p):
        """
        Sets the distribution function and momentum grid.
        """
        self._codef = f
        self._codeP = p
        self._codeNp = p.size
        self._codeNxi = f.shape[0]

        self._codeInterpf = scipy.interpolate.interp1d(self._codeP, self._codef, bounds_error=False, fill_value=(0.0, 0.0))

        self.nr   = 1
        self.nmom = self._codeNp
        self.maxp = np.amax(self._codeP)
        self.r    = [0.0]


    def extrapolatePitch(self, nL=None, Lcutoff=None):
        """
        Extrapolate the distribution function in pitch angle, by adding
        more Legendre modes. It is assumed that the pitch angle distribution
        at a given momentum p takes the form

          f(p_0, xi) = f_0 + C*exp(A*xi)
        
        and that f_0 decays faster than exp(A*xi) as xi decreases. The
        exponential function is then Legendre decomposed according to

          exp(A*xi) = \sum_{n=0}^\infty (2n + 1) [\sqrt{\pi/2A} I_{n+1/2}(A)] P_n(xi),
        
        where I_{n+1/2}(z) is the modified Bessel function of the
        first kind, and P_n(x) is the n'th Legendre polynomial.

        PARAMETERS
        nL:      Number of Legendre modes in the extrapolated distribution
                 function. (Default: twice as many modes as in the original
                 distribution function).
        Lcutoff: Last Legendre mode number to use for fitting the
                 extrapolation parameters. This mode should be sufficiently
                 well-resolved to still attain a physical value, while
                 sufficiently large that f(p_0, xi) is dominated by the
                 exponential function. (Default: next-to-last Legendre mode)
        """
        nP   = self._codeNp
        nXi  = self._codeNxi

        if nL is None:
            nL = nXi * 2
        if Lcutoff is None:
            Lcutoff = nXi-2

        newf = np.zeros((nL, nP))

        if Lcutoff > nXi:
            raise Exception("Invalid cut-off mode number 'Lcutoff'.")

        # Copy original Legendre coefficients
        newf[0:Lcutoff,:] = self._codef[0:Lcutoff,:] / self.getNormalizationFactor()

        # TODO We always evaluate Bessel functions of the same order
        # (i.e. always of orders Lc-1 and Lc), so we could build a
        # lookup table first and instead interpolate in that table
        def f(A, y):
            ff  = (2*Lcutoff + 1) / (2*Lcutoff - 1)
            In1 = scipy.special.iv(Lcutoff-0.5, A)
            I   = scipy.special.iv(Lcutoff+0.5, A)

            return (y - ff*(I / In1))
        
        # Derivative...
        def fprime(A, y):
            In3 = scipy.special.iv(Lcutoff-1.5, A)
            In1 = scipy.special.iv(Lcutoff-0.5, A)
            Ip1 = scipy.special.iv(Lcutoff+0.5, A)
            Ip3 = scipy.special.iv(Lcutoff+1.5, A)

            ff = (2*Lcutoff+1)/((2*Lcutoff-1) * 2 * In1)
            T1 = (Ip1/In1) * (In3 + Ip1)
            T2 = (In1 + Ip3)

            return ff * (T1 - T2)

        # At each energy, fit the extrapolation parameters A & C
        A0 = 400
        for i in range(0, nP):
            y0 = newf[Lcutoff,i]
            y1 = newf[Lcutoff-1,i]
            y  = y0 / y1

            #A, info, ler, msg = scipy.optimize.fsolve(f, A0, args=(y,), fprime=fprime, full_output=True)
            A, info, ler, msg = scipy.optimize.fsolve(f, A0, args=(y,), fprime=fprime, full_output=True)
            fac  = np.sqrt(np.pi / (2*A))
            C    = y1 / ((2*Lcutoff-1) * fac * scipy.special.iv(Lcutoff-0.5, A))

            # Evaluate the Legendre coefficients
            for n in range(Lcutoff, nL):
                newf[n,i] = C * (2*n + 1) * fac * scipy.special.iv(n+0.5, A)

        return CODEDistribution(f=newf, p=self._codeP, TRef=self._TRef, nRef=self._nRef, delta=self._delta)

    
    def save(self, filename):
        """
        Save this CODE distribution function to the file
        with the given name.
        """
        with h5py.File(filename, 'w') as f:
            self._save_internal(f)


    def _save_internal(self, f):
        """
        Save this CODE distribution function using the
        given HDF5 file handle 'f'.
        """
        wf = self._codef / self.getNormalizationFactor()
        Nxi = wf.shape[0]
        Np  = wf.shape[1]

        wf = np.reshape(wf, (Nxi*Np))

        f.create_dataset('f', wf.shape, data=wf)
        f.create_dataset('Nxi', (1,), data=Nxi)
        f.create_dataset('y', self._codeP.shape, data=self._codeP / self._delta)
        f.create_dataset('TRef', (1,), data=self._TRef)
        f.create_dataset('nRef', (1,), data=self._nRef)
        f.create_dataset('delta', (1,), data=self._delta)


