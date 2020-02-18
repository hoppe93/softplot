
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from ui import orbits_design
import numpy as np
import os
import time

from PlotWindow import PlotWindow
from PlotSliderWindow import PlotSliderWindow
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

        self.ORBIT_CLASS_DISCARDED = 5
        self.CLASSNAMES = [
            'Unknown',
            'Collided',
            'Stagnated',
            'Passing',
            'Trapped',
            'Discarded'
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

        # Plot windows (for 1D plots)
        self.windows = {}
        self.windows['Orbit1D']  = (PlotWindow(800, 500), self.updatePlotOrbit1D)
        self.windows['Orbit2D']  = (PlotWindow(), self.updatePlotOrbit2D)
        self.windows['Ppar']     = (PlotWindow(800, 500), self.updatePlotPpar)
        self.windows['Pperp']    = (PlotWindow(800, 500), self.updatePlotPperp)
        self.windows['Pitch']    = (PlotWindow(800, 500), self.updatePlotPitch)
        self.windows['B']        = (PlotWindow(800, 500), self.updatePlotB)
        self.windows['Time']     = (PlotWindow(800, 500), self.updatePlotTime)
        self.windows['Jacobian'] = (PlotWindow(800, 500), self.updatePlotJ)

        self.spaceWindows = {}
        self.spaceWindows['class']   = PlotSliderWindow(800, 500)
        self.spaceWindows['minB']    = PlotSliderWindow(800, 500)
        self.spaceWindows['maxB']    = PlotSliderWindow(800, 500)
        self.spaceWindows['transit'] = PlotSliderWindow(800, 500)
        self.spaceWindows['Jacobian'] = PlotSliderWindow(800, 500)

        self.toggleEnabled(False)
        self.bindEvents()

        if filename is not None and os.path.isfile(filename):
            self.loadFile(filename)


    def bindEvents(self):
        self.ui.btnBrowse.clicked.connect(self.browseFile)

        self.ui.hsRadius.valueChanged.connect(self.hsRadiusChanged)
        self.ui.hsParam1.valueChanged.connect(self.hsParam1Changed)
        self.ui.hsParam2.valueChanged.connect(self.hsParam2Changed)

        self.ui.btnPlotOrbit1D.clicked.connect(self.plotOrbit1D)
        self.ui.btnPlotOrbit2D.clicked.connect(self.plotOrbit2D)
        self.ui.btnPlotPpar.clicked.connect(self.plotPpar)
        self.ui.btnPlotPperp.clicked.connect(self.plotPperp)
        self.ui.btnPlotPitch.clicked.connect(self.plotPitch)
        self.ui.btnPlotB.clicked.connect(self.plotB)
        self.ui.btnPlotJ.clicked.connect(self.plotJacobian)

        self.ui.btnShowClassification.clicked.connect(self.plotClassification)
        self.ui.btnShowMinB.clicked.connect(self.plotMinBSpace)
        self.ui.btnShowMaxB.clicked.connect(self.plotMaxBSpace)
        self.ui.btnShowTransitTime.clicked.connect(self.plotTransitTimeSpace)
        self.ui.btnShowJacobian.clicked.connect(self.plotJacobianSpace)


    def browseFile(self):
        """
        Show an "open file" dialog and request that the
        user specifies which file to load. Also calls
        'loadFile()' to open the specified file.
        """
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT Orbits file", filter="SOFT Orbits file (*.mat *.h5 *.hdf5);;All files (*.*)")

        if filename:
            self.loadFile(filename)


    def closeEvent(self, event):
        self.exit()


    def exit(self):
        for _, w in self.windows.items():
            if w[0].isVisible():
                w[0].close()

        for _, w in self.spaceWindows.items():
            if w.isVisible():
                w.close()

        self.close()

    
    def getSelectedOrbit(self):
        """
        Returns the currently selected orbit.
        """
        idxr = self.ui.hsRadius.value()
        idx1 = self.ui.hsParam1.value()
        idx2 = self.ui.hsParam2.value()

        idx  = (idx2 + self.orbits._n2*(idx1 + self.orbits._n1*idxr))
        return self.orbits[idx]


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


    def plotOrbit1D(self):
        orb = self.getSelectedOrbit()
        if orb is None: return

        window = self.windows['Orbit1D'][0]
        R, _ = orb.getRZ()
        T    = orb.getTime()

        self.plotQuantity(window, T, R, ylabel='$R$ (m)')


    def plotOrbit2D(self):
        orb = self.getSelectedOrbit()
        if orb is None: return

        R, Z = orb.getRZ()
        window = self.windows['Orbit2D'][0]

        self.plotQuantity(window, R, Z, xlabel='$R$ (m)', ylabel='$Z$ (m)', autolimits=False)

        if orb.WALL is not None:
            window.ax.plot(orb.WALL[0,:], orb.WALL[1,:], 'k-', linewidth=3)

        if orb.SEPARATRIX is not None:
            window.ax.plot(orb.SEPARATRIX[0,:], orb.SEPARATRIX[1,:], 'k--', linewidth=2)

        window.ax.set_aspect('equal', 'box')


    def plotPpar(self):
        orb = self.getSelectedOrbit()
        if orb is None: return

        window = self.windows['Ppar'][0]
        PPAR = orb.PPAR
        T    = orb.getTime()

        self.plotQuantity(window, T, PPAR, ylabel='$p_\parallel / mc$')

        # Plot ppar = 0
        window.h0, = window.ax.plot([T[0], T[-1]], [0, 0], 'k--', linewidth=1)


    def plotPperp(self):
        orb    = self.getSelectedOrbit()
        if orb is None: return

        window = self.windows['Pperp'][0]
        PPERP  = orb.PPERP
        T      = orb.getTime()

        self.plotQuantity(window, T, PPERP, ylabel='$p_\perp / mc$')


    def plotPitch(self):
        orb    = self.getSelectedOrbit()
        if orb is None: return

        window = self.windows['Pitch'][0]
        XI     = orb.XI
        T      = orb.getTime()

        self.plotQuantity(window, T, XI, ylabel=r'$\xi$')

        # Plot ppar = 0
        window.h0, = window.ax.plot([T[0], T[-1]], [0, 0], 'k--', linewidth=1)


    def plotB(self):
        orb    = self.getSelectedOrbit()
        if orb is None: return

        window = self.windows['B'][0]
        B      = orb.Babs
        T      = orb.getTime()

        self.plotQuantity(window, T, B, ylabel='$|B|$ (T)')


    def plotJacobian(self):
        orb    = self.getSelectedOrbit()
        if orb is None: return

        window = self.windows['Jacobian'][0]
        J      = orb.Jdtdrho
        T      = orb.getTime()

        self.plotQuantity(window, T, J, ylabel=r'$J\,\mathrm{d}\tau\mathrm{d}\rho$')


    def plotClassification(self):
        window = self.spaceWindows['class']
        self.plotSpace(window, r=self.orbits._radius, p1=self.orbits._param1, p2=self.orbits._param2, data=self.orbits.CLASSIFICATION, title='Orbit classification')


    def plotMinBSpace(self):
        window = self.spaceWindows['minB']
        self.plotSpace(window, r=self.orbits._radius, p1=self.orbits._param1, p2=self.orbits._param2, data=np.amin(self.orbits.BABS, axis=1), title='Minimum magnetic field')


    def plotMaxBSpace(self):
        window = self.spaceWindows['maxB']
        self.plotSpace(window, r=self.orbits._radius, p1=self.orbits._param1, p2=self.orbits._param2, data=np.amax(self.orbits.BABS, axis=1), title='Maximum magnetic field')
    

    def plotTransitTimeSpace(self):
        window = self.spaceWindows['transit']
        self.plotSpace(window, r=self.orbits._radius, p1=self.orbits._param1, p2=self.orbits._param2, data=np.amax(self.orbits.T, axis=1), title='Transit time')

    
    def plotJacobianSpace(self):
        window = self.spaceWindows['Jacobian']
        self.plotSpace(window, r=self.orbits._radius, p1=self.orbits._param1, p2=self.orbits._param2, data=np.amax(self.orbits.JACOBIAN, axis=1), title='Maximum Jacobian')


    def plotSpace(self, window, r, p1, p2, data, title=''):
        # Check which parameters are worth visualizing...
        params = []
        paramsl = [r,p1,p2]

        if r.size > 1: params.append(0)
        if p1.size > 1: params.append(1)
        if p2.size > 1: params.append(2)

        if not window.isVisible():
            window.show()

        if len(params) == 3:
            DATA = np.reshape(data, (r.size, p1.size, p2.size))
            window.setData(r, x=p1, y=p2, z=DATA, paramName='Radius', title=title, xlabel=self.PARAMNAMES[self.orbits._param1name], ylabel=self.PARAMNAMES[self.orbits._param2name])
        elif len(params) == 2:
            DATA = np.reshape(data, (1, paramsl[0].size, paramsl[1].size))
            xlabel, ylabel = None, None

            if params[0] == 0: xlabel = 'Radius (m)'
            elif params[0] == 1: xlabel = self.PARAMNAMES[self.orbits._param1name]
            else: xlabel = self.PARAMNAMES[self.orbits._param2name]

            if params[1] == 1: xlabel = self.PARAMNAMES[self.orbits._param1name]
            else: xlabel = self.PARAMNAMES[self.orbits._param2name]

            window.setData(r=np.array([0]), x=paramsl[params[0]], y=paramsl[params[1]], paramName='None', title=title, xlabel=xlabel, ylabel=ylabel)
        elif len(params) == 1:
            pass
        else:
            return


    def plotQuantity(self, window, x, y, xlabel='Time $t$ (s)', ylabel=None, autolimits=True):
        window.ax = window.figure.add_subplot(111)

        window.h, = window.ax.plot(x, y, linewidth=2)

        if xlabel is not None:
            window.ax.set_xlabel(xlabel)
        if ylabel is not None:
            window.ax.set_ylabel(ylabel)

        if autolimits:
            xmin, xmax = np.amin(x), np.amax(x)
            ymin, ymax = np.amin(y), np.amax(y)

            window.ax.set_xlim(xmin, xmax)
            window.ax.set_ylim(ymin - 0.1*(ymax-ymin), ymax + 0.1*(ymax-ymin))

        if not window.isVisible():
            window.show()


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

        self.togglePlotBtnEnabled(enabled)


    def togglePlotBtnEnabled(self, enabled):
        self.ui.btnPlotOrbit1D.setEnabled(enabled)
        self.ui.btnPlotOrbit2D.setEnabled(enabled)
        self.ui.btnPlotOrbit3D.setEnabled(enabled)
        self.ui.btnPlotPpar.setEnabled(enabled)
        self.ui.btnPlotPperp.setEnabled(enabled)
        self.ui.btnPlotPitch.setEnabled(enabled)
        self.ui.btnPlotB.setEnabled(enabled)

        self.ui.btnPlotTime.setEnabled(False)
        
        if self.orbits is not None and self.orbits.JACOBIAN is not None:
            self.ui.btnPlotJ.setEnabled(enabled)
            self.ui.btnShowJacobian.setEnabled(enabled)
        else:
            self.ui.btnPlotJ.setEnabled(False)
            self.ui.btnShowJacobian.setEnabled(False)

    
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

        self.ui.lblRadialPoints.setText('{}'.format(self.orbits._nr))
        self.ui.lblParam1Points.setText('{}'.format(self.orbits._n1))
        self.ui.lblParam2Points.setText('{}'.format(self.orbits._n2))
        self.ui.lblParam1Name.setText('{}:'.format(self.PARAMNAMES[self.orbits._param1name]))
        self.ui.lblParam2Name.setText('{}:'.format(self.PARAMNAMES[self.orbits._param2name]))

        # Get file size
        fsize = os.path.getsize(self.ui.tbFileName.text())
        units = ['B', 'kiB', 'MiB', 'GiB', 'TiB', 'PiB']
        uindx = 0
        while fsize > 1024:
            fsize /= 1024
            uindx += 1

        self.ui.lblFileSize.setText('{:.1f} {}'.format(fsize, units[uindx]))


    def updateOrbitDetails(self):
        """
        Set the labels in the 'Selected orbit' GroupBox.
        """
        orb = self.getSelectedOrbit()

        if orb is None:
            self.ui.lblClass.setText(self.CLASSNAMES[self.ORBIT_CLASS_DISCARDED])
            self.ui.lblMinB.setText('N/A')
            self.ui.lblMaxB.setText('N/A')
            self.ui.lblTransitTime.setText('N/A')

            self.togglePlotBtnEnabled(False)
            return
        else:
            self.togglePlotBtnEnabled(True)

        # Classification
        if orb.classification > 0 and orb.classification < len(self.CLASSNAMES):
            self.ui.lblClass.setText(self.CLASSNAMES[orb.classification])
        else:
            self.ui.lblClass.setText(self.CLASSNAMES[0])
        # Min B
        self.ui.lblMinB.setText('{:.2f} T'.format(np.amin(orb.Babs)))
        # Max B
        self.ui.lblMaxB.setText('{:.2f} T'.format(np.amax(orb.Babs)))

        # Transit time
        tt = orb.getTransitTime()
        ts = tt
        smallunits = ['s', 'ms', 'µs', 'ns', 'ps']
        largeunits = ['s', 'minutes', 'hours']
        unit = 's'

        if ts <= 0: pass
        elif ts < 1:
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

        # Update open orbit plots
        for _, w in self.windows.items():
            if w[0].isVisible():
                w[1]()

    
    def updatePlotOrbit1D(self):
        orb = self.getSelectedOrbit()
        R, _ = orb.getRZ()
        T    = orb.getTime()
        window = self.windows['Orbit1D'][0]

        self.updatePlotQuantity(window, T, R)

    def updatePlotOrbit2D(self):
        orb = self.getSelectedOrbit()
        R, Z = orb.getRZ()
        window = self.windows['Orbit2D'][0]
        self.updatePlotQuantity(window, R, Z, autolimits=False)

    def updatePlotPpar(self):
        orb = self.getSelectedOrbit()
        PPAR = orb.PPAR
        T    = orb.getTime()
        window = self.windows['Ppar'][0]

        window.h0.set_xdata([T[0], T[-1]])
        self.updatePlotQuantity(window, T, PPAR)

    def updatePlotPperp(self):
        orb = self.getSelectedOrbit()
        PPERP = orb.PPERP
        T    = orb.getTime()
        window = self.windows['Pperp'][0]

        self.updatePlotQuantity(window, T, PPERP)

    def updatePlotPitch(self):
        orb  = self.getSelectedOrbit()
        XI   = orb.XI
        T    = orb.getTime()
        window = self.windows['Pitch'][0]

        window.h0.set_xdata([T[0], T[-1]])
        self.updatePlotQuantity(window, T, XI)

    def updatePlotB(self):
        orb = self.getSelectedOrbit()
        B   = orb.Babs
        T   = orb.getTime()
        window = self.windows['B'][0]

        self.updatePlotQuantity(window, T, B)

    def updatePlotTime(self):
        pass

    def updatePlotJ(self):
        orb = self.getSelectedOrbit()
        J   = orb.Jdtdrho
        T   = orb.getTime()
        window = self.windows['Jacobian'][0]

        self.updatePlotQuantity(window, T, J)
    
    def updatePlotQuantity(self, window, x, y, autolimits=True):
        window.h.set_xdata(x)
        window.h.set_ydata(y)

        if autolimits:
            xmin, xmax = np.amin(x), np.amax(x)
            ymin, ymax = np.amin(y), np.amax(y)

            window.ax.set_xlim(xmin, xmax)
            window.ax.set_ylim(ymin - 0.1*(ymax-ymin), ymax + 0.1*(ymax-ymin))

        window.drawSafe()


