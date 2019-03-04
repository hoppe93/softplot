
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from ui.green import SingleEnergyPitchIJ_design
import numpy as np
import os

from PlotWindow import PlotWindow

from Green import Green

from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

class SingleEnergyPitchIJ(QtWidgets.QMainWindow):
    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = SingleEnergyPitchIJ_design.Ui_SingleEnergyPitchIJ()
        self.ui.setupUi(self)

        filename = None
        if len(argv) > 1:
            raise Exception("Too many input arguments given to 's12ij'.")
        elif len(argv) == 1:
            filename = argv[0]

        self.plotWindow = PlotWindow()
        
        self.GF = None
        self.GFintensity = None

        self.superPlotCanvas = None
        self.superPlotLayout = None
        self.superPlotAx = None
        self.superPlotHandle = None
        self.superPlotDomHandle = None
        self.pitchAngles = None
        self.overlay = None
        self.overlayHandle = None

        self.toggleEnabled(False)

        self.bindEvents()

        if filename is not None and os.path.isfile(filename):
            self.loadFile(filename)


    def bindEvents(self):
        self.ui.btnBrowse.clicked.connect(self.openFile)
        self.ui.btnBrowseOverlay.clicked.connect(self.openOverlay)

        self.ui.sliderEnergy.valueChanged.connect(self.energyChanged)
        self.ui.sliderPitchAngle.valueChanged.connect(self.pitchAngleParameterChanged)
        self.ui.sliderOverlay.valueChanged.connect(self.updateOverlay)

    def closeEvent(self, event):
        self.exit()

    def exit(self):
        self.plotWindow.close()
        self.close()

    def setupSuperPlot(self):
        ymax = 1.1
        z = np.zeros(self.pitchAngles.shape)

        self.superPlotLayout = QtWidgets.QVBoxLayout(self.ui.widgetDistPlot)

        self.superPlotCanvas = FigureCanvas(Figure())
        self.superPlotLayout.addWidget(self.superPlotCanvas)

        self.superPlotAx = self.superPlotCanvas.figure.subplots()
        self.superPlotHandle, = self.superPlotAx.plot(self.pitchAngles, z)
        self.superPlotDomHandle, = self.superPlotAx.plot([0, 0], [0, ymax], 'k--')

        self.superPlotAx.set_xlim([self.pitchAngles[0], self.pitchAngles[-1]])
        self.superPlotAx.set_ylim([0, ymax])
        self.superPlotAx.get_yaxis().set_ticks([])

        self.superPlotAx.set_xlabel(r'$\theta_{\rm p}$ (rad)')
        self.superPlotAx.set_ylabel(r'$f(\theta_{\rm p}) / f_{\rm max}$')

        self.superPlotCanvas.figure.tight_layout(pad=2.5)

    def updateSuperPlot(self, f=None):
        ei = self.getEnergyIndex()

        if f is None:
            f = self.getDistributionFunction()

        superParticle = self.GFintensity[ei,:] * f
        superParticle = superParticle / np.amax(superParticle)
        maxpitch = self.pitchAngles[np.argmax(superParticle)]

        self.ui.lblDomPitch.setText('{0:.3f} rad'.format(maxpitch))

        self.superPlotHandle.set_ydata(superParticle)
        self.superPlotDomHandle.set_xdata([maxpitch, maxpitch])

        self.superPlotCanvas.draw()
        self.superPlotCanvas.flush_events()

    def getDistributionFunction(self):
        C = self.ui.sliderPitchAngle.value()

        f = np.exp(C * self.cosPitchAngles)
        return f
    
    def energyChanged(self):
        ei = self.ui.sliderEnergy.value()
        self.ui.lblEnergy.setText('{0:.2f}'.format(self.GF._param1[0][ei]))

        f = self.getDistributionFunction()
        self.updateSuperPlot(f=f)
        self.updateImage(f=f)

    def pitchAngleParameterChanged(self):
        self.ui.lblPitchAngle.setText(str(self.ui.sliderPitchAngle.value()))

        f = self.getDistributionFunction()
        self.updateSuperPlot(f=f)
        self.updateImage(f=f)
        

    def toggleEnabled(self, enabled=False):
        self.ui.lblREEnergy.setEnabled(enabled)
        self.ui.lblREPitchAngle.setEnabled(enabled)

        self.ui.lblEnergy.setEnabled(enabled)
        self.ui.lblPitchAngle.setEnabled(enabled)

        self.ui.sliderEnergy.setEnabled(enabled)
        self.ui.sliderPitchAngle.setEnabled(enabled)

        self.ui.lblEnergyMin.setEnabled(enabled)
        self.ui.lblEnergyMax.setEnabled(enabled)
        self.ui.lblPitchAngleMin.setEnabled(enabled)
        self.ui.lblPitchAngleMax.setEnabled(enabled)

        self.ui.lblOverlay.setEnabled(enabled)
        self.ui.lblOverlayMin.setEnabled(enabled)
        self.ui.lblOverlayMax.setEnabled(enabled)
        self.ui.lblOverlay25.setEnabled(enabled)
        self.ui.lblOverlay50.setEnabled(enabled)
        self.ui.lblOverlay75.setEnabled(enabled)
        self.ui.btnBrowseOverlay.setEnabled(enabled)
        self.ui.tbOverlay.setEnabled(enabled)
        self.ui.sliderOverlay.setEnabled(enabled)

        self.ui.widgetDistPlot.setEnabled(enabled)

    def loadFile(self, filename):
        self.ui.tbFilename.setText(filename)

        self.GF = Green(filename)

        if not self.validateGreensFunction(self.GF):
            return

        self.toggleEnabled(True)
        self.pitchAngles = np.abs(self.GF._param2[0])
        self.cosPitchAngles = np.cos(self.pitchAngles)

        # Sum all pixels of each image
        self.GFintensity = np.sum(self.GF.FUNC, axis=(2,3)) * np.sin(self.pitchAngles)

        self.setupEnergySlider()
        self.setupSuperPlot()
        self.setupImage()

        f = self.getDistributionFunction()
        self.updateSuperPlot(f=f)
        self.updateImage(f=f)

    def loadOverlay(self, filename):
        self.ui.tbOverlay.setText(filename)
        self.overlay = mpimg.imread(filename)

        if self.overlayHandle is not None:
            self.overlayHandle.remove()
            
        a = (self.ui.sliderOverlay.value()) / 100.0
        self.overlayHandle = self.imageAx.imshow(self.overlay, alpha=a, extent=[-1,1,-1,1])
        self.plotWindow.drawSafe()
        
    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT Green's function file", filter="SOFT Green's function (*.mat *.h5 *.hdf5);;All files (*.*)")

        if filename:
            self.loadFile(filename)

    def openOverlay(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open image overlay", filter="Portable Network Graphics (*.png)")

        if filename:
            self.loadOverlay(filename)

    def validateGreensFunction(self, gf):
        if gf.getFormat() != '12ij':
            QMessageBox.critical(self, 'Invalid input file', "The specified Green's function is not of the appropriate format. Expected '12ij', got '{0}'.".format(gf.getFormat()))
            return False

        pn = gf.getParameterName('1')
        if pn != 'gamma' and pn != 'p':
            QMessageBox.critical(self, 'Invalid input file', "The first momentum parameter has an invalid type: '{0}'. Expected either 'gamma' or 'p'.".format(pn))
            return False

        return True

    def setupEnergySlider(self):
        vmin, vmax, vn = self.GF._param1[0][0], self.GF._param1[0][-1], self.GF._param1[0].size

        if self.GF.getParameterName('1') == 'gamma':
            self.ui.lblREEnergy.setText('Runaway energy (mc²)')
        else:
            self.ui.lblREEnergy.setText('Runaway momentum (mc)')

        self.ui.lblEnergyMin.setText('{0:.2f}'.format(vmin))
        self.ui.lblEnergyMax.setText('{0:.2f}'.format(vmax))
        self.ui.lblEnergy.setText('{0:.2f}'.format(vmin))

        self.ui.sliderEnergy.setMinimum(0)
        self.ui.sliderEnergy.setMaximum(vn-1)
        self.ui.sliderEnergy.setSingleStep(1)

    def getEnergyIndex(self):
        return self.ui.sliderEnergy.value()

    
    def setupImage(self):
        self.imageAx = self.plotWindow.figure.add_subplot(111)

        dummy = np.zeros(self.GF._pixels)
        self.imageHandle = self.imageAx.imshow(dummy, cmap='GeriMap', interpolation=None, clim=(0, 1), extent=[-1,1,-1,1])
        self.imageAx.get_xaxis().set_visible(False)
        self.imageAx.get_yaxis().set_visible(False)

        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        self.plotWindow.drawSafe()


    def updateOverlay(self):
        if self.overlayHandle is not None:
            a = float(self.ui.sliderOverlay.value()) / 100.0
            self.overlayHandle.set_alpha(a)
            self.plotWindow.drawSafe()


    def updateImage(self, f=None):
        ei = self.getEnergyIndex()

        if f is None:
            f = self.getDistributionFunction()

        g = self.GF[ei,:,:,:]
        I = 0
        for i in range(0, f.size):
            I += g[i,:,:] * f[i]

        I = I.T / np.amax(I)

        self.imageHandle.set_data(I)
        self.plotWindow.drawSafe()


