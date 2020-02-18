from PyQt5 import QtWidgets
from ui import meq_design
import sys
import os.path
import numpy as np
import scipy.io
import h5py
import SOFT
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from MeqPlot import MeqPlot
from SightlineMappingsWindow import SightlineMappingsWindow


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

ELECTRON_REST_MASS = 0.5109989461


class MeqWindow(QtWidgets.QMainWindow):
    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = meq_design.Ui_MeqWindow()
        self.ui.setupUi(self)

        # Parse command-line arguments
        filename = None
        if len(argv) > 1:
            raise Exception("Too many input arguments given to 'meq'.");
        elif len(argv) == 1:
            filename = argv[0]

        # Create plot window
        self.plotWindow = PlotWindow()
        self.meqplot = MeqPlot(self.plotWindow.figure, self.plotWindow.canvas)

        # Sightline mappings window
        self.sightlineMappingsWindow = SightlineMappingsWindow()

        # Bind to events
        self.bindEvents()

        # Check command-line arguments
        if filename is not None and os.path.isfile(filename):
            self.loadFile(filename)


    def bindEvents(self):
        # Browse
        self.ui.btnBrowse.clicked.connect(self.openFile)

        # Metadata
        self.ui.btnSaveMetadata.clicked.connect(self.saveMetadata)

        # Plot
        self.ui.cbBr.stateChanged.connect(self.cbPlotChanged)
        self.ui.cbBphi.stateChanged.connect(self.cbPlotChanged)
        self.ui.cbBz.stateChanged.connect(self.cbPlotChanged)
        self.ui.cbWall.stateChanged.connect(self.cbPlotChanged)
        self.ui.cbSeparatrix.stateChanged.connect(self.cbPlotChanged)
        self.ui.cbFlux.stateChanged.connect(self.cbPlotChanged)
        self.ui.cbMaxis.stateChanged.connect(self.cbPlotChanged)

        # Orbit
        self.ui.btnGCOrbit.clicked.connect(self.plotGCOrbit)
        self.ui.btnParticleOrbit.clicked.connect(self.plotParticleOrbit)
        self.ui.btnClearOrbits.clicked.connect(self.clearOrbits)

        # Sightline handling
        self.ui.btnSightlines.clicked.connect(self.sightlineMappings)

        # Plot-window
        self.plotWindow.canvas.mpl_connect('button_press_event', self.pointSelected)

    def cbPlotChanged(self):
        self.meqplot.plotBr = self.ui.cbBr.isChecked()
        self.meqplot.plotBphi = self.ui.cbBphi.isChecked()
        self.meqplot.plotBz = self.ui.cbBz.isChecked()
        self.meqplot.overlayFluxSurfaces = self.ui.cbFlux.isChecked()
        self.meqplot.overlaySeparatrix = self.ui.cbSeparatrix.isChecked()
        self.meqplot.overlayWallCrossSection = self.ui.cbWall.isChecked()
        self.meqplot.overlayMagneticAxis = self.ui.cbMaxis.isChecked()

        self.refreshImage()

    def closeEvent(self, event):
        self.exit()

    def exit(self):
        self.plotWindow.close()
        self.close()

    def loadFile(self, filename):
        try:
            self.meqplot.loadDataFile(filename)

            self.ui.tbMeqFile.setText(filename)
            self.sightlineMappingsWindow.setMagneticField(filename)
            self.filename = filename

            self.meqfileUpdated()

            if not self.meqplot.hasSeparatrix():
                self.ui.cbSeparatrix.setChecked(False)
                self.ui.cbSeparatrix.setEnabled(False)
            else:
                self.ui.cbSeparatrix.setEnabled(True)

            # Enable things to plot
            self.cbPlotChanged()
        except OSError as ex:
            QMessageBox.critical(self, 'Invalid input file', "The specified file is either corrupted or not a SOFT magnetic equilibrium file.\n\n{0}".format(ex))

    def meqfileUpdated(self):
        if self.filename is not None:
            self.ui.gbMetadata.setEnabled(True)
            self.ui.gbPlot.setEnabled(True)
            self.ui.gbOrbits.setEnabled(True)

            if not self.filename.endswith('.mat'):
                self.ui.btnSaveMetadata.setEnabled(True)
        else:
            self.ui.gbMetadata.setEnabled(False)
            self.ui.gbPlot.setEnabled(False)
            self.ui.gbOrbits.setEnabled(False)
            self.ui.btnSaveMetadata.setEnabled(False)

        self.ui.tbName.setText(self.meqplot.magneticfield.name)
        self.ui.tbDescription.setPlainText(self.meqplot.magneticfield.description)
        self.ui.lblMaxis.setText('(%.3f, %.3f)' % (self.meqplot.magneticfield.maxis[0], self.meqplot.magneticfield.maxis[1]))

        # Calculate flux surfaces for future use
        self.meqplot.calculateFluxSurfaces()

        # Get plasma boundaries
        r0, rmax = self.meqplot.getPlasmaBoundaries()

        self.ui.dsbRadius.setRange(r0, rmax*2)
        self.ui.dsbRadius.setValue(r0+(rmax-r0)*0.6)
        self.ui.lblMinorRadius.setText('{:.2f} cm'.format((rmax-r0)*100))
        self.ui.lblMajorRadius.setText('{:.2f} m'.format(rmax))

        # Calculate magnetic field at axis
        self.evalBAt(self.meqplot.magneticfield.maxis[0], self.meqplot.magneticfield.maxis[1])

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT Magnetic Equilibrium file", filter="SOFT Magnetic Equilibrium (*.mat *.h5 *.hdf5);;All files (*.*)")

        if filename:
            self.loadFile(filename)

    def refreshImage(self):
        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        #self.plotWindow.plotImage(self.meqplot)
        self.meqplot.assemblePlot()
        self.meqplot.axes.axis('equal')
        self.plotWindow.drawSafe()

    def saveMetadata(self):
        self.meqplot.updateNameAndDescription(self.ui.tbName.text(), self.ui.tbDescription.toPlainText())
        QMessageBox.information(self, 'Equilibrium metadata updated', 'The SOFT magnetic equilibrium meta data was successfully updated.')

    #############################
    #
    # ORBITS
    #
    #############################
    def clearOrbits(self):
        self.meqplot.clearOrbits()
        self.meqplot.update()

    def plotGCOrbit(self):
        global ELECTRON_REST_MASS
        r = self.ui.dsbRadius.value()
        p = self.ui.dsbMomentum.value() / ELECTRON_REST_MASS
        theta = self.ui.dsbPitch.value()

        try:
            T, X, Y, Z = SOFT.runOrbit(minradius=r, maxradius=r, nradius=1, momentum=p, pitchangle=theta, meqfile=self.ui.tbMeqFile.text(), gc_position=False, reverseOrbit=self.ui.cbReverseOrbit.isChecked())
            R = np.sqrt(X**2 + Y**2)

            self.meqplot.plotOrbit(R[0], Z[0])
            self.meqplot.update()
        except RuntimeError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.setWindowTitle('SOFT Error')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def plotParticleOrbit(self):
        global ELECTRON_REST_MASS
        r = self.ui.dsbRadius.value()
        p = self.ui.dsbMomentum.value() / ELECTRON_REST_MASS
        theta = self.ui.dsbPitch.value()

        try:
            T, X, Y, Z = SOFT.runOrbit(minradius=r, maxradius=r, nradius=1, momentum=p, pitchangle=theta, meqfile=self.ui.tbMeqFile.text(), particleOrbit=True, reverseOrbit=self.ui.cbReverseOrbit.isChecked())
            R = np.sqrt(X**2 + Y**2)

            self.meqplot.plotOrbit(R, Z)
            self.meqplot.update()
        except RuntimeError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.setWindowTitle('SOFT Error')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def evalBAt(self, R, Z):
        Br, Bphi, Bz, B = self.meqplot.evaluateB(R, Z)
    
        self.ui.lblSampledB.setText("(%.3f, %.3f) m" % (R,Z))
        self.ui.lblBStrength.setText("%.3f T" % B)
        self.ui.lblBComp.setText("(%.3f, %.3f, %.3f) T" % (Br, Bphi, Bz))

    def pointSelected(self, event):
        R = event.xdata
        Z = event.ydata

        self.evalBAt(R, Z)


    def sightlineMappings(self):
        self.sightlineMappingsWindow.show()


######################################
# PLOT WINDOW CLASS
######################################
class PlotWindow(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = None
        self.setWindowTitle('Magnetic Equilibrium')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.resize(600,800)

    def drawSafe(self):
        try:
            self.canvas.draw()
        except RuntimeError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(e.strerror)
            msg.setWindowTitle('Runtime Error')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

