
from PyQt5 import QtCore, QtGui, QtWidgets
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
            elif d == 'w':
                self.buildControl(index=i, coordname='Wavelength', vals=gf._wavelengths)
            else:
                raise Exception("Unrecognized or unsupported Green's function format: '{}'.".format(d))

            i += 1

    
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


    def classifyGreensFunction(self, gf):
        dims = gf.format

        if dims[-2] != 'i' or dims[-1] != 'j':
            raise Exception("Invalid format of Green's function. Format string must end in 'ij'.")

        # Just pick out the interesting dimensions
        dims = dims[:-2]
        nparams = len(dims)

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
        if self.wfgb.isChecked():   # Draw with weight function
            print('Not supported yet...')
            return np.zeros(self.gf._pixels)
        else:
            indices = list()
            F = self.gf.FUNC
            for s in self.paramSliders:
                F = F[s.value()]
            
            if len(F.shape) != 2:
                raise Exception('INTERNAL ERROR: F does not have the expected shape.')

            F /= np.amax(F)
            return F.T


    def redrawFigure(self):
        F = self.getSelectedGreensFunction()
        self.imageHandle.set_data(F)
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

        F = self.getSelectedGreensFunction()
        self.imageHandle = self.imageAx.imshow(F, cmap='GeriMap', interpolation=None, clim=(0, 1), extent=[-1, 1, -1, 1])
        self.imageAx.get_xaxis().set_visible(False)
        self.imageAx.get_yaxis().set_visible(False)

        if not self.plotWindow.isVisible():
            self.plotWindow.show()
        
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


    def toggleWeightFunction(self):
        for gb in self.controlGroupboxes:
            gb.setEnabled(not self.wfgb.isChecked())


