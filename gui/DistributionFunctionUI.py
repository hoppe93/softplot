
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import distfunc_design
import sys
import os.path
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PlotWindow import PlotWindow
from DistributionFunctionAnalysePitch import DistributionFunctionAnalysePitch
import time
import Bekefi

from Distribution.CODEDistribution import CODEDistribution
from Distribution.DistributionFunction import DistributionFunction
from Distribution.GOCODEDistribution import GOCODEDistribution
from Distribution.SOFTDistribution import SOFTDistribution
import GeriMap

class DistributionFunctionUI(QtWidgets.QMainWindow):
    
    def __init__(self, argv):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = distfunc_design.Ui_DistfuncUI()
        self.ui.setupUi(self)

        if len(argv) != 1:
            raise Exception("The distribution function must be specified at startup.")

        self.filename = argv[0]
        self.plotWindow = PlotWindow(width=800, height=600)
        self.ax = None
        self.radialAx = None
        self.colorbar = None

        self.radialPlotWindow = PlotWindow(width=700, height=400)

        self.anapitchWindow = DistributionFunctionAnalysePitch(self)

        self.maxF = None    # Maximum of distribution function
        self.maxP = None    # Maximum momentum on distribution grid

        self.currentPlotHandle = None
        self.plotHandles = []
        self.linestyles  = []
        self.logarithmicPlot = False

        self.generateLineStyles()

        self.loadDistribution(self.filename)
        self.setupFigure()
        
        self.bindEvents()


    def analysePitchDistribution(self):
        r = self.ui.sliderRadius.value()
        self.anapitchWindow.setDistribution(r, self.distfunc)
        self.anapitchWindow.show()


    def bindEvents(self):
        self.ui.sliderRadius.valueChanged.connect(self.sliderRadiusChanged)
        
        self.ui.gbMoments.toggled.connect(self.plotMomentsChanged)
        self.ui.cbVolumeElement.toggled.connect(self.plotMomentsChanged)

        self.ui.rbDistParPerp.toggled.connect(self.plotTypeChanged)
        self.ui.rbDistPXi.toggled.connect(self.plotTypeChanged)
        self.ui.rbDist1D.toggled.connect(self.plotTypeChanged)
        self.ui.rbSynchrotron.toggled.connect(self.rbSynchrotronChanged)
        self.ui.rbRunaway.toggled.connect(self.rbRunawayChanged)

        self.ui.btnAnalysePitch.clicked.connect(self.analysePitchDistribution)
        self.ui.btnAutomaticY.clicked.connect(self.setAutomaticYLimit)
        self.ui.btnClearKeptDistributions.clicked.connect(self.keepDistributionClear)
        self.ui.btnKeepDistribution.clicked.connect(self.keepDistribution)
        self.ui.btnUpdateYAxis.clicked.connect(self.setYLimit)
        self.ui.btnPlotCurrent.clicked.connect(self.plotCurrentDensity)
        self.ui.btnPlotRadprof.clicked.connect(self.plotRadialDensity)
        self.ui.btnMomentProfile.clicked.connect(self.plotMomentProfile)
        self.ui.btnPlotNow.clicked.connect(self.plotNow)

        self.ui.tbMinY.returnPressed.connect(self.setYLimit)
        self.ui.tbMaxY.returnPressed.connect(self.setYLimit)
        self.ui.tbRunawayPc.returnPressed.connect(self.plotNow)


    def closeEvent(self, event):
        self.exit()


    def exit(self):
        self.plotWindow.close()
        self.radialPlotWindow.close()
        self.close()


    def generateLineStyles(self):
        """
        Generate a list of line styles that can be used
        when making 1D plots.
        """
        NCOLORS = 4
        ls      = ['-', '--', ':']
        cmap    = GeriMap.get()

        for i in range(0, len(ls)*NCOLORS):
            ci  = i % NCOLORS
            li  = i % len(ls)
            clr = cmap(float(ci/NCOLORS))
            self.linestyles.append((clr, ls[li]))


    def generateMoment(self, P, XI, F):
        """
        Calculate a moment of the distribution function according
        to the settings in the 'Moments' group box in the GUI.

        P:  Momentum grid on which the distribution function is defined.
        XI: Pitch grid on which the distribution function is defined.
        F:  Distribution function.
        """
        rF = F
        logged = False  # Should the returned function be plotted on a logarithmic scale?

        if self.ui.rbSynchrotron.isChecked():
            wavelength = float(self.ui.sbSynchWavelength.value()) * 1e-9
            magfield   = self.ui.sbSynchMagneticField.value()
            synch = Bekefi.synchrotron(P, XI, wavelength, magfield)

            rF = synch * rF
        elif self.ui.rbRunaway.isChecked():
            try:
                pc = float(self.ui.tbRunawayPc.text())
                rF[np.where(P < pc)] = np.amin(rF)
                logged = True
            except ValueError:
                QMessageBox.critical(self,
                    'Invalid format for critical momentum',
                    "The specified value for the critical momentum has an invalid format.")
        else:
            print('WARNING: A moment which has not been implemented seems to have been selected. Ignoring...')


        return rF, logged


    def getAngleAveragedDistribution(self, r):
        """
        Returns the 1D function to plot at the given radius.
        This may be just the distribution function, or it may
        be the distribution weighted with some quantity.
        """
        self.logarithmicPlot = False
        p, fp = self.distfunc.getAngleAveragedDistribution(r)

        # This is difficult for 1D distributions...
        if self.ui.gbMoments.isChecked():
            pass

        return p, fp


    def getParPerpDistribution(self, r):
        """
        Returns the 2D function to plot in ppar/pperp coordinates
        at the given radius. This may be just the distribution function,
        or it may be the distribution weighted with some quantity.
        """
        p        = np.linspace(0, self.distfunc.getMaxP(), 1000)
        P, XI, F = self.distfunc.eval(r, p)

        PPAR = P*XI
        PPERP = np.sqrt(P**2 - PPAR**2)

        if self.ui.gbMoments.isChecked():
            F, self.logarithmicPlot = self.generateMoment(P, XI, F)

            if self.ui.cbVolumeElement.isChecked():
                F = F * P**2

            if self.logarithmicPlot:
                F = np.log10(np.abs(F))
        else:
            F = np.log10(np.abs(F))
            self.logarithmicPlot = True

        return PPAR, PPERP, F


    def getPXiDistribution(self, r):
        """
        Returns the 2D function to plot in p/xi coordinates at the
        given radius. This may be just the distribution function,
        or it may be the distribution weighted with some quantity.
        """
        p        = np.linspace(0, self.distfunc.getMaxP(), 1000)
        P, XI, F = self.distfunc.eval(r, p)

        if self.ui.gbMoments.isChecked():
            F, self.logarithmicPlot = self.generateMoment(P, XI, F)

            if self.ui.cbVolumeElement.isChecked():
                F = F * P**2

            if self.logarithmicPlot:
                F = np.log10(np.abs(F))
        else:
            F = np.log10(np.abs(F))
            self.logarithmicPlot = True

        return P, XI, F


    def getRadius(self):
        """
        The returns the currently selected radius.
        """
        return self.distfunc.getRadius(self.ui.sliderRadius.value())


    def keepDistribution(self):
        self.plotHandles.append(self.currentPlotHandle)
        self.currentPlotHandle = None


    def keepDistributionClear(self):
        for h in self.plotHandles:
            h.remove()

        self.plotHandles = []
        self.currentPlotHandle.remove()
        self.currentPlotHandle = None

        self.plotSelection()


    def loadDistribution(self, filename):
        """
        Load the named distribution function.

        filename: Name of file to load.
        """
        self.ui.lblFileName.setText(os.path.basename(filename))

        # Try to open the distribution using different methods
        flist = [
            self.loadGOCODEDistribution,
            self.loadCODEDistribution,
            self.loadSOFTDistribution
        ]

        found = False
        for f in flist:
            try:
                f(filename)
                found = True
                break
            except Exception as ex:
                pass

        if not found:
            QMessageBox.critical(self,
                'Unrecognized type',
                "The specified file is either corrupt or not a SOFT compatible distribution function.")
            self.exit()

        self.loadDistributionUI()


    def loadCODEDistribution(self, filename):
        self.distfunc = CODEDistribution(filename)

        self.ui.lblDistType.setText('CODE')


    def loadGOCODEDistribution(self, filename):
        self.distfunc = GOCODEDistribution(filename)

        self.ui.lblDistType.setText('GO+CODE')


    def loadSOFTDistribution(self, filename):
        self.distfunc = SOFTDistribution(filename)

        self.ui.lblDistType.setText('SOFT')
    

    def loadDistributionUI(self):
        """
        This function sets up certain parts of the UI relating
        to the distribution function, after the function has been
        loaded.
        """
        nr   = self.distfunc.getNr()
        nmom = self.distfunc.getNmomentum()

        self.maxP = self.distfunc.getMaxP()

        if nr is not None: self.ui.lblNRadii.setText(str(nr))
        else:
            raise ValueError("Internal error: Unable to determine the number of radial points in distribution.")

        if nmom is not None: self.ui.lblNMomentum.setText(str(self.distfunc.getNmom()))
        else: self.ui.lblNMomentum.setText('[Several]')

        if self.maxP is not None: self.ui.lblMaxP.setText(str(self.maxP)+'mc')
        else: self.ui.lblMaxP.setText('[Several]')

        self.ui.sliderRadius.setMaximum(nr-1)


    def plotSelection(self, vmin=None, vmax=None):
        first = False
        r  = self.getRadius()

        # 2D Ppar/Pperp distribution
        if self.ui.rbDistParPerp.isChecked():
            if self.currentPlotHandle is not None:
                self.ax.clear()
            
            PPAR, PPERP, F = self.getParPerpDistribution(r)

            self.maxF = np.amax(F)
            if self.logarithmicPlot:
                self.maxF = np.power(10, self.maxF)
            if vmax is None:
                vmax = np.amax(F)

            levels = None
            if vmin is None:
                if self.logarithmicPlot:
                    levels = np.linspace(vmax-20, vmax, 50)
                else:
                    levels = np.linspace(vmax*1e-20, vmax, 50)
            else:
                if self.logarithmicPlot:
                    levels = np.linspace(vmin, vmax, 50)
                else:
                    levels = np.linspace(vmin, vmax, 50)

            self.currentPlotHandle = self.ax.contourf(PPAR, PPERP, F, cmap='GeriMap', levels=levels)

            self.ax.set_xlabel(r'$p_\parallel$')
            self.ax.set_ylabel(r'$p_\perp / mc$')

            self.ax.set_xlim([-self.maxP, self.maxP])
            self.ax.set_ylim([0, self.maxP])
        # D P/XI distribution
        elif self.ui.rbDistPXi.isChecked():
            if self.currentPlotHandle is not None:
                self.ax.clear()

            P, XI, F = self.getPXiDistribution(r)

            self.maxF = np.amax(F)
            if self.logarithmicPlot:
                self.maxF = np.power(10, self.maxF)
            if vmax is None:
                vmax = np.amax(F)

            levels = None
            if vmin is None:
                if self.logarithmicPlot:
                    levels = np.linspace(vmax-20, vmax, 50)
                else:
                    levels = np.linspace(vmax*1e-20, vmax, 50)
            else:
                if self.logarithmicPlot:
                    levels = np.linspace(vmin, vmax, 50)
                else:
                    levels = np.linspace(vmin, vmax, 50)

            self.currentPlotHandle = self.ax.contourf(P, XI, F, cmap='GeriMap', levels=levels)
            self.ax.set_xlim([0, self.maxP])
            self.ax.set_ylim([-1, 1])

            self.ax.set_xlabel(r'$p$')
            self.ax.set_ylabel(r'$\xi$')
        # 1D angle-averaged distribution
        elif self.ui.rbDist1D.isChecked():
            if self.currentPlotHandle is None:
                lsc = self.linestyles[len(self.plotHandles)]
                self.currentPlotHandle, = self.ax.semilogy([], [], lsc[1], color=lsc[0], linewidth=3)
                first = True
            
            h = self.currentPlotHandle

            p, fp = self.getAngleAveragedDistribution(r)
            h.set_data(p, fp)
            self.ax.set_xlim([0, self.maxP])
            self.setYLimit()

            self.maxF = np.amax(fp)
        else:
            raise Exception("Unrecognized or no plot type selected.")

        if first:
            self.setAutomaticYLimit()

        self.plotWindow.drawSafe()


    def rbRunawayChanged(self, checked):
        self.ui.lblRunawayPc.setEnabled(checked)
        self.ui.tbRunawayPc.setEnabled(checked)

        self.plotMomentsChanged(checked)


    def rbSynchrotronChanged(self, checked):
        self.ui.lblSynchB0.setEnabled(checked)
        self.ui.lblSynchWavelength.setEnabled(checked)
        self.ui.sbSynchMagneticField.setEnabled(checked)
        self.ui.sbSynchWavelength.setEnabled(checked)

        self.plotMomentsChanged(checked)


    def plotMomentsChanged(self, checked):
        if isinstance(self, QtWidgets.QRadioButton) and not checked:
            self.ui.btnMomentProfile.setEnabled(False)
            return

        self.ui.btnMomentProfile.setEnabled(True)

        self.plotSelection()


    def plotCurrentDensity(self):
        r, nr = self.distfunc.getCurrentDensity()
        self.plotRadialProfile(r, -nr, label=r'$j(r)$ (A/m$^2$)')
        

    def plotRadialDensity(self):
        r, nr = self.distfunc.getRadialDensity()
        self.plotRadialProfile(r, nr, label=r'$n_e(r)$ (m$^{-3}$)')


    def plotMomentProfile(self):
        mc = 9.109e-31 * 299792458.0
        r = np.copy(self.distfunc._radii)[:,0]
        nr = np.zeros(r.shape)

        for i in range(0, r.size):
            print('Evaluating moment at r = {:.3f}...'.format(r[i]))

            p        = np.linspace(0, self.distfunc.getMaxP(), 1000)
            P, XI, F = self.distfunc.eval(r[i], p)

            if self.ui.gbMoments.isChecked():
                F, _ = self.generateMoment(P, XI, F)

            dp = np.zeros(p.shape)
            dp[:-1] = np.diff(p)
            dp[-1] = dp[-2]

            xi = XI[:,0]
            dxi = np.zeros(xi.shape)
            dxi[:-1] = np.diff(xi)
            dxi[-1] = dxi[-2]

            DP, DXI = np.meshgrid(dp, dxi)

            nr[i] = np.sum(F * P**2 * DP*DXI * mc**3)

        label = 'UNKNOWN'
        if self.ui.rbSynchrotron.isChecked():
            label = r'$P$ (W/m$^{3?}$)'
        elif self.ui.rbRunaway.isChecked():
            label = r'$n_{\rm RE}$ (m$^{-3}$)'

        self.plotRadialProfile(r, nr, label=label)


    def plotRadialProfile(self, r, nr, label):
        self.radialPlotAx = self.radialPlotWindow.figure.add_subplot(111)
        self.radialPlotAx.plot(r, nr, linewidth=2, color='k')
        self.radialPlotAx.set_xlabel(r'$r$ (m)')
        self.radialPlotAx.set_ylabel(label)
        self.radialPlotAx.set_xlim([0, np.amax(r)])
        self.radialPlotAx.set_ylim([0, np.amax(nr)*1.1])
        self.radialPlotWindow.drawSafe()

        if not self.radialPlotWindow.isVisible():
            self.radialPlotWindow.show()



    def plotNow(self):
        self.plotTypeChanged(True)


    def plotTypeChanged(self, checked):
        if not checked: return

        # Enable/disable moments group box
        self.ui.gbMoments.setEnabled(not self.ui.rbDist1D.isChecked())

        self.setupFigure()


    def setAutomaticYLimit(self):
        if self.maxF is None: return
        else:
            if self.logarithmicPlot or self.ax.get_yaxis().get_scale() == 'log':
                self.ui.tbMinY.setText('{:.7e}'.format(self.maxF*1e-30))
                self.ui.tbMaxY.setText('{:.7e}'.format(self.maxF*10))
            else:
                self.ui.tbMinY.setText('0')
                self.ui.tbMaxY.setText('{:.7e}'.format(self.maxF*1.1))

        self.setYLimit()


    def setYLimit(self):
        minY, maxY = 0, 0
        try:
            minY = float(self.ui.tbMinY.text())
            maxY = float(self.ui.tbMaxY.text())
        except Exception as ex:
            print(ex)
            QMessageBox.critical(self, 'Invalid Y-axis limits', "The Y-axis limits are specified in a invalid format.")
            return

        if self.ui.rbDist1D.isChecked():
            if self.logarithmicPlot:
                self.ax.set_ylim([np.log10(minY), np.log10(maxY)])
            else:
                self.ax.set_ylim([minY, maxY])
        else:
            if self.logarithmicPlot:
                self.plotSelection(vmin=np.log10(minY), vmax=np.log10(maxY))
            else:
                self.plotSelection(vmin=minY, vmax=maxY)

        self.plotWindow.drawSafe()


    def setupFigure(self):
        self.plotWindow.figure.clear()
        self.ax = self.plotWindow.figure.add_subplot(111)
        self.currentPlotHandle = None

        if not self.plotWindow.isVisible():
            self.plotWindow.show()

        self.plotSelection()


    def sliderRadiusChanged(self):
        """
        Function called when the value of the radius slider is changed.
        """
        self.ui.lblRadius.setText(str(self.getRadius()))
        self.plotSelection()


