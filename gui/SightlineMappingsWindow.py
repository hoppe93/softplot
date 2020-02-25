
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QFileDialog

import numpy as np
import traceback

from ui import sightlineMappings_design
from threading import Thread, Event

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from LineOfSightGeometry import LineOfSightGeometry
from MSERadialMapping import MSERadialMapping
from SightlineMappingsView import SightlineMappingsView

class SightlineMappingsWindow(QtWidgets.QFrame):

    simulationError = pyqtSignal(Exception)
    simulationFinished = pyqtSignal(int, np.ndarray, np.ndarray, np.ndarray)
    mappingFinished = pyqtSignal()

    def __init__(self, magneticField=None, width=600, height=800, parent=None):
        super(SightlineMappingsWindow, self).__init__(parent)

        self.ui = sightlineMappings_design.Ui_SightlineMappings()
        self.ui.setupUi(self)

        self.runningCalculation = False
        self.magneticField = magneticField
        self.calcThread = None
        self.result = None

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = None

        layout = QtWidgets.QVBoxLayout()
        #layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.ui.widgetPlot.setLayout(layout)

        self.bindEvents()


    def bindEvents(self):
        self.ui.btnBrowse.clicked.connect(self.openGeometryFile)
        self.ui.btnCalc.clicked.connect(self.startCalculateRadii)
        self.ui.btnViewMapping.clicked.connect(self.viewMapping)

        self.mappingFinished.connect(self.finishSimulation)
        self.simulationError.connect(self.reportError)
        self.simulationFinished.connect(self.updateProgress)


    def closeEvent(self, event):
        if self.runningCalculation:
            status = QMessageBox.question(self, 'Calculation in progress', "A SOFT radial mapping calculation is in progress. Are you sure that you would like to abort this calculation?")

            if status == QMessageBox.No:
                event.ignore()
            else:
                self.calcThread.join()


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


    def loadGeometryFile(self, filename):
        """
        Load an MSE detector geometry file.

        filename: Name of file to load.
        """
        self.ui.tbGeometryFile.setText(filename)

        self.geometry = LineOfSightGeometry(filename=filename)
        self.toggleEnabled(True)

        self.ui.progressBar.setMaximum(self.geometry.nlos())
        self.ui.progressBar.setMinimum(0)
        self.ui.lblCalcStatus.setText('Ready to map radii!')


    def openGeometryFile(self):
        """
        Launches an 'Open File dialog' in which the user can
        choose which MSE geometry file to open.
        """
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open MSE geometry file", filter="MSE geometry file (*.mat *.h5 *.hdf5);;All files (*.*)")

        if filename:
            self.loadGeometryFile(filename)


    def runSOFT(self, geom, magneticField):
        try:
            mrm = MSERadialMapping(magneticField, geom)
            r, s, rm = mrm.constructMapping(qtSignal=self.simulationFinished)

            self.result = {
                'r': r,
                'sensitivities': s,
                'radiusmap': rm
            }
        except Exception as e:
            traceback.print_exc()
            self.simulationError.emit(e)
        
        self.mappingFinished.emit()


    def setMagneticField(self, mf):
        self.magneticField = mf


    def startCalculateRadii(self):
        """
        Start the first SOFT calculation.
        """
        self.runningCalculation = True
        self.ui.btnClose.setEnabled(False)
        self.toggleEnabled(False)

        if self.ax is None:
            self.ax = self.figure.add_subplot(111)

        self.ui.lblCalcStatus.setText('Calculating radial map...')

        self.ui.progressBar.setValue(0)
        
        self.calcThread = Thread(target=self.runSOFT, args=(self.geometry, self.magneticField))
        self.calcThread.daemon = True
        self.calcThread.start()


    def stopCalculateRadii(self, msg='Done.'):
        """
        Finish the SOFT radial mapping calculation.
        """
        self.toggleEnabled(True)
        self.ui.btnClose.setEnabled(True)
        self.runningCalculation = False

        self.ui.lblCalcStatus.setText(msg)
        

    def toggleEnabled(self, enabled):
        self.ui.btnCalc.setEnabled(enabled)
        #self.ui.btnSave.setEnabled(enabled)
        #self.ui.btnPlotXS.setEnabled(enabled)


    def finishSimulation(self):
        self.ui.progressBar.setValue(self.geometry.nlos())
        self.stopCalculateRadii()


    def updateProgress(self, index, softRadii, sensitivities, radiusMap):
        self.ui.progressBar.setValue(index+1)

        self.ax.plot(softRadii, sensitivities[index])
        self.ax.set_xlim([0, np.amax(softRadii)])
        self.ax.set_ylim([0, 1.1])
        self.ax.set_xlabel('$r\ \mathrm{(m)}$')
        self.ax.set_ylabel('$\mathrm{Normalized intensity}$')

        self.drawSafe()


    def viewMapping(self):
        if self.result is None:
            return

        self.slmv = SightlineMappingsView(self.result['radiusmap'])
        self.slmv.show()


    def reportError(self, ex):
        self.ui.lblCalcStatus.setText('{}'.format(ex))
        self.stopCalculateRadii(msg='Error occured. Simulation was stopped.')

        QMessageBox.critical(self, 'Simulation error', 'An unexpected error occured during the simulation: {}'.format(ex))


