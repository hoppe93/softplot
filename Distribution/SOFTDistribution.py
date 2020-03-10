# Implementation of SOFT distribution function

from Distribution.PhaseSpaceDistribution import PhaseSpaceDistribution
from Distribution.SOFTMomentumDistribution import SOFTMomentumDistribution
import h5py
import numpy as np


class SOFTDistribution(PhaseSpaceDistribution):
    
    def __init__(self, filename=None):
        super().__init__()

        self.MAGIC = 'distribution/soft'

        if filename != None:
            self.load(filename)


    def load(self, filename, path=''):
        """
        Load the SOFT distribution function from the
        file named 'filename'.

        filename: Name of file to load distribution function from.
        path:     Path in file to load distribution from (for
                    HDF5: group to load distribution from
                    MAT:  struct to load distribution from)
        """
        def tos(v):
            if v.dtype == 'O':
                return v[:][0]
            elif v.dtype == 'uint16':
                return v[:].tostring().decode('utf-16')
            else:
                return v[:].tostring().decode('utf-8')

        with h5py.File(filename, 'r') as f:
            if 'type' in f:
                dtype = tos(f['type'][:])

                if dtype != self.MAGIC:
                    raise Exception("The given file is not a SOFT distribution function.")

            r  = f[path+'/r'][:]
            nr = r.size

            self.r = r
            self.maxp = 0
            self.nr = nr

            for i in range(0, nr):
                mdf = SOFTMomentumDistribution()
                mdf._load_internal(f, 'r{}'.format(i))

                if mdf.getMaxP() > self.maxp:
                    self.maxp = mdf.getMaxP()

                self.insertMomentumDistribution(r[i], mdf)

            if self.maxp == 0:
                self.maxp = None


    def save(self, filename):
        """
        Save this SOFT distribution function to the
        named file.

        filename: Name of file to save distribution function to.
        """
        tos = lambda v : np.array(list(v), dtype='S1')

        with h5py.File(filename, 'w') as f:
            ddesc = tos(self.desc)
            dtype = tos(self.MAGIC)

            r = np.array(self._radii)
            f.create_dataset('r', r.shape, data=r)
            f.create_dataset('desc', ddesc.shape, dtype="S1", data=ddesc)
            f.create_dataset('type', dtype.shape, dtype="S1", data=dtype)

            for i in range(0, r.size):
                gname = 'r{}'.format(i)
                f.create_group(gname)

                self._distributions[i]._save_internal(f[gname])


