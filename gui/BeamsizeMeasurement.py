
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from ui.green import BeamsizeMeasurement_design
import numpy as np
import os

from PIL import Image

from PlotWindow import PlotWindow
from Green import Green
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import skimage.measure

from evaluateExpression import evaluateExpression

class BeamsizeMeasurement(QtWidgets.QMainWindow):
    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = BeamsizeMeasurement_design.Ui_BeamsizeMeasurement()
        self.ui.setupUi(self)

        filename = None
        if len(argv) > 1:
            raise Exception("Too many input arguments given to 'beamsize'.")
        elif len(argv) == 1:
            filename = argv[0]

        self.plotWindow = PlotWindow()

        self.GF = None
        self.beamHandle = None
        self.radius = None

        self.imageContoursHandle = None
        self.imageHandle = None
        self.overlay = None
        self.overlayHandle = None

        self.toggleEnabled(False)
        self.bindEvents()

        if filename is not None and os.path.isfile(filename):
            self.loadFile(filename)

        self.setupImage()

    def bindEvents(self):
        self.ui.btnBrowse.clicked.connect(self.openFile)
        self.ui.btnBrowseOverlay.clicked.connect(self.openOverlay)

        self.ui.sliderBeamsize.valueChanged.connect(self.sliderBeamsizeChanged)
        self.ui.sliderIntensity.valueChanged.connect(self.sliderIntensityChanged)
        self.ui.tbRadialProfile.textChanged.connect(self.radialProfileChanged)

        self.ui.gbRadialProfile.toggled.connect(self.fullProfileToggled)

        self.ui.sliderIntensity.valueChanged.connect(self.intensityChanged)
        self.ui.sliderOverlay.valueChanged.connect(self.updateOverlay)

        self.ui.cbContour.toggled.connect(self.contourToggled)

        self.ui.actionSave.triggered.connect(self.saveImage)
        self.ui.actionExit.triggered.connect(self.exit)

    def closeEvent(self, event):
        self.exit()

    def contourToggled(self):
        enabled = self.ui.cbContour.isChecked()

        self.ui.sliderIntensity.setEnabled(enabled)
        self.ui.lblIntensity_desc.setEnabled(enabled)
        self.ui.lblIntensity.setEnabled(enabled)
        self.ui.lblIntensity0.setEnabled(enabled)
        self.ui.lblIntensity20.setEnabled(enabled)
        self.ui.lblIntensity40.setEnabled(enabled)
        self.ui.lblIntensity60.setEnabled(enabled)
        self.ui.lblIntensity80.setEnabled(enabled)
        self.ui.lblIntensity100.setEnabled(enabled)

        self.updateImage()

    def exit(self):
        self.plotWindow.close()
        self.close()

    def toggleEnabled(self, enabled):
        self.ui.lblBeamRadius.setEnabled(enabled)

        self.ui.sliderBeamsize.setEnabled(enabled)
        self.ui.lblBeamsize.setEnabled(enabled)
        self.ui.lblBeamsize_desc.setEnabled(enabled)
        self.ui.lblBeamsize0.setEnabled(enabled)
        self.ui.lblBeamsize20.setEnabled(enabled)
        self.ui.lblBeamsize40.setEnabled(enabled)
        self.ui.lblBeamsize60.setEnabled(enabled)
        self.ui.lblBeamsize80.setEnabled(enabled)
        self.ui.lblBeamsize100.setEnabled(enabled)

        self.ui.sliderIntensity.setEnabled(enabled)
        self.ui.lblIntensity.setEnabled(enabled)
        self.ui.lblIntensity_desc.setEnabled(enabled)
        self.ui.lblIntensity0.setEnabled(enabled)
        self.ui.lblIntensity20.setEnabled(enabled)
        self.ui.lblIntensity40.setEnabled(enabled)
        self.ui.lblIntensity60.setEnabled(enabled)
        self.ui.lblIntensity80.setEnabled(enabled)
        self.ui.lblIntensity100.setEnabled(enabled)

        self.ui.sliderOverlay.setEnabled(enabled)
        self.ui.lblOverlay_desc.setEnabled(enabled)
        self.ui.tbOverlay.setEnabled(enabled)
        self.ui.btnBrowseOverlay.setEnabled(enabled)
        self.ui.lblOverlay0.setEnabled(enabled)
        self.ui.lblOverlay20.setEnabled(enabled)
        self.ui.lblOverlay40.setEnabled(enabled)
        self.ui.lblOverlay60.setEnabled(enabled)
        self.ui.lblOverlay80.setEnabled(enabled)
        self.ui.lblOverlay100.setEnabled(enabled)
        self.ui.gbRadialProfile.setEnabled(enabled)
        
    def loadFile(self, filename):
        self.ui.tbGreensFunction.setText(filename)

        self.GF = Green(filename)

        if not self.validateGreensFunction(self.GF):
            return

        # Store radii in centimeters
        self.radius = (self.GF._r[0,:] - self.GF._r[0,0]) * 100.0
        
        self.toggleEnabled(True)
        self.ui.sliderBeamsize.setMaximum(self.GF.nr-1)
        self.ui.sliderBeamsize.setSliderPosition(self.GF.nr-1)

        self.updateBeamRadiusLabel()
        self.setupRadialProfile()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT Green's function file", filter="SOFT Green's function (*.mat *.h5 *.hdf5);;All files (*.*)")

        if filename:
            self.loadFile(filename)
    
    def loadOverlay(self, filename):
        self.ui.tbOverlay.setText(filename)
        self.overlay = mpimg.imread(filename)

        if self.overlayHandle is not None:
            self.overlayHandle.remove()

        a = (self.ui.sliderOverlay.value()) / 100.0
        self.overlayHandle = self.imageAx.imshow(self.overlay, alpha=a, extent=[-1, 1, -1, 1])
        self.plotWindow.drawSafe()

    def openOverlay(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open overlay image", filter="Portable Network Graphics (*.png)")

        if filename:
            self.loadOverlay(filename)

    def updateBeamRadiusLabel(self):
        v = self.ui.sliderBeamsize.value()
        r = self.radius[v]
        p = int(np.round((v / self.radius.size) * 100.0))

        self.ui.lblBeamRadius.setText('{0:.1f} cm'.format(r))
        self.ui.lblBeamsize.setText('{0}%'.format(p))

    def validateGreensFunction(self, gf):
        if gf.getFormat() != 'rij':
            QMessageBox.critical(self, 'Invalid input file', "The specified Green's function is not of the appropriate format. Expected 'rij', got {0}.".format(gf.getFormat()))
            return False

        return True

    def sliderBeamsizeChanged(self):
        self.updateBeamRadiusLabel()

        if self.imageHandle is not None:
            self.updateRadialProfile()

    def sliderIntensityChanged(self):
        v = self.ui.sliderIntensity.value()
        self.ui.lblIntensity.setText('{0}%'.format(v))

        i = float(v) / 100.0

    def setupRadialProfile(self):
        self.radialProfileLayout = QtWidgets.QVBoxLayout(self.ui.widgetRadialProfile)

        self.radialProfileCanvas = FigureCanvas(Figure())
        self.radialProfileLayout.addWidget(self.radialProfileCanvas)

        f = self.getRadialProfile()
        self.radialProfileAx = self.radialProfileCanvas.figure.subplots()
        self.radialProfileHandle, = self.radialProfileAx.plot(self.radius, f)

        self.radialProfileAx.set_xlim([0, self.radius[-1]])
        self.radialProfileAx.set_ylim([0, 1.2])
        
        self.radialProfileAx.set_xlabel(r'$r$ (cm)')
        self.radialProfileAx.set_ylabel(r'Radial density')

        self.radialProfileAx.figure.tight_layout(pad=4.5)

    def updateRadialProfile(self):
        f = self.getRadialProfile()
        self.radialProfileHandle.set_ydata(f)

        maxf = np.amax(f)
        if maxf == 0:
            self.radialProfileAx.set_ylim([0, 1])
        else:
            self.radialProfileAx.set_ylim([0, np.amax(f)*1.2])
            self.updateImage()

        self.radialProfileCanvas.draw()

    def getRadialProfile(self):
        s = self.ui.tbRadialProfile.toPlainText().strip()
        x = self.radius / self.radius[-1]
        f0 = np.zeros(self.radius.shape)

        if not s:
            f = np.ones(self.radius.shape)
        else:
            # Parse string
            f = None
            try:
                f = evaluateExpression(s, x)
            except Exception as ex:
                #print('ERROR: {0}'.format(ex))
                return np.zeros(self.radius.shape)

            # Set negative values to zero
            f = np.where(f < 0, f0, f)

        # Apply step function
        a = self.radius[self.ui.sliderBeamsize.value()] / self.radius[-1]
        f = np.where(x < a, f, f0)

        return f

    def radialProfileChanged(self):
        self.updateRadialProfile()

    def setupImage(self):
        self.imageAx = self.plotWindow.figure.add_subplot(111)

        dummy = np.zeros(self.GF._pixels)
        self.imageHandle = self.imageAx.imshow(dummy, cmap='GeriMap', interpolation=None, clim=(0, 1), extent=[-1, 1, -1, 1])
        self.imageAx.get_xaxis().set_visible(False)
        self.imageAx.get_yaxis().set_visible(False)

        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        self.updateImage()

    def updateImage(self):
        # Generate image
        f = self.getRadialProfile()
        img = np.zeros(self.GF._pixels)

        for i in range(0, len(self.radius)):
            img += self.GF[i,:,:] * f[i]

        img = img.T / np.amax(img)

        if self.ui.gbRadialProfile.isChecked():
            self.imageHandle.set_data(img)
        else:
            self.imageHandle.set_data(np.zeros(self.GF._pixels))

        if self.imageContoursHandle is not None:
            self.imageContoursHandle.remove()
            self.imageContoursHandle = None

        if self.ui.cbContour.isChecked():
            threshold = self.ui.sliderIntensity.value() / 100.0
            cntr = skimage.measure.find_contours(img.T, threshold)[0]

            ipix, jpix = img.shape
            i, j = cntr[:,0], cntr[:,1]
            i = (i - ipix/2) / ipix * 2
            j = (-j+ jpix/2) / jpix * 2

            self.imageContoursHandle, = self.imageAx.plot(i, j, 'w--')

        self.plotWindow.drawSafe()

    def fullProfileToggled(self):
        self.updateImage()

    def intensityChanged(self):
        self.updateImage()

    def updateOverlay(self):
        if self.overlayHandle is not None:
            a = float(self.ui.sliderOverlay.value()) / 100.0
            self.overlayHandle.set_alpha(a)
            self.plotWindow.drawSafe()

    def saveImage(self):
        """
        Save the currently displayed SOFT image to a PNG file.
        """
        filename, _ = QFileDialog.getSaveFileName(self, caption='Save image', filter='Portable Network Graphics (*.png)')

        if filename:
            f = self.getRadialProfile()
            img = np.zeros(self.GF._pixels)

            for i in range(0, len(self.radius)):
                img += self.GF[i,:,:] * f[i]

            img = img.T / np.amax(img)

            cmap = plt.get_cmap('GeriMap')
            im = Image.fromarray(np.uint8(cmap(img)*255))
            im.save(filename)


