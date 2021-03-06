# Specification of line-of-sight geometry (for, for example,
# MSE systems).

import numpy as np
import h5py


class LineOfSightGeometry:
    
    def __init__(self, filename=None, position=None, nhat=None, alpha=None, aperture=None, spectrum=None):
        """
        Constructor.

        filename: Name of file to load geometry from.

          OR

        position: Position of origin of lines-of-sight (where all LoS
                  intersect).
        nhat:     List of line-of-sight vectors/viewing directions.
        alpha:    Line-of-sight (half) opening angle (same for every LoS).
        aperture: Line-of-sight aperture size.
        spectrum: Tuple specifying the LoS spectral range and resolution
                  (when running SOFT). Syntax: (lambdaMin, lambdaMax, nLambda)
        """
        if filename is not None:
            self.load(filename)
        else:
            if position is None or nhat is None or alpha is None or aperture is None or spectrum is None:
                raise Exception("All of 'position', 'nhat', 'alpha', 'aperture' or 'spectrum' must be specified.")

            self.position = position
            self.nhat     = nhat
            self.alpha    = alpha
            self.aperture = aperture
            self.spectrum = spectrum

    
    def generatePiScript(self, filename=None, prefix="mse"):
        """
        Defines all lines-of-sight in this geometry using
        SOFT pi file syntax. If 'filename' is specified, the
        generated script is written to a file with the given
        name.

        filename: Name of file to save pi script to.
        prefix:   String to prefix all detector definition names with.
        """
        pi = ''
        for i in range(0, len(self.nhat)):
            pi += generatePiDetectorDefinition(i, prefix=prefix)

        if filename is not None:
            with open(filename, 'w') as f:
                f.write(pi)

        return pi


    def generatePiDetectorDefinition(self, index, prefix='mse'):
        """
        Generates a SOFT @Detector definition for the line-of-sight
        with the given index.

        index:  Index of line-of-sight to generate definition for.
        prefix: String to prefix all detector definition names with.
        """
        pos  = self.position
        nh   = self.nhat[index,:]

        detname = "{}_{:d}".format(prefix, index+1)
        pi  = "@Detector {} {{\n".format(detname)
        pi += "    position     = {:.8f}, {:.8f}, {:.8f};\n".format(pos[0], pos[1], pos[2])
        pi += "    direction    = {:.8f}, {:.8f}, {:.8f};\n".format(nh[0], nh[1], nh[2])
        pi += "    aperture     = {:.8f};\n".format(self.aperture)
        pi += "    spectrum     = {:.8e}, {:.8e}, {:d};\n".format(self.spectrum[0], self.spectrum[1], self.spectrum[2])
        pi += "    vision_angle = {:.8f};\n".format(self.alpha)
        pi += "}\n\n"

        return pi, detname


    def nlos(self):
        """
        Returns the number of lines-of-sight represented by this object.
        """
        return self.nhat.shape[0]


    def load(self, filename):
        """
        Load line-of-sight geometry from the specified file.

        filename: Name of (HDF5) file to load line-of-sight geometry from.
        """
        with h5py.File(filename, 'r') as f:
            self.position = f['position'][:]
            self.nhat = f['nhat'][:]
            self.alpha = f['alpha'][:][0]
            self.aperture = f['aperture'][:][0]
            self.spectrum = f['spectrum'][:]

            self.spectrum = (np.amin(self.spectrum), np.amax(self.spectrum), self.spectrum.size)


    def save(self, filename):
        """
        Save this line-of-sight geometry to the file with the given name.

        filename: Name of file to save line-of-sight geometry to.
        """
        with h5py.File(filename, 'w') as f:
            f.create_dataset('position', self.position.shape, data=self.position)
            f.create_dataset('nhat', self.nhat.shape, data=self.nhat)
            f.create_dataset('alpha', (1,), data=self.alpha)
            f.create_dataset('aperture', (1,), data=self.aperture)
            
            srange = np.linspace(self.spectrum[0], self.spectrum[1], self.spectrum[2])
            f.create_dataset('spectrum', srange.shape, data=srange)


