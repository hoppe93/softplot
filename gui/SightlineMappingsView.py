
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QFileDialog

import numpy as np
import traceback

from ui import sightlineMappingsView_design
from threading import Thread, Event

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from LineOfSightGeometry import LineOfSightGeometry
from MSERadialMapping import MSERadialMapping

class SightlineMappingsView(QtWidgets.QFrame):

    def __init__(self, radiusmap, parent=None):
        super(SightlineMappingsView, self).__init__(parent)

        self.ui = sightlineMappingsView_design.Ui_SightlineMappingsView()
        self.ui.setupUi(self)

        self.ui.tableWidget.setHorizontalHeaderLabels(['Major radius (m)'])
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.ui.tableWidget.setRowCount(radiusmap.size)
        for i in range(0, radiusmap.size):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem('{:.8f}'.format(radiusmap[i])))

        self.bindEvents()

    
    def bindEvents(self):
        pass


    def closeEvent(self, event):
        pass

