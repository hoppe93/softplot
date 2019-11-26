
import numpy as np
import scipy.optimize
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from ui import distfunc_anapitch_design
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class DistributionFunctionAnalysePitch(QtWidgets.QDialog):
    

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        super(DistributionFunctionAnalysePitch, self).setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.ui = distfunc_anapitch_design.Ui_DistributionFunctionAnalysePitch()
        self.ui.setupUi(self)

        self.rindex   = 0
        self.r        = 0
        self.distfunc = None

        self.figure  = Figure(tight_layout=True)
        self.canvas  = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax      = None

        self.fmax    = 0
        self.fabsmin = 0

        self.plotLayout = QtWidgets.QVBoxLayout(self.ui.widgetPlot)
        self.plotLayout.addWidget(self.canvas)

        self.bindEvents()


    def bindEvents(self):
        self.ui.btnLogPlot.clicked.connect(self.toggleLogarithmicPlot)
        self.ui.sliderMomentum.valueChanged.connect(self.sliderMomentumChanged)


    def fitExponential(self, XI, F):
        f0 = F[0,0]

        def expCxi(xi, C):
            return f0*np.exp(-C*(xi+1))

        def jac(xi, C):
            return -f0*(xi+1)*np.exp(-C*(xi+1))

        popt, _ = scipy.optimize.curve_fit(expCxi, XI[:,0], F[:,0], jac=jac)
        self.ui.lblExpFit.setText('{:.5e}'.format(popt[0]))

        # Plot
        self.fitline.set_data(XI, expCxi(XI, popt[0]))


    def plotDistribution(self):
        p = self.momentum[self.ui.sliderMomentum.value()]
        P, XI, F = self.distfunc.eval(self.r, p)

        self.plotline.set_data(XI[:,0], F[:,0])
        self.fmax = np.amax(F)
        self.fabsmin = np.amin(np.abs(F))
        self.setAxisLimits()

        if self.ui.gbFit.isChecked():
            self.fitExponential(XI, F)

        self.canvas.draw()


    def setDistribution(self, radius, distfunc):
        self.rindex   = radius
        self.r        = distfunc.getRadius(radius)
        self.distfunc = distfunc
        self.momentum = distfunc.getMomentum(radius)

        self.ui.sliderMomentum.setMaximum(self.momentum.size-1)
        self.ui.sliderMomentum.setTickInterval(int(np.ceil(self.momentum.size / 20)))

        self.setupFigure()


    def setAxisLimits(self):
        if self.ax.get_yaxis().get_scale() == 'log':
            self.ax.set_ylim([self.fabsmin*0.1, self.fmax*10])
        else:
            self.ax.set_ylim([0, self.fmax*1.1])


    def setupFigure(self):
        self.ax = self.figure.add_subplot(111)
        self.plotline = self.ax.plot([], [], linewidth=2)[0]
        self.fitline  = self.ax.plot([], [], linewidth=2, linestyle='--')[0]
        self.ax.set_xlim([-1, 1])
        self.ax.set_xlabel(r'$\xi$')
        self.ax.set_ylabel(r'$f(p_0,\xi)$')

        self.plotDistribution()


    def sliderMomentumChanged(self):
        self.ui.lblMomentum.setText('{:.4e}'.format(self.momentum[self.ui.sliderMomentum.value()]))
        self.plotDistribution()


    def toggleLogarithmicPlot(self):
        if self.ax.get_yaxis().get_scale() == 'log':
            self.ax.set_yscale('linear')
            self.ui.btnLogPlot.setText('Toggle logarithmic scale')
        else:
            self.ax.set_yscale('log')
            self.ui.btnLogPlot.setText('Toggle linear scale')

        self.setAxisLimits()
        self.canvas.draw()


