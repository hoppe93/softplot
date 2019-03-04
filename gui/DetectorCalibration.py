
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ui import detcal_design
import sys
import numpy as np
import numpy.linalg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.io

from MagneticField import MagneticField

from PlotWindow import PlotWindow

COLORS = {'white': (1.0, 1.0, 1.0), 'black': (0, 0, 0), 'red': (1.0, 0, 0), 'blue': (0, 0, 1.0), 'green': (0, 1.0, 0)}

class DetectorCalibration(QtWidgets.QMainWindow):
    def __init__(self, argv):
        global COLORS

        QtWidgets.QMainWindow.__init__(self)
        self.ui = detcal_design.Ui_DetectorCalibration()
        self.ui.setupUi(self)

        self.magfield = None
        self.image = None
        self.plotWindow = PlotWindow()
        self.toggleEnabled(False)

        if len(argv) > 2:
            QMessageBox.critical(self, 'Too many input arguments', 'Too many input arguments were given. Expected at most 2 arguments.')
            self.exit()

        imagefile = None
        meqfile   = None
        for arg in argv:
            if arg.endswith('.png'):
                imagefile = arg
            elif arg.endswith('.h5') or arg.endswith('.mat') or args.endswith('.hdf5'):
                meqfile = arg
            else:
                QMessageBox.critical(self, 'Unrecognized input file', 'The given input file is of an unrecognized type: {0}'.format(arg))
                self.exit()

        i, selindex = 0, 0
        for clr, _ in COLORS.items():
            self.ui.cbColor.addItem(clr)

            if clr == 'white':
                selindex = i

            i += 1
        
        self.ui.cbColor.setCurrentIndex(selindex)

        if imagefile is not None:
            self.loadImage(imagefile)
        if meqfile is not None:
            self.loadEquilibrium(meqfile)

        self.bindEvents()

    def bindEvents(self):
        self.ui.btnBrowseEq.clicked.connect(self.openEquilibrium)
        self.ui.btnBrowseImage.clicked.connect(self.openImage)
        self.ui.btnRedraw.clicked.connect(self.updateWall)

        self.ui.cbColor.currentIndexChanged.connect(self.toroidalChanged)
        self.ui.sliderToroidal.valueChanged.connect(self.toroidalChanged)
        self.ui.dsbLinewidth.valueChanged.connect(self.toroidalChanged)

    def toggleEnabled(self, enabled=False):
        self.ui.gbDetector.setEnabled(enabled)

        self.ui.gbOverlay.setEnabled(enabled)
        """
        self.ui.sliderToroidal.setEnabled(enabled)
        self.ui.lblToroidal.setEnabled(enabled)
        self.ui.lblTor0.setEnabled(enabled)
        self.ui.lblTor90.setEnabled(enabled)
        self.ui.lblTor180.setEnabled(enabled)
        self.ui.lblTor270.setEnabled(enabled)
        self.ui.lblTor360.setEnabled(enabled)
        """

    def closeEvent(self, event):
        self.exit()

    def exit(self):
        self.plotWindow.close()
        self.close()

    def openEquilibrium(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT magnetic equilibrium", filter="SOFT Equilibrium Data (*.h5 *.mat)")

        if filename:
            self.loadEquilibrium(filename)

    def loadEquilibrium(self, filename):
        self.ui.tbEquilibrium.setText(filename)
        self.magfield = MagneticField(filename)

        self.toggleEnabled(True)
        self.updateWall()
        
    def openImage(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open SOFT magnetic equilibrium", filter="Image (*.png)")

        if filename:
            self.loadImage(filename)

    def loadImage(self, filename):
        self.ui.tbImage.setText(filename)
        self.image = mpimg.imread(filename)
        
        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        self.setImage(self.image)

    def updateWall(self):
        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        try:
            detpos = np.array([float(self.ui.tbPosX.text()), float(self.ui.tbPosY.text()), float(self.ui.tbPosZ.text())])
            detdir = np.array([float(self.ui.tbDirX.text()), float(self.ui.tbDirY.text()), float(self.ui.tbDirZ.text())])
            detdir = detdir / np.linalg.norm(detdir)
            visang = float(self.ui.tbVisang.text())
            tiltAngle = float(self.ui.tbTilt.text())
            self.setWall(detpos, detdir, visang, tiltAngle)
        except ValueError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(e.strerror)
            msg.setWindowTitle('Runtime Error')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def toroidalChanged(self):
        self.plotWindow.ax = self.gen()
        self.plotWindow.drawSafe()

    def gen(self):
        fig = self.plotWindow.figure

        fig.clear()
        ax = fig.add_subplot(111)
        pixelscale = 1

        if self.magfield is not None:
            pixelscale = np.tan(self.visang) / 2
            
        if self.image is not None:
            h = self.image.shape[0]
            w = self.image.shape[1]

            extent = []
            if h >= w:
                extent = [-(w/h)*pixelscale,(w/h)*pixelscale,-pixelscale,pixelscale]
            else:
                extent = [-pixelscale,pixelscale,-(h/w)*pixelscale,(h/w)*pixelscale]

            ax.imshow(self.image, extent=extent)

        if self.magfield is not None:
            toffset = self.ui.sliderToroidal.value()
            clr = self.ui.cbColor.currentText()
            linewidth = self.ui.dsbLinewidth.value()

            plotwall(ax, self.magfield.wall, self.detpos, self.detdir, degreesStart=[toffset-30, toffset+210], degreesEnd=[toffset-29,toffset+211], tiltAngle=self.tiltAngle, color=COLORS[clr], linewidth=linewidth)
            #plotwall(ax, self.magfield.wall, self.detpos, self.detdir, degreesStart=[toffset+190], degreesEnd=[toffset+350], rlim=0.46, spacing=5, tiltAngle=self.tiltAngle, color=COLORS[clr], linewidth=linewidth)
            #plotwall(ax, self.magfield.wall, self.detpos, self.detdir, degreesStart=[toffset+190], degreesEnd=[toffset+350], zuplim=-0.4, spacing=3, tiltAngle=self.tiltAngle, color=COLORS[clr], linewidth=linewidth)

            ax.set_xlim([-pixelscale,pixelscale])
            ax.set_ylim([-pixelscale,pixelscale])

        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        ax.set_axis_off()

        return ax

    def plot(self):
        self.plotWindow.ax = self.gen()
        self.plotWindow.drawSafe()

    def setImage(self, image):
        self.image = image
        self.plot()

    def setWall(self, detpos, detdir, visang, tiltAngle):
        self.detpos = detpos
        self.detdir = detdir
        self.visang = visang
        self.tiltAngle = tiltAngle

        self.plot()


def limitwall(rc, zc, rlim, zuplim, zlowlim):
    nrc, nzc = np.array([]), np.array([])
    for i in range(len(rc)):
        if rlim <= 0 or rc[i] < rlim:
            if zuplim != 0 and zc[i] > zuplim: continue
            if zlowlim != 0 and zc[i] < zlowlim: continue

            nrc = np.append(nrc, rc[i])
            nzc = np.append(nzc, zc[i])

    return nrc, nzc

def rotateWall(rc, zc, angle=1):
    """ Rotate wall section around the symmetry axis """
    radAngle = angle * np.pi / 180
    nrc = rc * np.cos(radAngle)
    nyc =-rc * np.sin(radAngle) #here
    nzc = zc

    return nrc, nyc, nzc

def transformWall(rc, yc, zc, cameraPosition, cameraDirection):
    # [1] COMPUTE ROTATION MATRIX
    y = [0,1,0]
    v = np.cross(cameraDirection, y)
    c = np.dot(cameraDirection, y)

    vmat = [[0,-v[2],v[1]], [v[2],0,-v[0]], [-v[1],v[0],0]]
    R = np.add(np.identity(3), vmat)
    vmat2 = np.dot(vmat, vmat) * 1 / (1+c)
    R = np.add(R, vmat2)

    nrc = np.subtract(rc, cameraPosition[0])
    nyc = np.subtract(yc, cameraPosition[1])
    nzc = np.subtract(zc, cameraPosition[2])

    wallVector = np.dot(R, [nrc,nyc,nzc])

    return wallVector[0,:], wallVector[1,:], wallVector[2,:]

def plotwall(ax, wall, cameraPosition, cameraDirection, degreesStart=[0],
             degreesEnd=[360], rlim=0, zuplim=0, zlowlim=0, rmin=-1,
             rmax=1, zmin=-1, zmax=1, spacing=1, tiltAngle=0, color=(1.0,1.0,1.0),
             linewidth=1.0):
    rc = wall[0]
    zc = wall[1]

    # Limit the wall to only inner parts
    rc, zc = limitwall(rc, zc, rlim, zuplim, zlowlim)

    n = len(rc)

    for i in range(len(degreesStart)):
        for degree in range(degreesStart[i], degreesEnd[i], spacing):
            # [1] ROTATE WALL SECTION AROUND ORIGO
            nrc, nyc, nzc = rotateWall(rc, zc, angle=degree)

            # [2] ROTATE AND TRANSLATE WALL SECTION AROUND CAMERA
            nrc, nyc, nzc = transformWall(nrc, nyc, nzc, cameraPosition, cameraDirection)
            wallVector = [nrc, nzc, nyc, np.ones((1,n))[0]]

            # [3] Apply camera matrix
            cameraMatrix = [[1,0,0,0],[0,1,0,0],[0,0,1,0]]
            projectedVector = np.dot(cameraMatrix, wallVector)
            factor = np.divide(1, wallVector[2])
            factorMatrix = [factor,factor,factor]
            projectedVector = np.multiply(factorMatrix, projectedVector)

            # [4] Account for camera tilt
            r = projectedVector[0,:] * np.cos(tiltAngle) + projectedVector[1,:] * np.sin(tiltAngle)
            z =-projectedVector[0,:] * np.sin(tiltAngle) + projectedVector[1,:] * np.cos(tiltAngle)

            ax.plot(r, z, color=color, linewidth=linewidth)

