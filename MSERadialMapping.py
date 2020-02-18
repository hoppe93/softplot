# This class allows you to generate a radial mapping for
# the MSE(/polarimeter) system available at many tokamaks
# (in SOFT circles, famously, Alcator C-Mod and JET). The
# mapping connects flux surface radii to MSE lines-of-sight
# for a given magnetic equilibrium.

import numpy as np
import matplotlib.pyplot as plt
import h5py
from Green import Green
from LineOfSightGeometry import LineOfSightGeometry
from MagneticField import MagneticField
import SOFT
import os, tempfile


class MSERadialMapping:
    
    def __init__(self, meq, geometry):
        """
        Constructor.

        meq:      If a string, interprets this variable as a filename
                  and loads the corresponding file, which is assumed to
                  be a SOFT magnetic field.
        geometry: MSE line-of-sight geometry object.
        """

        if type(meq) != str:
            raise Exception("The provided magnetic field 'meq' is not a file name.")

        self.magneticfieldname = meq
        self.magneticfield = MagneticField(meq)

        if type(geometry) != LineOfSightGeometry:
            raise Exception("The provided line-of-sight geometry is not a LineOfSightGeometry object.")

        self.geometry      = geometry

        self.nradii = 400
        self.ntime  = 2000


    def constructMapping(self, verbose=False, qtSignal=None):
        """
        Executes SOFT and constructs the radial mapping.

        RETURNS
        r:             SOFT radial coordinates.
        sensitivities: Array containing the sensitivity of each
                       MSE chord as a function of SOFT radius (i.e.
                       flux surface).
        radiusmap:     Array mapping each MSE chord to a SOFT radius
                       (i.e. flux surface).
        """
        nc = self.geometry.nlos()
        radiusmap = np.zeros((nc,))
        sensitivities = np.zeros((nc, self.nradii))
        prevri = self.nradii
        flipped = False
        r = None

        for i in range(0, nc):
            pi, outfile = self.__generatePi(i, prefix='mse')

            if verbose:
                print('Running SOFT for line-of-sight {}/{}...'.format(i+1, nc))

            # Run SOFT
            SOFT.runSOFT(pi)

            # Read back output
            gf = Green(outfile)
            r = gf._r
            r -= np.amin(r)
            f = gf.FUNC

            fmax = np.amax(f)
            if fmax != 0:
                sensitivities[i] = f / fmax
            else:
                sensitivities[i] = f

            maxri = np.argmax(f)
            radiusmap[i] = r[maxri]

            # On the other side of the magnetic axis?
            if flipped or maxri > prevri:
                radiusmap[i] = -radiusmap[i]
            else:
                prevri = maxri

            os.remove(outfile)

            if qtSignal is not None:
                qtSignal.emit(i, r, sensitivities, radiusmap)

        self.r = r
        self.sensitivities = sensitivities
        self.radiusmap = radiusmap

        return r, sensitivities, radiusmap


    def __generatePi(self, index, prefix='mse'):
        """
        Generate a pi script for the line-of-sight with
        the given index.
        """
        outfile = next(tempfile._get_candidate_names())+'.h5'
        detdef, detname = self.geometry.generatePiDetectorDefinition(index, prefix=prefix)

        pi  = "magnetic_field = mf;\n"
        pi += "particle_generator = PGen;\n"
        pi += "particle_pusher = PPusher;\n"
        pi += "tools = rad;\n"
        pi += "include_drifts = no;\n"

        pi += detdef

        pi += "@MagneticField mf (numeric) {\n"
        pi += "    filename = \"{}\";\n".format(self.magneticfieldname)
        pi += "}\n"

        pi += "@ParticleGenerator PGen {\n"
        pi += "    a = 0, 1, {};\n".format(self.nradii)
        pi += "    p = 10, 10, 1;\n"
        pi += "    thetap = 0.2, 0.2, 1;\n"
        pi += "}\n"

        pi += "@ParticlePusher PPusher {\n"
        pi += "    equation = guiding-center;\n"
        pi += "    nt       = {};\n".format(self.ntime)
        pi += "    force_numerical_jacobian = yes;\n"
        pi += "}\n"

        pi += "@Radiation rad {\n"
        pi += "    detector = {};\n".format(detname)
        pi += "    ntoroidal = 7000;\n"
        pi += "    model = isotropic;\n"
        pi += "    output = green;\n"
        pi += "    torquad = trapz;\n"
        pi += "}\n"

        pi += "@RadiationModel isotropic (isotropic) {\n"
        pi += "    value = 1;\n"
        pi += "}\n"

        pi += "@RadiationOutput green (green) {\n"
        pi += "    format = r;\n"
        pi += "    output = \"{}\";\n".format(outfile)
        pi += "}\n"

        return pi, outfile


    def saveMapping(self, filename, includeMagneticField=False):
        """
        Saves the radial mapping to a file.

        filename:             Name of file to save map to.
        includeMagneticField: If True, also stores a copy of
                              the magnetic field used in the file.
        """
        with h5py.File(filename, 'w') as f:
            f.create_dataset('rmap', self.radiusmap.shape, data=self.radiusmap)
            self.magneticfield.store(f)


    def visualize(self):
        """
        Visualize the computed radial sensitivities
        """
        plt.figure(figsize=(8,3))

        nc = self.geometry.nlos()
        for i in range(0, nc):
            sen = self.sensitivities[i,:]
            if np.sum(sen) == 0: continue

            plt.plot(self.r, sen/np.amax(sen), linewidth=2)

        plt.xlim([0, np.amax(self.r)])
        plt.ylim([0, 1.25])
        plt.xlabel('Minor radius (m)')
        plt.ylabel('Normalized intensity')
        plt.gca().get_yaxis().set_ticks([])

        plt.tight_layout()
        plt.show()
        

