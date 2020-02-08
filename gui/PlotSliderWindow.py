
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

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

    def setData(self, p, x, y, z):
        pass

