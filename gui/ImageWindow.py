from PyQt5 import QtWidgets
from ui import image_design
import sys
import os.path
import numpy as np
import scipy.io
import h5py
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class ImageWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = image_design.Ui_ImageWindow()
        self.ui.setupUi(self)

        self.image = None
        self.filename = ""
        self.detectorPosition = None
        self.detectorDirection = None
        self.detectorVisang = None
        self.wall = None
        self.separatrix = None
        self.imageMax = 0
        self.brightImageModifier = 1
        self.imageType = ImageType.I

        # Create plot window
        self.plotWindow = PlotWindow()

        # Bind to events
        self.bindEvents()

        # Add plot types
        self.ui.cbPlotType.addItem('Normal', 0)
        self.ui.cbPlotType.addItem('Logarithmic', 1)

        # Add color map options
        self.ui.cbColormap.addItem('afmhot')
        self.ui.cbColormap.addItem('GeriMap')
        self.ui.cbColormap.addItem('gray')
        self.ui.cbColormap.addItem('viridis')
        self.ui.cbColormap.addItem('jet')

        # Add polarized image options
        for s in ImageType:
            if s != ImageType.EMPTY:
                self.ui.cbImageType.addItem(s.value)

        #self.ui.cbImageType.addItem('Image')
        #self.ui.cbImageType.addItem('Stokes Q (+)')
        #self.ui.cbImageType.addItem('Stokes Q (-)')
        #self.ui.cbImageType.addItem('Stokes U (+)')
        #self.ui.cbImageType.addItem('Stokes U (-)')
        #self.ui.cbImageType.addItem('Stokes V (+)')
        #self.ui.cbImageType.addItem('Stokes V (-)')
        #self.ui.cbImageType.addItem('Linear polarization fraction')
        #self.ui.cbImageType.addItem('Polarization angle')
        #self.ui.cbImageType.addItem('Horizontal')
        #self.ui.cbImageType.addItem('Vertical')
        #self.ui.cbImageType.addItem('Diagonal 1')
        #self.ui.cbImageType.addItem('Diagonal 2')

        # Check command-line arguments
        if len(sys.argv) == 2:
            if os.path.isfile(sys.argv[1]):
                self.ui.txtFilename.setText(os.path.abspath(sys.argv[1]))
                self.loadFile(sys.argv[1])

        self.ui.cbColormap.setCurrentIndex(1)

    def bindEvents(self):
        self.ui.sliderIntensity.valueChanged.connect(self.intensityChanged)
        self.ui.cbPlotType.currentIndexChanged.connect(self.toggleLogarithmic)
        self.ui.cbColormap.currentIndexChanged.connect(self.setColormap)
        self.ui.cbImageType.currentIndexChanged.connect(self.setImageType)
        self.ui.cbColorbar.stateChanged.connect(self.toggleColorbar)
        self.ui.cbInvert.stateChanged.connect(self.setColormap)
        self.ui.cbBrightImage.stateChanged.connect(self.intensityChanged)
        self.ui.cbRelativeColorbar.stateChanged.connect(self.toggleColorbar)
        self.ui.cbSeparatrix.stateChanged.connect(self.showSeparatrix)
        self.ui.cbTopview.stateChanged.connect(self.showTopview)
        self.ui.cbWallCross.stateChanged.connect(self.showWallCrossSection)
        self.ui.btnOpen.clicked.connect(self.openFile)
        self.ui.btnReload.clicked.connect(self.reloadFile)
        self.ui.btnSave.clicked.connect(self.saveFile)
        self.ui.btnWall.clicked.connect(self.setWallOverlay)

        self.vesselDialog.overlayChanged.connect(self.vesselUpdated)

    def closeEvent(self, event):
        self.exit()

    def exit(self):
        self.plotWindow.close()
        self.vesselDialog.close()
        self.close()

    def intensityChanged(self):
        bim = 1
        if self.ui.cbBrightImage.isChecked():
            bim = 1.0 / 100.0

        self.ui.lblIntensity.setText(str(self.ui.sliderIntensity.value()*bim)+'%')
        intmax = (self.ui.sliderIntensity.value() / 100.0) * bim
        self.plotWindow.image.changeIntensity(intmax, relative=True)
        self.plotWindow.syntheticImageUpdated()

    def loadFile(self, filename):
        self.ui.txtFilename.setText(filename)
        self.filename = filename

        self.plotWindow.image.loadImageFile(filename, self.imageType)
        imageMax = self.plotWindow.image.getImageMax()

        # Enable overlay checkboxes
        if self.plotWindow.image.hasSeparatrix():
            self.ui.cbSeparatrix.setEnabled(True)
        if self.plotWindow.image.hasTopview():
            self.ui.cbTopview.setEnabled(True)
        if self.plotWindow.image.hasWall():
            self.ui.cbWallCross.setEnabled(True)

        if imageMax == 0:
            self.statusBar().showMessage("Image is empty!")
        else:
            #self.statusBar().showMessage("Successfully loaded "+filename, 3000)
            self.statusBar().showMessage("Max value = "+str(imageMax))

        self.refreshImage()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT image file", filter="SOFT Output (*.dat *.h5 *.hdf5 *.mat *.sdt);;All files (*.*)")

        if filename:
            self.loadFile(filename)

    def refreshImage(self):
        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        self.plotWindow.plotImage()

    def reloadFile(self):
        if self.filename is "":
            return

        self.loadFile(self.filename)

    def saveFile(self):
        if not self.plotWindow.isVisible():
            QMessageBox.information(self, 'No image open', 'No SOFT image file is currently open, thus there is no image to save. Please, open an image file!')
            return

        filename, _ = QFileDialog.getSaveFileName(self, caption='Save SOFT image', filter='Encapsulated Post-Script (*.eps);;Portable Network Graphics (*.png);;Portable Document Format (*.pdf);;Scalable Vector Graphics (*.svg)')

        if filename:
            self.plotWindow.image.savePlot(filename)

    def setColormap(self):
        cmname = self.ui.cbColormap.currentText()
        if self.ui.cbInvert.isChecked():
            self.plotWindow.image.setColormap(cmname+'_r')
            self.plotWindow.syntheticImageUpdated(True)
        else:
            self.plotWindow.image.setColormap(cmname)
            self.plotWindow.syntheticImageUpdated(True)

    def setImageType(self):
        self.imageType = ImageType(self.ui.cbImageType.currentText())
        self.reloadFile()

    def setWallOverlay(self):
        self.vesselDialog.show()

    def showSeparatrix(self):
        if self.ui.cbSeparatrix.isChecked():
            self.plotWindow.image.plotSeparatrix()
        else:
            self.plotWindow.image.removeSeparatrix()

        self.plotWindow.syntheticImageUpdated()
    
    def showTopview(self):
        if self.ui.cbTopview.isChecked():
            self.plotWindow.image.plotTopview()
        else:
            self.plotWindow.image.removeTopview()

        self.plotWindow.syntheticImageUpdated()
    
    def showWallCrossSection(self):
        if self.ui.cbWallCross.isChecked():
            self.plotWindow.image.plotWallCrossSection()
        else:
            self.plotWindow.image.removeWallCrossSection()

        self.plotWindow.syntheticImageUpdated()
    
    def toggleColorbar(self):
        self.plotWindow.image.toggleColorbar(self.ui.cbColorbar.isChecked())
        self.plotWindow.image.toggleColorbarRelative(self.ui.cbRelativeColorbar.isChecked())

        if self.ui.cbColorbar.isChecked():
            self.plotWindow.image.plotColorbar()
        else:
            self.plotWindow.image.removeColorbar()

        self.plotWindow.syntheticImageUpdated()

    def toggleLogarithmic(self):
        if self.ui.cbPlotType.currentIndex() == 1:
            self.plotWindow.image.toggleLogarithmic(True)
        else:
            self.plotWindow.image.toggleLogarithmic(False)

        self.plotWindow.syntheticImageUpdated(True)

    def vesselUpdated(self, status):
        self.plotWindow.image.setOverlays(status)
        self.plotWindow.image.plotOverlays()
        self.plotWindow.syntheticImageUpdated()


