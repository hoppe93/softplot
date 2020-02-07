
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from ui import orbits_design
import numpy as np
import os

from PlotWindow import PlotWindow
from Orbits import Orbits
from Orbit import Orbit
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker

class OrbitWindow(QtWidgets.QMainWindow):

    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = orbits_design.Ui_Orbits()
        self.ui.setupUi(self)

        self.CLASSNAMES = [
            'Unknown',
            'Collided',
            'Stagnated',
            'Passing',
            'Trapped'
        ]
        self.PARAMNAMES = {
            'gamma':   'Energy (mc^2)',
            'p':       'Momentum (mc)',
            'ppar':    'Parallel momentum (mc)',
            'pperp':   'Perpendicular momentum (mc)',
            'thetap':  'Pitch angle (rad)',
            'ithetap': 'Pitch angle (rad)',
            'xi':      'Pitch'
        }

        filename = None
        if len(argv) > 1:
            raise Exception("Too many input arguments given to 'orbits'.")
        elif len(argv) == 1:
            filename = argv[0]

        self.orbits = None

        self.toggleEnabled(False)
        self.bindEvents()

        if filename is not None and os.path.isfile(filename):
            self.loadFile(filename)


    def bindEvents(self):
        self.ui.btnBrowse.clicked.connect(self.browseFile)

        self.ui.hsRadius.valueChanged.connect(self.hsRadiusChanged)


    def browseFile(self):
        """
        Show an "open file" dialog and request that the
        user specifies which file to load. Also calls
        'loadFile()' to open the specified file.
        """
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT Orbits file", filter="SOFT Orbits file (*.mat *.h5 *.hdf5);;All files (*.*)")

        if filename:
            self.loadFile(filename)

    
    def hsRadiusChanged(self, v=None):
        idx = self.ui.hsRadius.value()
        self.ui.lblRadius.setText('{}'.format(self.orbits._radius[idx]))
        
        self.updateOrbitDetails()


    def hsParam1Changed(self, v=None):
        idx = self.ui.hsParam1.value()
        self.ui.lblParam1.setText('{}'.format(self.orbits._param1[idx]))
        
        self.updateOrbitDetails()


    def hsParam2Changed(self, v=None):
        idx = self.ui.hsParam2.value()
        self.ui.lblParam2.setText('{}'.format(self.orbits._param2[idx]))
        
        self.updateOrbitDetails()


    def loadFile(self, filename):
        self.ui.tbFileName.setText(filename)

        self.orbits = Orbits(filename)

        self.updateDetails()
        self.toggleEnabled(True)


    def toggleEnabled(self, enabled):
        self.ui.gbDetails.setEnabled(enabled)
        self.ui.hsRadius.setEnabled(enabled)
        self.ui.hsParam1.setEnabled(enabled)
        self.ui.hsParam2.setEnabled(enabled)
        self.ui.lblRadius.setEnabled(enabled)
        self.ui.lblRadiusHS.setEnabled(enabled)
        self.ui.lblParam1.setEnabled(enabled)
        self.ui.lblParam1HS.setEnabled(enabled)
        self.ui.lblParam2.setEnabled(enabled)
        self.ui.lblParam2HS.setEnabled(enabled)

        self.ui.gbOrbit.setEnabled(enabled)

        self.ui.btnPlotOrbit1D.setEnabled(enabled)
        self.ui.btnPlotOrbit2D.setEnabled(enabled)
        self.ui.btnPlotOrbit3D.setEnabled(enabled)
        self.ui.btnPlotPpar.setEnabled(enabled)
        self.ui.btnPlotPperp.setEnabled(enabled)
        self.ui.btnPlotPitch.setEnabled(enabled)
        self.ui.btnPlotB.setEnabled(enabled)
        self.ui.btnPlotTime.setEnabled(enabled)
        self.ui.btnPlotJ.setEnabled(enabled)

    
    def updateDetails(self):
        self.ui.lblNumberOfOrbits.setText('{}'.format(self.orbits.NORBITS))

        if self.orbits._param1 is None:
            raise Exception("The SOFT Orbits file must contain the configuration space variables.")

        # Set up configuration space variables
        self.ui.hsRadius.setMaximum(self.orbits._radius.size-1)
        self.ui.hsParam1.setMaximum(self.orbits._param1.size-1)
        self.ui.hsParam2.setMaximum(self.orbits._param2.size-1)

        self.ui.lblParam1HS.setText(self.PARAMNAMES[self.orbits._param1name])
        self.ui.lblParam2HS.setText(self.PARAMNAMES[self.orbits._param2name])

        self.ui.hsRadius.setSliderPosition(0)
        self.ui.hsParam1.setSliderPosition(0)
        self.ui.hsParam2.setSliderPosition(0)

        self.hsRadiusChanged()
        self.hsParam1Changed()
        self.hsParam2Changed()

        # Get file size
        fsize = os.path.getsize(self.ui.tbFileName.text())
        units = ['B', 'kiB', 'MiB', 'GiB', 'TiB', 'PiB']
        uindx = 0
        while fsize > 1024:
            fsize /= 1024
            uindx += 1

        self.ui.lblFileSize.setText('{:.1f} {}'.format(fsize, units[uindx]))


    def updateOrbitDetails(self):
        idxr = self.ui.hsRadius.value()
        idx1 = self.ui.hsParam1.value()
        idx2 = self.ui.hsParam2.value()

        idx  = (idxr + self.orbits._nr*(idx1 + self.orbits._n1*idx2))

        orb = self.orbits[idx]

        # Classification
        self.ui.lblClass.setText(self.CLASSNAMES[orb.classification])
        # Min B
        #self.ui.lblMinB.setText('{:.2f} T'.format(np.amin(orb.
        # Max B
        #
        # Transit time
        tt = orb.getTransitTime()
        ts = tt
        smallunits = ['s', 'ms', 'µs', 'ns', 'ps']
        largeunits = ['s', 'minutes', 'hours']
        unit = 's'

        if ts < 1:
            i = 0
            while ts < 1:
                ts *= 1e3
                i += 1
            unit = smallunits[i]
        elif ts >= 60:
            i = 0
            ts /= 60

            if ts > 60:
                ts /= 60
                unit = largeunits[2]
            else:
                unit = largeunits[1]

        self.ui.lblTransitTime.setText('{:.2f} {} ({:.3e} s)'.format(ts, unit, tt))


