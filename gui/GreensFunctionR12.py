
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.green import r12_design
import sys
import os.path
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PlotWindow import PlotWindow

from Green import Green


def calcpolangle(f):
    ang = 0.5 * np.arctan2(f[2], f[1]) * 180 / np.pi
    f[np.where(f < -45)] += 180
    fmin, fmax = -45, 135
    return ang, fmin, fmax

def calcpolfrac(f):
    fr = np.sqrt(f[1]**2 + f[2]**2) / f[0]
    fr[np.where(np.isnan(fr))] = 0
    fmin, fmax = 0, 1

    return fr, fmin, fmax

class GreensFunctionR12(QtWidgets.QMainWindow):
    
    labels = {
        'gamma': r'$\gamma$',
        'p': r'$p / mc$',
        'ppar': r'$p_{\parallel} / mc$',
        'pperp': r'$p_{\perp} / mc$',
        'thetap': r'$\theta_{\rm p}$ (rad)',
        'ithetap': r'$\theta_{\rm p}$ (rad)',
        'xi': r'$\xi$'
    }

    poltypes = {
        'Intensity': lambda f : (f[0], 0, 1),
        'Horizontal polarization': lambda f : (0.5*(f[0] + f[1]), 0, 1),
        'Vertical polarization': lambda f : (0.5*(f[0] - f[1]), 0, 1),
        'Polarization angle': calcpolangle,
        'Polarization fraction': calcpolfrac,
        'Stokes I': lambda f : (f[0], 0, 1),
        'Stokes Q': lambda f : (f[1], -1, 1),
        'Stokes U': lambda f : (f[2], -1, 1),
        'Stokes V': lambda f : (f[3], -1, 1)
    }

    
    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = r12_design.Ui_R12()
        self.ui.setupUi(self)

        if len(argv) != 1:
            raise Exception("The Green's function must be specified at startup")

        self.filename = argv[0]
        self.plotWindow = PlotWindow(width=800, height=600)
        self.radialPlotWindow = PlotWindow(width=700, height=400)
        self.ax = None
        self.radialAx = None
        self.colorbar = None

        self.hasStokesParameters = False

        for key in self.poltypes:
            self.ui.cbRadiationType.addItem(key)

        self.loadGreensFunction(self.filename)
        self.setupFigure()

        self.bindEvents()


    def closeEvent(self, event):
        self.exit()


    def exit(self):
        self.plotWindow.close()
        self.radialPlotWindow.close()
        self.close()


    def bindEvents(self):
        self.ui.rbSingleR.toggled.connect(self.toggleSingleSum)
        self.ui.sliderRadius.valueChanged.connect(self.sliderRadiusChanged)
        self.ui.cbRadiationType.currentTextChanged.connect(self.cbRadiationTypeChanged)

        self.ui.btnMark.clicked.connect(self.markSuperParticle)
        self.ui.btnPlotRadialProfile.clicked.connect(self.plotRadialProfile)
        self.ui.btnSave.clicked.connect(self.saveFigure)

    
    def getGF(self):
        F = None

        FUNC = self.gf.FUNC
        fmin, fmax = 0, 1
        if self.hasStokesParameters:
            FUNC, fmin, fmax = self.getPolFunction()

        if self.format == '12':
            F  = np.copy(FUNC).T
            mx = np.amax(np.abs(F))
            if mx != 0: F /= mx
        elif self.ui.rbSingleR.isChecked():
            idx = self.ui.sliderRadius.value()
            F   = np.copy(FUNC[idx]).T
            mx  = np.amax(np.abs(F))
            if mx != 0: F  /= mx
        else:
            F = np.sum(FUNC, axis=0).T
            mx = np.amax(np.abs(F))
            if mx != 0: F /= mx

        # Locate super particle
        self.getSuperParticle(F)

        return F, fmin, fmax


    def getPolFunction(self):
        tp = self.ui.cbRadiationType.currentText()

        fun = self.poltypes[tp]
        return fun(self.gf.FUNC)


    def getSuperParticle(self, F):
        i, j = np.unravel_index(np.argmax(F), F.shape)
        param1max = self.gf._param1[j]
        param2max = self.gf._param2[i]

        self.ui.lblParam1.setText('{:.4}'.format(param1max))
        self.ui.lblParam2.setText('{:.4}'.format(param2max))
        self.ui.lblSuperEnergy.setText('{:.4} mc²'.format(self.gf.GAMMA[i,j]))
        self.ui.lblSuperPitch.setText('{:.4} rad'.format(self.gf.THETAP[i,j]))

        return param1max, param2max, i, j


    def loadGreensFunction(self, filename):
        self.gf = Green(filename=filename)

        fmt = self.gf.getFormat()
        if fmt == '12':
            self.ui.rbSingleR.setEnabled(False)
        elif fmt != 'r12':
            raise Exception("The Green's function has an invalid format: '{}'. Expected '(s)12' or '(s)r12'.".format(fmt))

        self.format = fmt
        self.hasStokesParameters = self.gf.stokesparams
        self.ui.cbRadiationType.setEnabled(self.gf.stokesparams)

        self.ui.sliderRadius.setMaximum(self.gf.nr-1)
        self.ui.sliderRadius.setTickInterval(max(1, int(np.round(self.gf.nr / 20))))

        self.ui.lblParam1Name.setText('Parameter 1 ({}):'.format(self.gf._param1name))
        self.ui.lblParam2Name.setText('Parameter 2 ({}):'.format(self.gf._param2name))

        self.sliderRadiusChanged()


    def markSuperParticle(self):
        F, _, _ = self.getGF()
        m1, m2, _, _ = self.getSuperParticle(F)
        self.ax.plot(m1, m2, 'x', color=(0, 1, 0), markersize=10, markeredgewidth=3)
        self.plotWindow.drawSafe()


    def plotRadialProfile(self):
        mc = 9.109e-31 * 299792458
        J  = self.gf.getJacobian().T * mc**3
        r  = self.gf._r
        fr = np.zeros((r.size,))
        F  = self.gf.FUNC

        for i in range(0, r.size):
            rrr = np.sum(F[i,:,:]*J)
            fr[i] = rrr

        self.radialAx = self.radialPlotWindow.figure.add_subplot(111)
        self.radialAx.plot(r, fr / (r-r[0])**2, linewidth=2)
        self.radialAx.set_xlabel(r'$\mathrm{Major\ radius}\ \rho$')
        self.radialAx.set_ylabel(r'$\mathrm{Radial\ intensity}\ \partial I/\partial\rho$')
        self.radialPlotWindow.drawSafe()

        if not self.radialPlotWindow.isVisible():
            self.radialPlotWindow.show()


    def redrawFigure(self):
        F, fmin, fmax = self.getGF()
        r = np.linspace(fmin, fmax, 20)
        self.ax.clear()

        cmap = 'GeriMap'
        if fmin < 0:
            cmap = 'RdBu'

        cntr = self.ax.contourf(self.gf._param1, self.gf._param2, F, levels=r, cmap=cmap, vmin=fmin, vmax=fmax)

        if self.colorbar is None:
            self.colorbar = self.plotWindow.figure.colorbar(cntr)
        else:
            self.colorbar.ax.clear()
            self.colorbar = self.plotWindow.figure.colorbar(cntr, cax=self.colorbar.ax)

        self.ax.set_xlabel(self.labels[self.gf._param1name])
        self.ax.set_ylabel(self.labels[self.gf._param2name])

        self.plotWindow.drawSafe()


    def saveFigure(self):
        filename, _ = QFileDialog.getSaveFileName(self, caption='Save figure', filter='Portable Document Format (*.pdf);;Encapsulated PostScript (*.eps);;Portable Network Graphics (*.png);;All files (*.*)')

        if filename:
            self.plotWindow.canvas.print_figure(filename, bbox_inches='tight')
        

    def setupFigure(self):
        self.ax = self.plotWindow.figure.add_subplot(111)

        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        self.redrawFigure()

    
    def cbRadiationTypeChanged(self):
        self.redrawFigure()


    def sliderRadiusChanged(self):
        idx = self.ui.sliderRadius.value()
        self.ui.lblRIndex.setText(str(idx))
        self.ui.lblR.setText('r = {:.4}'.format(self.gf._r[idx]))

        if self.ax is not None:
            self.redrawFigure()


    def toggleSingleSum(self):
        enbl = self.ui.rbSingleR.isChecked()
        self.ui.sliderRadius.setEnabled(enbl)
        self.ui.lblRIndex.setEnabled(enbl)
        self.ui.lblR.setEnabled(enbl)

        self.redrawFigure()