class PlotWindow(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        self.figure = Figure(facecolor='black')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.image = SyntheticImage(self.figure, self.canvas)
        self.setWindowTitle('Synthetic synchrotron image')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def drawSafe(self):
        try:
            self.image.update()
        except RuntimeError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(e.strerror)
            msg.setWindowTitle('Runtime Error')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    
    def plotImage(self):
        self.image.assembleImage()
        self.drawSafe()

    def set_colormax(self, intmax=1):
        self.image.changeIntensity(intmax)

    def savePlot(self, imageData, filename, cmname=None,
                 intmin=0, intmax=1, colorbar=False):
        pass
        """
        fig = False
        if len(self.captions) == 0:
            fig = Figure(figsize=(1,1))
        else:
            sz = self.figure.get_size_inches()
            minsz = min(sz)
            fig = Figure(figsize=(minsz,minsz))

        canvas = FigureCanvas(fig)
        ax, image = self.genImage(fig, imageData, cmname, intmin,
                                  intmax, colorbar)
        self.drawCaptions(fig=fig, ax=ax)

        ax.margins(0,0)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_major_locator(matplotlib.ticker.NullLocator())
        ax.get_yaxis().set_major_locator(matplotlib.ticker.NullLocator())
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

        canvas.print_figure(filename, dpi=len(imageData[0]))
        """

    def setSyntheticImage(self, image):
        self.image = image

    def syntheticImageUpdated(self, hard=False):
        if not self.image.hasImage(): return
        if hard:
            self.image.assembleImage()

        self.drawSafe()

