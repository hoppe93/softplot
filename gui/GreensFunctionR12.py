
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.green import r12_design
import sys
import os.path
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PlotWindow import PlotWindow

from Green import Green

class GreensFunctionR12(QtWidgets.QMainWindow):
    
    labels = {
        'gamma': r'$\gamma$',
        'ppar': r'$p_{\parallel} / mc$',
        'pperp': r'$p_{\perp} / mc$',
        'thetap': r'$\theta_{\rm p}$ (rad)',
        'ithetap': r'$\theta_{\rm p}$ (rad)',
        'xi': r'$\xi$'
    }

    
    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = r12_design.Ui_R12()
        self.ui.setupUi(self)

        if len(argv) != 1:
            raise Exception("The Green's function must be specified at startup")

        self.filename = argv[0]
        self.plotWindow = PlotWindow(width=800, height=600)
        self.ax = None
        self.colorbar = None

        self.loadGreensFunction(self.filename)
        self.setupFigure()

        self.bindEvents()


    def closeEvent(self, event):
        self.exit()


    def exit(self):
        self.plotWindow.close()
        self.close()


    def bindEvents(self):
        self.ui.rbSingleR.toggled.connect(self.toggleSingleSum)
        self.ui.sliderRadius.valueChanged.connect(self.sliderRadiusChanged)

        self.ui.btnMark.clicked.connect(self.markSuperParticle)
        self.ui.btnSave.clicked.connect(self.saveFigure)

    
    def getGF(self):
        F = None
        if self.format == '12':
            F  = self.gf.FUNC.T
            mx = np.amax(F)
            if mx != 0: F /= mx
        elif self.ui.rbSingleR.isChecked():
            idx = self.ui.sliderRadius.value()
            F   = self.gf.FUNC[idx].T
            mx  = np.amax(F)
            if mx != 0: F  /= mx
        else:
            F = np.sum(self.gf.FUNC, axis=0).T
            mx = np.amax(F)
            if mx != 0: F /= mx

        # Locate super particle
        self.getSuperParticle(F)

        return F


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
            raise Exception("The Green's function has an invalid format: '{}'. Expected '12' or 'r12'.".format(fmt))

        self.format = fmt
        
        self.ui.sliderRadius.setMaximum(self.gf.nr-1)
        self.ui.sliderRadius.setTickInterval(max(1, int(np.round(self.gf.nr / 20))))

        self.ui.lblParam1Name.setText('Parameter 1 ({}):'.format(self.gf._param1name))
        self.ui.lblParam2Name.setText('Parameter 2 ({}):'.format(self.gf._param2name))

        self.sliderRadiusChanged()


    def markSuperParticle(self):
        F = self.getGF()
        m1, m2, _, _ = self.getSuperParticle(F)
        self.ax.plot(m1, m2, 'x', color=(0, 1, 0), markersize=10, markeredgewidth=3)
        self.plotWindow.drawSafe()


    def redrawFigure(self):
        F = self.getGF()
        r = np.linspace(0, 1, 20)
        cntr = self.ax.contourf(self.gf._param1, self.gf._param2, F, levels=r, cmap='GeriMap', vmin=0, vmax=1)

        if self.colorbar is None:
            self.colorbar = self.plotWindow.figure.colorbar(cntr)
        else:
            self.colorbar.update_normal(cntr)

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


