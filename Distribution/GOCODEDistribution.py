# GO+CODE distribution function

import numpy as np
import h5py
from Distribution.CODEDistribution import CODEDistribution
from Distribution.PhaseSpaceDistribution import PhaseSpaceDistribution


class GOCODEDistribution(PhaseSpaceDistribution):
    
    def __init__(self, filename=None):
        super().__init__()

        self.MAGIC = 'distribution/gocode'

        if filename is not None:
            self.load(filename)


    def load(self, filename, path='', timestep=-1):
        """
        Load the GO+CODE distribution function from the
        file named 'filename'.

        filename: Name of file to load distribution function from.
        path:     Path in HDF5 file where data is stored.
        timestep: Time step to load distribution for.
        """
        def tos(v):
            if v.dtype == 'O':
                return v[:][0]
            else:
                return v[:].tostring().decode('utf-8')

        it = timestep
        with h5py.File(filename, 'r') as f:
            if 'type' in f:
                dtype = tos(f['type'][:])

                if dtype != self.MAGIC:
                    raise Exception("The given file is not a GO+CODE distribution function.")

            nt = int(f[path+'/nt'][:][0])

            if it < 0:
                it = nt+it

            if it < 0 or it >= nt:
                raise IndexError("Time step index out-of-range: {}. Number of time steps: {}".format(it, nt))
            
            r = f[path+'/r'][:]
            self._loadDist(f['/t{}'.format(it)], r)

        
    def _loadDist(self, f, r):
        """
        Internal routine for loading a GO+CODE distribution
        function struct from the given h5py file handle.

        f: h5py file handle to use for loading. Must represent
           the Group object to read from.
        r: Radial grid on which the GO+CODE distribution is defined.
        """
        nr        = r.size
        self.nr   = nr
        if len(r.shape) == 1:
            self.r = r
        else:
            self.r    = r[:,0]
        self.maxp = 0
        for i in range(0, nr):
            dist = CODEDistribution()
            dist._load_internal(f, 'r{}'.format(i))

            if dist.getMaxP() > self.maxp:
                self.maxp = dist.getMaxP()

            self.insertMomentumDistribution(r[i], dist)

        if self.maxp == 0:
            self.maxp = None

    
    def extrapolatePitch(self, nL=None, Lcutoff=None):
        """
        Extrapolate Legendre modes of the CODE distribution functions.
        See the implementation in 'CODEDistribution' for more details.
        Returns a new, extrapolated GO+CODE distribution function.
        """
        nr = self.nr
        newd = GOCODEDistribution()

        for ir in range(0, nr):
            dist = self.getMomentumDistribution(ir)
            newd.insertMomentumDistribution(self.r[ir], dist.extrapolatePitch(nL, Lcutoff))

        return newd

    
    def save(self, filename):
        """
        Save this GO+CODE distribution function to the HDF5
        file with the given name.
        """
        with h5py.File(filename, 'w') as f:
            self._save_internal(f)


    def _save_internal(self, f):
        """
        Save this GO+CODE distribution function using the
        given HDF5 file handle 'f'.

        f: HDF5 file handle to use for writing the distribution
           function to a file.
        """
        f.create_dataset('nt', (1,), data=1)
        f.create_dataset('r', (len(self._radii),), data=self._radii)
        l = len(self.MAGIC)
        tset = f.create_dataset('type', (1,), dtype='S'+str(l))
        tset[0:l] = np.string_(self.MAGIC)

        tg = f.create_group('t0')
        for i in range(0, len(self._radii)):
            g = tg.create_group('r{}'.format(i))
            dist = self.getMomentumDistribution(i)

            dist._save_internal(g)


