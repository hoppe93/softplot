
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import meq_design
import sys
import os.path
import numpy as np
import scipy.io
import h5py
import SOFT
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PlotWindow import PlotWindow

from Green import Green

class GreensFunctionIJ(QtWidgets.QMainWindow):
    
    WIDTH = 550
    HEIGHT = 450

    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)

        self.setupUi()

        if len(argv) != 1:
            raise Exception("The Green's function must be specified at startup")

        self.filename=argv[0]
        
        # Create plot window
        self.plotWindow = PlotWindow()

        self.imageAx = None
        self.overlayHandle = None

        # Combobox used for select polarization quantity to plot
        self.stokesbox = None

        # Overlay controls
        self.tbOverlay        = None
        self.btnOverlay       = None
        self.lblOverlaySlider = None
        self.sliderOverlay    = None

        # Load Green's function
        self.gf = Green(filename=self.filename)
        nparams, dims = self.classifyGreensFunction(self.gf)

        self.buildControls(dims, self.gf)
        self.setDetails()

        self.setWindowTitle("Green's function with image")
        self.setupImage()


    def closeEvent(self, event):
        self.exit()


    def exit(self):
        self.plotWindow.close()
        self.close()


    def buildControls(self, dims, gf):
        i = 0
        for d in dims:
            if d == '1':
                self.buildControl(index=i, coordname=self.getCoordinateName(gf._param1name), vals=gf._param1)
            elif d == '2':
                self.buildControl(index=i, coordname=self.getCoordinateName(gf._param2name), vals=gf._param2)
            elif d == 'r':
                self.buildControl(index=i, coordname='Radius', vals=gf._r)
            elif d == 's':
                self.buildStokes(index=i, coordname='Polarization quantity')
            elif d == 'w':
                self.buildControl(index=i, coordname='Wavelength', vals=gf._wavelengths)
            else:
                raise Exception("Unrecognized or unsupported Green's function format: '{}'.".format(d))

            i += 1

        self.buildOverlay(index=i)

    
    def buildControl(self, index, coordname, vals):
        vmin = np.amin(vals)
        vmax = np.amax(vals)
        vn   = vals.size
        self.paramValues.append(vals)

        gb = QtWidgets.QGroupBox(self.centralwidget)
        gb.setTitle(coordname)
        self.controlGroupboxes.append(gb)

        vl = QtWidgets.QVBoxLayout(gb)

        lbl = QtWidgets.QLabel(gb)
        font = QtGui.QFont()
        font.setPointSize(14)
        lbl.setFont(font)
        lbl.setText('{}'.format(vmin))
        lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.paramLabels.append(lbl)

        hs = QtWidgets.QSlider(gb)
        hs.setOrientation(QtCore.Qt.Horizontal)
        hs.setMinimum(0)
        hs.setMaximum(vn-1)
        hs.setTickPosition(QtWidgets.QSlider.TicksBelow)
        hs.setTickInterval(1)
        self.paramSliders.append(hs)

        hs.valueChanged.connect(self.sliderChanged)

        vl.addWidget(lbl)
        vl.addWidget(hs)

        # Insert groupbox into window
        idx = self.verticalLayout.count()-1
        self.verticalLayout.insertWidget(idx, gb)

        self.HEIGHT += gb.height()
        self.resize(self.WIDTH, self.HEIGHT)


    def buildOverlay(self, index):
        hl = QtWidgets.QHBoxLayout()

        lbl = QtWidgets.QLabel(self.centralwidget)
        lbl.setText("Overlay:")

        tb = QtWidgets.QLineEdit(self.centralwidget)
        tb.setReadOnly(True)
        self.tbOverlay = tb

        btn = QtWidgets.QPushButton(self.centralwidget)
        btn.setText('Browse...')
        self.btnOverlay = btn
        self.btnOverlay.clicked.connect(self.openOverlay)

        lblOverlaySlider = QtWidgets.QLabel(self.centralwidget)
        lblOverlaySlider.setText('50%')
        lblOverlaySlider.setAlignment(QtCore.Qt.AlignRight)
        self.lblOverlaySlider = lblOverlaySlider

        slider = QtWidgets.QSlider(self.centralwidget)
        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        slider.setTickInterval(5)
        self.sliderOverlay = slider

        slider.valueChanged.connect(self.sliderOverlayChanged)

        hl.addWidget(tb)
        hl.addWidget(btn)

        self.verticalLayout.addWidget(lbl)
        self.verticalLayout.addLayout(hl)
        self.verticalLayout.addWidget(lblOverlaySlider)
        self.verticalLayout.addWidget(slider)

        self.HEIGHT += tb.height() + lbl.height() + slider.height() + lblOverlaySlider.height()
        self.resize(self.WIDTH, self.HEIGHT)


    def buildStokes(self, index, coordname):
        cb = QtWidgets.QComboBox(self.centralwidget)
        self.stokesbox = cb

        cb.addItem("Polarization angle")
        cb.addItem("Polarization fraction")
        cb.addItem("Stokes I")
        cb.addItem("Stokes Q")
        cb.addItem("Stokes U")
        cb.addItem("Stokes V")

        cb.setCurrentIndex(2)
        cb.currentIndexChanged.connect(self.redrawFigure)
        
        self.verticalLayout.insertWidget(index, cb)

        self.HEIGHT += cb.height()
        self.resize(self.WIDTH, self.HEIGHT)


    def classifyGreensFunction(self, gf):
        dims = gf.format

        if dims[-2] != 'i' or dims[-1] != 'j':
            raise Exception("Invalid format of Green's function. Format string must end in 'ij'.")

        # Just pick out the interesting dimensions
        dims = dims[:-2]
        nparams = len(dims)

        # Append Stoke's dimension?
        if gf.stokesparams:
            dims = 's'+dims
            nparams += 1

        return nparams, dims
        

    def getCoordinateName(self, s):
        """
        Converts a SOFT parameter name to a proper parameter label.
        """
        if s == "gamma": return "Energy (γ)"
        elif s == "p": return "Momentum (p)"
        elif s == "ppar": return "Parallel momentum"
        elif s == "pperp": return "Perpendicular momentum"
        elif s == "thetap": return "Pitch angle (θ)"
        elif s == "ithetap": return "Pitch angle (θ)"
        elif s == "xi": return "Pitch (ξ)"
        else: return "<UNKNOWN>"


    def getSelectedGreensFunction(self):
        """
        Returns the appropriate image to draw based on
        how the GUI controls are set.
        """
        F = self.gf.FUNC
        colormap = 'GeriMap'

        # Compute select polarization quantity
        if self.stokesbox is not None:
            val = self.stokesbox.currentText()

            Fmax, Fmin = None, 0
            if val == "Polarization angle":
                F = 0.5 * np.arctan2(F[2], F[1]) * 180/np.pi
                Fmax, Fmin = 90, -90
                colormap = 'RdBu'
            elif val == "Polarization fraction":
                F = np.sqrt(F[1]**2 + F[2]**2) / F[0]
                F[np.where(np.isnan(F))] = 0
                Fmax = 1
            elif val == "Stokes I":
                F = F[0]
            elif val == "Stokes Q":
                F = F[1]
            elif val == "Stokes U":
                F = F[2]
            elif val == "Stokes V":
                F = F[3]
            else:
                raise Exception("INTERNAL ERROR: Unrecognized polarization quantity select: '{}'.".format(val))

        if self.wfgb.isChecked():   # Draw with weight function
            print('Not supported yet...')
            return np.zeros(self.gf._pixels)
        else:
            indices = list()
            for s in self.paramSliders:
                F = F[s.value()]
            
            if len(F.shape) != 2:
                raise Exception('INTERNAL ERROR: F does not have the expected shape.')

            if Fmax is None:
                F /= np.amax(F)
                Fmax = 1

            return F.T, Fmax, Fmin, colormap


    def loadOverlay(self, filename):
        self.tbOverlay.setText(filename)
        self.overlay = mpimg.imread(filename)

        self.setupOverlay()


    def openOverlay(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open image overlay", filter="Portable Network Graphics (*.png)")

        if filename:
            self.loadOverlay(filename)


    def redrawFigure(self):
        F, Fmax, Fmin, cmap = self.getSelectedGreensFunction()
        self.imageHandle.set_data(F)
        self.imageHandle.set_clim(vmin=Fmin, vmax=Fmax)
        self.imageHandle.set_cmap(cmap)
        self.plotWindow.drawSafe()


    def setDetails(self):
        self.lblFilename.setText(self.filename)

        # Green's function size
        totsize = self.gf.FUNC.size*8
        fsize   = totsize
        prefixes = ['ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']
        pfi = -1 
        while fsize > 1024:
            fsize /= 1024.0
            pfi += 1

        prefix = ''
        if pfi >= 0:
            prefix = prefixes[pfi]

        self.lblGFSize.setText('{:.1f} {:s}B ({:d} bytes)'.format(fsize, prefix, totsize))

        # Format
        self.lblFormat.setText(self.gf.format)

        # Number of pixels
        hpix, vpix = self.gf._pixels[0], self.gf._pixels[1]
        self.lblPixels.setText('{} × {} pixels'.format(hpix, vpix))
        

    def setupImage(self):
        self.imageAx = self.plotWindow.figure.add_subplot(111)

        F, Fmax, Fmin, cmap = self.getSelectedGreensFunction()
        self.imageHandle = self.imageAx.imshow(F, cmap=cmap, interpolation=None, clim=(Fmin, Fmax), extent=[-1, 1, -1, 1])
        self.imageAx.get_xaxis().set_visible(False)
        self.imageAx.get_yaxis().set_visible(False)

        self.colorbar = self.plotWindow.figure.colorbar(self.imageHandle, ax=self.imageAx)

        if not self.plotWindow.isVisible():
            self.plotWindow.show()
        
        self.plotWindow.drawSafe()


    def setupOverlay(self):
        if self.overlayHandle is not None:
            self.overlayHandle.remove()

        val = self.sliderOverlay.value() / 100.0
        self.overlayHandle = self.imageAx.imshow(self.overlay, alpha=val, extent=[-1,1,-1,1], zorder=100)
        self.plotWindow.drawSafe()


    def setupUi(self):
        self.resize(self.WIDTH, self.HEIGHT)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Control groupboxes
        self.controlGroupboxes = list()
        self.paramLabels  = list()
        self.paramSliders = list()
        self.paramValues  = list()

        # Information groupbox
        gb = QtWidgets.QGroupBox(self.centralwidget)
        gb.setTitle("Green's function details")

        # (declare labels)
        self.lblFilename = QtWidgets.QLabel(gb)
        self.lblGFSize = QtWidgets.QLabel(gb)
        self.lblFormat   = QtWidgets.QLabel(gb)
        self.lblPixels   = QtWidgets.QLabel(gb)
        
        vli = QtWidgets.QVBoxLayout(gb)

        h1 = QtWidgets.QHBoxLayout()
        h1.addWidget(QtWidgets.QLabel('File name:', gb))
        h1.addWidget(self.lblFilename)

        h2 = QtWidgets.QHBoxLayout()
        h2.addWidget(QtWidgets.QLabel('Function size: ', gb))
        h2.addWidget(self.lblGFSize)

        h3 = QtWidgets.QHBoxLayout()
        h3.addWidget(QtWidgets.QLabel('Pixels:', gb))
        h3.addWidget(self.lblPixels)

        h4 = QtWidgets.QHBoxLayout()
        h4.addWidget(QtWidgets.QLabel('Format: ', gb))
        h4.addWidget(self.lblFormat)

        vli.addLayout(h1)
        vli.addLayout(h2)
        vli.addLayout(h3)
        vli.addLayout(h4)

        # Distribution function window
        self.wfgb = QtWidgets.QGroupBox(self.centralwidget)
        self.wfgb.setCheckable(True)
        self.wfgb.setChecked(False)
        self.wfgb.setTitle('Weight function')
        
        vl  = QtWidgets.QVBoxLayout(self.wfgb)

        font = QtGui.QFont()
        font.setFamily("Droid Sans Mono")

        txt = QtWidgets.QPlainTextEdit(self.wfgb)
        txt.setFont(font)
        txt.setMaximumSize(QtCore.QSize(16777215, 300))

        frm = QtWidgets.QFrame(self.wfgb)
        frm.setMinimumSize(QtCore.QSize(0, 200))
        frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frm.setFrameShadow(QtWidgets.QFrame.Raised)

        vl.addWidget(txt)
        vl.addWidget(frm)

        self.verticalLayout.addWidget(gb)
        self.verticalLayout.addWidget(self.wfgb)
        self.setCentralWidget(self.centralwidget)

        self.wfgb.toggled.connect(self.toggleWeightFunction)


    def sliderChanged(self):
        for i in range(0, len(self.paramSliders)):
            idx = self.paramSliders[i].value()
            val = self.paramValues[i][idx]
            self.paramLabels[i].setText('{}'.format(val))

        self.redrawFigure()


    def sliderOverlayChanged(self):
        val = self.sliderOverlay.value() / 100.0
        self.lblOverlaySlider.setText('{}%'.format(self.sliderOverlay.value()))

        if self.overlayHandle is not None:
            self.overlayHandle.set_alpha(val)

        self.plotWindow.drawSafe()


    def toggleWeightFunction(self):
        for gb in self.controlGroupboxes:
            gb.setEnabled(not self.wfgb.isChecked())


