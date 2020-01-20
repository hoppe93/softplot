
import h5py
import numpy as np
import scipy.interpolate
import SOFT
import tempfile
import os

class MagneticField:

    def __init__(self, filename):
        """
        Constructor.

        filename: Name of file containing SOFT magnetic field.
        """
        self.filename = filename

        self.wall = None
        self.separatrix = None

        self.Bphi = None
        self.Br = None
        self.Bz = None
        self.Psi = None
        self.r = None
        self.z = None

        self.description = None
        self.name = None
        self.maxis = None

        self.interpBphi = None
        self.interpBr = None
        self.interpBz = None

        self.verBr = None
        self.verBphi = None
        self.verBz = None

        self.meshR = None
        self.meshZ = None

        self.load(filename)

    
    def getPlasmaBoundaries(self):
        r0 = self.maxis[0]

        if self.separatrix is not None:
            sepR, _ = self.getSeparatrix()
            rmax = np.amax(sepR)
        else:
            wallR, _ = self.getWall()
            rmax = np.amax(wallR)
        
        return r0, rmax


    def load(self, filename):
        """
        Load the magnetic field file with the given name.
        Populates the members of this object.

        filename: Name of file to load.
        """
        self.filename = filename

        if filename.endswith('.mat'):
            self.loadHDF5(filename)
        elif filename.endswith('.h5') or filename.endswith('.hdf5'):
            self.loadHDF5(filename)
        elif filename.endswith('.sdt'):
            self.loadSDT(filename)
        else:
            raise Exception("Unrecognized file format: {0}.".format(filename))

        self.meshR, self.meshZ = np.meshgrid(self.r, self.z)

        self.interpBphi = scipy.interpolate.interp2d(x=self.r, y=self.z, z=self.Bphi, kind='cubic')
        self.interpBr   = scipy.interpolate.interp2d(x=self.r, y=self.z, z=self.Br, kind='cubic')
        self.interpBz   = scipy.interpolate.interp2d(x=self.r, y=self.z, z=self.Bz, kind='cubic')


    def loadHDF5(self, filename):
        # Convert array to string (MAT-files store strings as
        # arrays with 2 bytes per character)
        if filename.endswith('.mat'):
            tos = lambda v : "".join(map(chr, v[:,:][:,0].tolist()))
        else:
            def tos(v):
                if v.dtype == 'O':
                    return v[:][0]
                else:
                    return v[:].tostring().decode('utf-8')

        with h5py.File(filename, 'r') as f:
            self.Bphi       = np.array(f['Bphi'][:,:])
            self.Br         = np.array(f['Br'][:,:])
            self.Bz         = np.array(f['Bz'][:,:])
            self.r          = f['r'][:,:]
            self.z          = f['z'][:,:]

            self.description = tos(f['desc'])
            self.name        = tos(f['name'])
            self.maxis       = f['maxis'][:]

            if len(self.maxis.shape) != 1:
                if self.maxis.shape[0] == 1:
                    self.maxis = self.maxis[0,:]
                else:
                    self.maxis = self.maxis[:,0]

            try: self.verBphi       = np.array(f['verBphi'][:])
            except KeyError: pass
            try: self.verBr         = np.array(f['verBr'][:])
            except KeyError: pass
            try: self.verBz         = np.array(f['verBz'][:])
            except KeyError: pass

            try: self.Psi        = f['Psi'][:,:]
            except KeyError: pass
            try: self.wall       = f['wall'][:,:]
            except KeyError: pass
            try: self.separatrix = f['separatrix'][:,:]
            except KeyError: pass


    def loadSDT(self, filename):
        f = SDTReader.loadSDT(filename)

        self.Bphi = f['Bphi']
        self.Br   = f['Br']
        self.Bz   = f['Bz']
        self.r    = f['r']
        self.z    = f['z']

        self.description = f['desc']
        self.name        = f['name']

        self.maxis = f['maxis']

        try: self.verBphi = f['verBphi']
        except KeyError: pass
        try: self.verBr = f['verBr']
        except KeyError: pass
        try: self.verBz = f['verBz']
        except KeyError: pass

        try: self.Psi        = f['Psi']
        except KeyError: pass
        try: self.wall       = f['wall']
        except KeyError: pass
        try: self.separatrix = f['separatrix']
        except KeyError: pass
    

    def writeFile(self):
        """
        Sets the name and description to the given values and writes
        the new values to the magnetic field file.

        name:        Name of magnetic field.
        description: Description string of magnetic field.
        """
        if self.filename.endswith('.mat'):
            raise NotImplementedError('Magnetic field I/O has not been implemented for MAT-files yet.')

        if self.filename is None:
            raise ValueError("Magnetic field filename may not be 'None'.")

        # Write to temporary file first (in case something is
        # screwed up)
        tf = next(tempfile._get_candidate_names())+'.h5'
        try:
            with h5py.File(tf, 'w') as f:
                self.store(tf)
        except Exception as ex:
            os.remove(tf)
            raise ex

        os.remove(self.filename)
        os.rename(tf, self.filename)


    def store(self, f):
        """
        Stores this magnetic field in the given HDF5 file.
        """
        #if self.filename.endswith('.mat'):
        #    tos = lambda v : np.array([[np.uint16(ord(c)) for c in v]]).T
        #else:
        tos = lambda v : np.array(list(v), dtype='S1')
        #tos = lambda s : s
        
        dsBphi = f.create_dataset('Bphi', self.Bphi.shape, data=self.Bphi)
        dsBr   = f.create_dataset('Br', self.Br.shape, data=self.Br)
        dsBz   = f.create_dataset('Bz', self.Bz.shape, data=self.Bz)

        ddesc = tos(self.description)
        dname = tos(self.name)
        dsdesc = f.create_dataset('desc', ddesc.shape, dtype="S1", data=ddesc)
        dsname = f.create_dataset('name', dname.shape, dtype="S1", data=dname)

        dsmaxis = f.create_dataset('maxis', self.maxis.shape, data=self.maxis)
        dsr     = f.create_dataset('r', self.r.shape, data=self.r)
        dsz     = f.create_dataset('z', self.z.shape, data=self.z)

        if self.verBphi is not None:
            dsVerBp = f.create_dataset('verBphi', self.verBphi.shape, data=self.verBphi)
        if self.verBr is not None:
            dsVerBr = f.create_dataset('verBr', self.verBr.shape, data=self.verBr)
        if self.verBz is not None:
            dsVerBz = f.create_dataset('verBz', self.verBz.shape, data=self.verBz)

        if self.Psi is not None:
            dsPsi   = f.create_dataset('Psi', self.Psi.shape, data=self.Psi)
        if self.separatrix is not None:
            dssep   = f.create_dataset('separatrix', self.separatrix.shape, data=self.separatrix)
        if self.wall is not None:
            dswall  = f.create_dataset('wall', self.wall.shape, data=self.wall)
            

    def getSeparatrix(self):
        """
        Returns the magnetic field separatrix.
        """
        if self.separatrix is None:
            return [], []
        ni, nj = self.separatrix.shape

        if ni == 2:
            return self.separatrix[0,:], self.separatrix[1,:]
        elif nj == 2:
            return self.separatrix[:,0], self.separatrix[:,1]
        else:
            raise Exception('Invalid format of separatrix vector')


    def getWall(self):
        """
        Returns the R and Z wall contours associated with
        the magnetic field.
        """
        if self.wall is None:
            return [], []

        ni, nj = self.wall.shape

        if ni == 2:
            return self.wall[0,:], self.wall[1,:]
        elif nj == 2:
            return self.wall[:,0], self.wall[:,1]
        else:
            raise Exception('Invalid format of wall vector')

    
    def evaluateB(self, X):
        r = np.sqrt(X[0]**2 + X[1]**2)
        z = X[2]
        sinphi, cosphi = X[1]/r, X[0]/r

        bp = self.interpBphi(r, z)
        br = self.interpBr(r, z)
        bz = self.interpBz(r, z)

        bx = br*cosphi - bp*sinphi
        by = bp*cosphi + br*sinphi

        return np.array([bx, by, bz])


    def calculateFluxSurfaces(self):
        """
        Calculates 6 magnetic flux surface contours at
        15%, 30%, 45%, 60%, 75% and 90% of the minor radius.
        """
        # Find magnetic axis and plasma edge
        r0, rWall = self.getPlasmaBoundaries()

        # Set default surfaces
        rmin = r0 + 0.15 * (rWall-r0)
        rmax = r0 + 0.90 * (rWall-r0)
        nr   = 6

        # Loop over radii, generating and running pi files
        flux = {'R': [], 'Z': [], 'lengths': []}

        momentum = 2
        pitchangle = 0.2
        T, X, Y, Z = SOFT.runOrbit(minradius=rmin, maxradius=rmax, nradius=nr, momentum=momentum, pitchangle=pitchangle, meqfile=self.filename, drifts=False)

        flux['R'] = np.sqrt(X**2 + Y**2)
        flux['Z'] = Z
        flux['lengths'] = [T.shape[1]]*T.shape[0]
        
        return flux

