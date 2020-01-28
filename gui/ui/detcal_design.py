# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/detcal.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetectorCalibration(object):
    def setupUi(self, DetectorCalibration):
        DetectorCalibration.setObjectName("DetectorCalibration")
        DetectorCalibration.resize(481, 510)
        self.centralwidget = QtWidgets.QWidget(DetectorCalibration)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 111, 28))
        self.label.setObjectName("label")
        self.tbEquilibrium = QtWidgets.QLineEdit(self.centralwidget)
        self.tbEquilibrium.setGeometry(QtCore.QRect(120, 20, 271, 28))
        self.tbEquilibrium.setObjectName("tbEquilibrium")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 91, 28))
        self.label_2.setObjectName("label_2")
        self.tbImage = QtWidgets.QLineEdit(self.centralwidget)
        self.tbImage.setGeometry(QtCore.QRect(120, 50, 271, 28))
        self.tbImage.setObjectName("tbImage")
        self.btnBrowseEq = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowseEq.setGeometry(QtCore.QRect(390, 20, 84, 28))
        self.btnBrowseEq.setObjectName("btnBrowseEq")
        self.btnBrowseImage = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowseImage.setGeometry(QtCore.QRect(390, 50, 84, 28))
        self.btnBrowseImage.setObjectName("btnBrowseImage")
        self.gbDetector = QtWidgets.QGroupBox(self.centralwidget)
        self.gbDetector.setGeometry(QtCore.QRect(10, 90, 461, 221))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbDetector.setFont(font)
        self.gbDetector.setObjectName("gbDetector")
        self.label_3 = QtWidgets.QLabel(self.gbDetector)
        self.label_3.setGeometry(QtCore.QRect(250, 30, 21, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.gbDetector)
        self.label_4.setGeometry(QtCore.QRect(330, 30, 21, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.gbDetector)
        self.label_5.setGeometry(QtCore.QRect(410, 30, 21, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.tbPosX = QtWidgets.QLineEdit(self.gbDetector)
        self.tbPosX.setGeometry(QtCore.QRect(220, 50, 71, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbPosX.setFont(font)
        self.tbPosX.setObjectName("tbPosX")
        self.tbPosY = QtWidgets.QLineEdit(self.gbDetector)
        self.tbPosY.setGeometry(QtCore.QRect(300, 50, 71, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbPosY.setFont(font)
        self.tbPosY.setObjectName("tbPosY")
        self.tbPosZ = QtWidgets.QLineEdit(self.gbDetector)
        self.tbPosZ.setGeometry(QtCore.QRect(380, 50, 71, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbPosZ.setFont(font)
        self.tbPosZ.setObjectName("tbPosZ")
        self.tbDirX = QtWidgets.QLineEdit(self.gbDetector)
        self.tbDirX.setGeometry(QtCore.QRect(220, 80, 71, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbDirX.setFont(font)
        self.tbDirX.setObjectName("tbDirX")
        self.tbDirZ = QtWidgets.QLineEdit(self.gbDetector)
        self.tbDirZ.setGeometry(QtCore.QRect(380, 80, 71, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbDirZ.setFont(font)
        self.tbDirZ.setObjectName("tbDirZ")
        self.tbDirY = QtWidgets.QLineEdit(self.gbDetector)
        self.tbDirY.setGeometry(QtCore.QRect(300, 80, 71, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbDirY.setFont(font)
        self.tbDirY.setObjectName("tbDirY")
        self.label_6 = QtWidgets.QLabel(self.gbDetector)
        self.label_6.setGeometry(QtCore.QRect(10, 50, 131, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.gbDetector)
        self.label_7.setGeometry(QtCore.QRect(10, 80, 191, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.gbDetector)
        self.label_8.setGeometry(QtCore.QRect(10, 110, 141, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.tbVisang = QtWidgets.QLineEdit(self.gbDetector)
        self.tbVisang.setGeometry(QtCore.QRect(220, 110, 151, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbVisang.setFont(font)
        self.tbVisang.setObjectName("tbVisang")
        self.label_9 = QtWidgets.QLabel(self.gbDetector)
        self.label_9.setGeometry(QtCore.QRect(380, 110, 63, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.gbDetector)
        self.label_10.setGeometry(QtCore.QRect(10, 140, 151, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.tbTilt = QtWidgets.QLineEdit(self.gbDetector)
        self.tbTilt.setGeometry(QtCore.QRect(220, 140, 151, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tbTilt.setFont(font)
        self.tbTilt.setObjectName("tbTilt")
        self.label_11 = QtWidgets.QLabel(self.gbDetector)
        self.label_11.setGeometry(QtCore.QRect(380, 140, 63, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.btnRedraw = QtWidgets.QPushButton(self.gbDetector)
        self.btnRedraw.setGeometry(QtCore.QRect(370, 180, 84, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnRedraw.setFont(font)
        self.btnRedraw.setObjectName("btnRedraw")
        self.gbOverlay = QtWidgets.QGroupBox(self.centralwidget)
        self.gbOverlay.setGeometry(QtCore.QRect(10, 320, 461, 141))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbOverlay.setFont(font)
        self.gbOverlay.setObjectName("gbOverlay")
        self.lblTor270 = QtWidgets.QLabel(self.gbOverlay)
        self.lblTor270.setGeometry(QtCore.QRect(324, 70, 41, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lblTor270.setFont(font)
        self.lblTor270.setObjectName("lblTor270")
        self.lblTor90 = QtWidgets.QLabel(self.gbOverlay)
        self.lblTor90.setGeometry(QtCore.QRect(115, 70, 31, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lblTor90.setFont(font)
        self.lblTor90.setObjectName("lblTor90")
        self.lblToroidal = QtWidgets.QLabel(self.gbOverlay)
        self.lblToroidal.setGeometry(QtCore.QRect(10, 25, 141, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lblToroidal.setFont(font)
        self.lblToroidal.setObjectName("lblToroidal")
        self.lblTor360 = QtWidgets.QLabel(self.gbOverlay)
        self.lblTor360.setGeometry(QtCore.QRect(420, 70, 41, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lblTor360.setFont(font)
        self.lblTor360.setObjectName("lblTor360")
        self.lblTor180 = QtWidgets.QLabel(self.gbOverlay)
        self.lblTor180.setGeometry(QtCore.QRect(215, 70, 41, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lblTor180.setFont(font)
        self.lblTor180.setObjectName("lblTor180")
        self.lblTor0 = QtWidgets.QLabel(self.gbOverlay)
        self.lblTor0.setGeometry(QtCore.QRect(10, 70, 67, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lblTor0.setFont(font)
        self.lblTor0.setObjectName("lblTor0")
        self.sliderToroidal = QtWidgets.QSlider(self.gbOverlay)
        self.sliderToroidal.setGeometry(QtCore.QRect(10, 45, 441, 24))
        self.sliderToroidal.setMaximum(360)
        self.sliderToroidal.setProperty("value", 0)
        self.sliderToroidal.setOrientation(QtCore.Qt.Horizontal)
        self.sliderToroidal.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderToroidal.setTickInterval(15)
        self.sliderToroidal.setObjectName("sliderToroidal")
        self.cbColor = QtWidgets.QComboBox(self.gbOverlay)
        self.cbColor.setGeometry(QtCore.QRect(70, 105, 141, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbColor.setFont(font)
        self.cbColor.setObjectName("cbColor")
        self.label_12 = QtWidgets.QLabel(self.gbOverlay)
        self.label_12.setGeometry(QtCore.QRect(10, 110, 67, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.gbOverlay)
        self.label_13.setGeometry(QtCore.QRect(230, 110, 81, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.dsbLinewidth = QtWidgets.QDoubleSpinBox(self.gbOverlay)
        self.dsbLinewidth.setGeometry(QtCore.QRect(320, 105, 131, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dsbLinewidth.setFont(font)
        self.dsbLinewidth.setDecimals(1)
        self.dsbLinewidth.setMinimum(0.5)
        self.dsbLinewidth.setMaximum(10.0)
        self.dsbLinewidth.setProperty("value", 2.0)
        self.dsbLinewidth.setObjectName("dsbLinewidth")
        DetectorCalibration.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DetectorCalibration)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 481, 22))
        self.menubar.setObjectName("menubar")
        DetectorCalibration.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DetectorCalibration)
        self.statusbar.setObjectName("statusbar")
        DetectorCalibration.setStatusBar(self.statusbar)

        self.retranslateUi(DetectorCalibration)
        QtCore.QMetaObject.connectSlotsByName(DetectorCalibration)

    def retranslateUi(self, DetectorCalibration):
        _translate = QtCore.QCoreApplication.translate
        DetectorCalibration.setWindowTitle(_translate("DetectorCalibration", "Detector Calibration Tool"))
        self.label.setText(_translate("DetectorCalibration", "Equilibrium file:"))
        self.label_2.setText(_translate("DetectorCalibration", "Image file:"))
        self.btnBrowseEq.setText(_translate("DetectorCalibration", "Browse..."))
        self.btnBrowseImage.setText(_translate("DetectorCalibration", "Browse..."))
        self.gbDetector.setTitle(_translate("DetectorCalibration", "Detector properties"))
        self.label_3.setText(_translate("DetectorCalibration", "X"))
        self.label_4.setText(_translate("DetectorCalibration", "Y"))
        self.label_5.setText(_translate("DetectorCalibration", "Z"))
        self.tbPosX.setText(_translate("DetectorCalibration", "0"))
        self.tbPosY.setText(_translate("DetectorCalibration", "0"))
        self.tbPosZ.setText(_translate("DetectorCalibration", "0"))
        self.tbDirX.setText(_translate("DetectorCalibration", "0"))
        self.tbDirZ.setText(_translate("DetectorCalibration", "0"))
        self.tbDirY.setText(_translate("DetectorCalibration", "1"))
        self.label_6.setText(_translate("DetectorCalibration", "Position:"))
        self.label_7.setText(_translate("DetectorCalibration", "Viewing direction:"))
        self.label_8.setText(_translate("DetectorCalibration", "Vision angle:"))
        self.tbVisang.setText(_translate("DetectorCalibration", "1"))
        self.label_9.setText(_translate("DetectorCalibration", "rad"))
        self.label_10.setText(_translate("DetectorCalibration", "CW tilt:"))
        self.tbTilt.setText(_translate("DetectorCalibration", "0"))
        self.label_11.setText(_translate("DetectorCalibration", "rad"))
        self.btnRedraw.setText(_translate("DetectorCalibration", "Redraw"))
        self.gbOverlay.setTitle(_translate("DetectorCalibration", "Overlay properties"))
        self.lblTor270.setText(_translate("DetectorCalibration", "270º"))
        self.lblTor90.setText(_translate("DetectorCalibration", "90º"))
        self.lblToroidal.setText(_translate("DetectorCalibration", "Wall toroidal offset"))
        self.lblTor360.setText(_translate("DetectorCalibration", "360º"))
        self.lblTor180.setText(_translate("DetectorCalibration", "180º"))
        self.lblTor0.setText(_translate("DetectorCalibration", "0º"))
        self.label_12.setText(_translate("DetectorCalibration", "Color:"))
        self.label_13.setText(_translate("DetectorCalibration", "Linewidth:"))


