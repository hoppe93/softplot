
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class PlotSliderWindow(QtWidgets.QFrame):
    def __init__(self, width=600, height=800, parent=None):
        super(PlotSliderWindow, self).__init__(parent)

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = None
        self.setWindowTitle('Plot window')
        self.cbar = None

        hl = QtWidgets.QHBoxLayout()
        self.lblParamName = QtWidgets.QLabel(self)
        self.lblParamName.setText('Parameter name')

        self.lblParamVal = QtWidgets.QLabel(self)
        self.lblParamVal.setText('N/A')
        self.lblParamVal.setAlignment(QtCore.Qt.AlignRight)

        hl.addWidget(self.lblParamName)
        hl.addWidget(self.lblParamVal)

        self.slider = QtWidgets.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(99)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        self.slider.valueChanged.connect(self.sliderChanged)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addLayout(hl)
        layout.addWidget(self.slider)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.resize(width,height)


    def drawSafe(self):
        try:
            self.canvas.draw()
        except RuntimeError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(e.strerror)
            msg.setWindowTitle('Runtime Error')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


    def setData(self, p, x, y, z, paramName='Parameter', xlabel=None, ylabel=None, title=None):
        if p is None or p.size == 1:
            self.lblParamName.hide()
            self.lblParamVal.hide()
            self.slider.hide()
        else:
            self.lblParamName.setText(paramName)
            self.lblParamVal.setText('{}'.format(p[0]))
            self.slider.setMaximum(p.size-1)

        self.param = p
        self.x = x
        self.y = y
        self.z = z

        if p is not None:
            self.updatePlot(xlabel=xlabel, ylabel=ylabel, title=title)

    
    def sliderChanged(self):
        i = self.slider.value()
        self.lblParamVal.setText('{}'.format(self.param[i]))

        self.updatePlot()


    def updatePlot(self, xlabel=None, ylabel=None, title=None):
        newAxis = (self.ax is None)
        if newAxis:
            self.ax = self.figure.add_subplot(111)

        i = self.slider.value()
        vmin = 0
        vmax = np.amax(self.z[i,:,:])
        h = self.ax.contourf(self.x, self.y, self.z[i,:,:].T, vmin=0, vmax=vmax)

        if newAxis:
            self.cbar = self.figure.colorbar(h)
        else:
            self.cbar.ax.clear()
            self.cbar = self.figure.colorbar(h, cax=self.cbar.ax)
            """
            self.cbar.set_clim(vmin, vmax)
            self.cbar.set_ticks(np.linspace(vmin, vmax, num=11, endpoint=True))
            self.cbar.draw_all()
            #self.cbar.ax.autoscale_view()
            """

        if xlabel is not None:
            self.ax.set_xlabel(xlabel)
        if ylabel is not None:
            self.ax.set_ylabel(ylabel)
        if title is not None:
            self.ax.set_title(title)


        self.drawSafe()


