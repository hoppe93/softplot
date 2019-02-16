# SOFT MAGNETIC EQUILIBRIUM PLOT CLASS
#
# This class is a simple interface for plotting SOFT Magnetic Equilibria
# with overlays etc. using Python's matplotlib.
#

import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import scipy.interpolate
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
import matplotlib.ticker
import io, os
import subprocess

from MagneticField import MagneticField


class MeqPlot:

    def __init__(self, figure=None, canvas=None, registerGeriMap=True):
        # PROPERTIES
        self.canvas = canvas
        self.colormapName = 'GeriMap'
        self.figure = figure
        self.flux = None
        self.overlayWallCrossSection = False
        self.overlaySeparatrix = False
        self.overlayFluxSurfaces = False
        self.overlayMagneticAxis = False

        self.plotBr = False
        self.plotBphi = False
        self.plotBz = False

        self.rmin, self.rmax = 0, 0
        self.zmin, self.zmax = 0, 0

        # Internal properties
        self._fluxOverlayHandles = []
        self._magneticAxisHandle = None
        self._orbitHandles = []
        self._separatrixOverlayHandle = None
        self._wallCrossSectionOverlayHandle = None

        if self.figure is None:
            self.figure = plt.gca().figure
            if self.canvas is not None:
                raise ValueError("Canvas set, but no figure given. If no figure is given, no canvas may be given.")
        if self.canvas is None:
            self.canvas = self.figure.canvas

        self.axes = None

        self._meqfile = None

        if registerGeriMap:
            MeqPlot.registerGeriMap()

    ####################################################
    #
    # GETTERS
    #
    ####################################################
    def hasSeparatrix(self): return self.magneticfield.separatrix is not None
    def getPlasmaBoundaries(self):
        return self.magneticfield.getPlasmaBoundaries()

    ####################################################
    #
    # SETTERS
    #
    ####################################################
    def setFluxSurfaces(self, flux): self.flux = flux

    ####################################################
    #
    # PUBLIC METHODS
    #
    ####################################################
    def adjustAxes(self):
        self.axes.axis('equal')
        self.axes.set_xlim([0.9*self.rmin, 1.1*self.rmax])
        self.axes.set_ylim([1.1*self.zmin, 1.1*self.zmax])


    def assemblePlot(self):
        """
        Plot the magnetic equilibrium, applying all settings
        given to this MeqPlot object. This means any overlays
        will be plotted.
        """
        self.clearPlot()
        self.axes = self.figure.add_subplot(111)

        # Reset handles
        self._fluxOverlayHandles = []
        self._magneticAxisHandle = None
        self._orbitHandles = []
        self._separatrixOverlayHandle = None
        self._wallCrossSectionOverlayHandle = None

        # Plot image
        self.plotEq()

        # Plot overlays
        self.plotOverlays()

        self.adjustAxes()

    def calculateFluxSurfaces(self):
        self.flux = self.magneticfield.calculateFluxSurfaces()

    def evaluateB(self, r, z):
        Bphi, Br, Bz = self.magneticfield.evaluateB(X=np.array([r, 0, z]))
        B = np.sqrt(Br**2 + Bphi**2 + Bz**2)

        return Br, Bphi, Bz, B

    def loadDataFile(self, filename):
        """
        Load a file containing a SOFT magnetic equilibrium

        filename: Path to file to load.
        """
        self.magneticfield = MagneticField(filename)
        self._meqfile = filename

        wallR, wallZ = self.magneticfield.getWall()

        self.rmin, self.rmax = np.amin(wallR), np.amax(wallR)
        self.zmin, self.zmax = np.amin(wallZ), np.amax(wallZ)


    def savePlot(self, filename):
        # TODO Work in progress...
        self.axes.set_axis_off()
        self.figure.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        self.axes.get_xaxis().set_major_locator(matplotlib.ticker.NullLocator())
        self.axes.get_yaxis().set_major_locator(matplotlib.ticker.NullLocator())

        self.canvas.print_figure(filename, bbox_inches='tight', pad_inches=0, facecolor='black')

    def update(self):
        self.canvas.draw()

    #TODO TODO TODO
    def updateNameAndDescription(self, name, desc):
        """
        Update the name and description fields of the eq file
        """
        self.magneticfield.name = name
        self.magneticfield.description = desc

        self.magneticfield.writeFile()


    ####################################################
    #
    # SEMI-PUBLIC PLOT ROUTINES
    #
    ####################################################
    def clearPlot(self):
        """
        Clear the canvas
        """
        self.figure.clear()

        # Reset plot handles
        self._fluxOverlayHandles = []
        self._magneticAxisHandle = None
        self._orbitHandles = []
        self._separatrixOverlayHandle = None
        self._wallOverlayHandle = None

    def plotOverlays(self):
        """
        Plot wall/flux surface overlays as specified in
        the 'overlays' list.
        """
        if self.overlayFluxSurfaces:
            self.plotFluxSurfaces()
        if self.overlayMagneticAxis:
            self.plotMagneticAxis()
        if self.overlaySeparatrix:
            self.plotSeparatrix()
        if self.overlayWallCrossSection:
            self.plotWallCrossSection()

    def plotEq(self):
        """
        Plot the magnetic field
        """
        Bsum = 0

        if self.plotBr:   Bsum += self.magneticfield.Br**2
        if self.plotBphi: Bsum += self.magneticfield.Bphi**2
        if self.plotBz:   Bsum += self.magneticfield.Bz**2

        B = np.sqrt(Bsum)
        if not hasattr(B, "__len__"): return

        self.axes.contour(self.magneticfield.meshR, self.magneticfield.meshZ, B)

    def plotFluxSurfaces(self, plotstyle='k-', linewidth=2):
        """
        Overlay the plot with flux surfaces
        """
        if self.flux is None:
            raise ValueError('No flux surfaces have been provided!')

        self.removeFluxSurfaces()

        R = self.flux['R']
        Z = self.flux['Z']
        lengths = self.flux['lengths']
        for i in range(0, len(lengths)):
            h = self.axes.plot(R[i][:lengths[i]], Z[i][:lengths[i]], plotstyle, linewidth=linewidth)
            self._fluxOverlayHandles.append(h.pop(0))

    def removeFluxSurfaces(self):
        """
        Remove all painted flux surfaces (if any)
        """
        if self._fluxOverlayHandles is not None:
            for h in self._fluxOverlayHandles:
                h.remove()

            self._fluxOverlayHandles = []
        self.overlayFluxSurfaces = False

    def plotMagneticAxis(self, plotstyle='rs', linewidth=3):
        """
        Plot the magnetic axis
        """

        self.removeMagneticAxis()
        l = self.axes.plot(self.magneticfield.maxis[0], self.magneticfield.maxis[1], plotstyle, linewidth=linewidth)
        self._magneticAxisHandle = l.pop(0)
        self.overlayMagneticAxis = True

    def removeMagneticAxis(self):
        """
        Removes the magnetic axis overlay from the plot
        """

        if self._magneticAxisHandle is not None:
            self._magneticAxisHandle.remove()
            self._magneticAxisHandle = None

        self.overlayMagneticAxis = False

    def plotWallCrossSection(self, plotstyle='k', linewidth=3):
        """
        Paint the wall cross section
        """

        self.removeWallCrossSection()
        R, Z = self.magneticfield.getWall()
        l = self.axes.plot(R, Z, plotstyle, linewidth=linewidth)
        self._wallCrossSectionOverlayHandle = l.pop(0)
        self.overlayWallCrossSection = True

    def removeWallCrossSection(self):
        """
        Removes any wall cross section overlay plotted
        over the image.
        """
        if self._wallCrossSectionOverlayHandle is not None:
            self._wallCrossSectionOverlayHandle.remove()
            self._wallCrossSectionOverlayHandle = None

        self.overlayWallCrossSection = False

    def plotSeparatrix(self, plotstyle='r', linewidth=2):
        """
        Plots a separatrix ovelay over the image.
        Also toggles the setting so that 'assembleImage' will
        automatically include the overlay.
        """
        if self.magneticfield.separatrix is None:
            raise ValueError("No separatrix data has been provided!")

        self.removeSeparatrix()
        R, Z = self.magneticfield.getSeparatrix()
        self._separatrixOverlayHandle = self.axes.plot(R, Z, plotstyle, linewidth=linewidth)
        self.overlaySeparatrix = True

    def removeSeparatrix(self):
        """
        Removes any separatrix overlay imposed over the image
        """
        if self._separatrixOverlayHandle is not None:
            self._separatrixOverlayHandle.remove()
            self._separatrixOverlayHandle = None

        self.overlaySeparatrix = False

    def plotOrbit(self, R, Z, plotstyle=None, linewidth=1):
        """
        Plots the orbit specified by R and Z coordinates
        """

        if plotstyle is None:
            plotstyle = self.getNextOrbitStyle()

        l = self.axes.plot(R, Z, plotstyle, linewidth)
        self._orbitHandles.append(l.pop(0))
        self.adjustAxes()

    def clearOrbits(self):
        """
        Remove all orbits from the plot
        """
        if self._orbitHandles is not None:
            for h in self._orbitHandles:
                h.remove()

            self._orbitHandles = []

    def getNextOrbitStyle(self):
        """
        Get the linestyle to use for next orbit
        """
        clrs = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        styles = [s for s in clrs] + [s+'--' for s in clrs] + [s+':' for s in clrs] + [s+'-.' for s in clrs]

        i = len(self._orbitHandles) % len(styles)

        return styles[i]

    ####################################################
    #
    # STATIC METHODS
    #
    ####################################################
    @staticmethod
    def registerGeriMap():
        """
        Register the perceptually uniform colormap 'GeriMap' with matplotlib
        """
        gm = [(0, 0, 0), (.15, .15, .5), (.3, .15, .75),
              (.6, .2, .50), (1, .25, .15), (.9, .5, 0),
              (.9, .75, .1), (.9, .9, .5), (1, 1, 1)]
        gerimap = LinearSegmentedColormap.from_list('GeriMap', gm)
        gerimap_r = LinearSegmentedColormap.from_list('GeriMap_r', gm[::-1])
        plt.register_cmap(cmap=gerimap)
        plt.register_cmap(cmap=gerimap_r)

