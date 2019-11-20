# GO+CODE distribution function

import h5py
from Distribution.CODEDistribution import CODEDistribution
from Distribution.PhaseSpaceDistribution import PhaseSpaceDistribution


class GOCODEDistribution(PhaseSpaceDistribution):
    
    def __init__(self, filename=None):
        super().__init__()

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
        it = timestep
        with h5py.File(filename, 'r') as f:
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


