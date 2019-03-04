# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/green/BeamsizeMeasurement.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BeamsizeMeasurement(object):
    def setupUi(self, BeamsizeMeasurement):
        BeamsizeMeasurement.setObjectName("BeamsizeMeasurement")
        BeamsizeMeasurement.resize(586, 871)
        self.centralwidget = QtWidgets.QWidget(BeamsizeMeasurement)
        self.centralwidget.setObjectName("centralwidget")
        self.tbGreensFunction = QtWidgets.QLineEdit(self.centralwidget)
        self.tbGreensFunction.setGeometry(QtCore.QRect(10, 40, 471, 25))
        self.tbGreensFunction.setReadOnly(True)
        self.tbGreensFunction.setObjectName("tbGreensFunction")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 161, 17))
        self.label.setObjectName("label")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(480, 40, 89, 25))
        self.btnBrowse.setObjectName("btnBrowse")
        self.gbRadialProfile = QtWidgets.QGroupBox(self.centralwidget)
        self.gbRadialProfile.setGeometry(QtCore.QRect(10, 345, 561, 371))
        self.gbRadialProfile.setCheckable(True)
        self.gbRadialProfile.setChecked(False)
        self.gbRadialProfile.setObjectName("gbRadialProfile")
        self.label_24 = QtWidgets.QLabel(self.gbRadialProfile)
        self.label_24.setGeometry(QtCore.QRect(10, 30, 271, 111))
        font = QtGui.QFont()
        font.setFamily("Liberation Mono")
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_24.setObjectName("label_24")
        self.tbRadialProfile = QtWidgets.QPlainTextEdit(self.gbRadialProfile)
        self.tbRadialProfile.setGeometry(QtCore.QRect(290, 30, 261, 101))
        font = QtGui.QFont()
        font.setFamily("Liberation Mono")
        self.tbRadialProfile.setFont(font)
        self.tbRadialProfile.setObjectName("tbRadialProfile")
        self.widgetRadialProfile = QtWidgets.QWidget(self.gbRadialProfile)
        self.widgetRadialProfile.setGeometry(QtCore.QRect(10, 140, 541, 221))
        self.widgetRadialProfile.setObjectName("widgetRadialProfile")
        self.sliderBeamsize = QtWidgets.QSlider(self.centralwidget)
        self.sliderBeamsize.setGeometry(QtCore.QRect(10, 195, 561, 24))
        self.sliderBeamsize.setMaximum(100)
        self.sliderBeamsize.setProperty("value", 100)
        self.sliderBeamsize.setOrientation(QtCore.Qt.Horizontal)
        self.sliderBeamsize.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderBeamsize.setTickInterval(10)
        self.sliderBeamsize.setObjectName("sliderBeamsize")
        self.lblBeamsize_desc = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize_desc.setGeometry(QtCore.QRect(10, 175, 111, 17))
        self.lblBeamsize_desc.setObjectName("lblBeamsize_desc")
        self.lblBeamsize0 = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize0.setGeometry(QtCore.QRect(10, 220, 31, 17))
        self.lblBeamsize0.setObjectName("lblBeamsize0")
        self.lblBeamsize20 = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize20.setGeometry(QtCore.QRect(115, 220, 31, 17))
        self.lblBeamsize20.setObjectName("lblBeamsize20")
        self.lblBeamsize40 = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize40.setGeometry(QtCore.QRect(222, 220, 31, 17))
        self.lblBeamsize40.setObjectName("lblBeamsize40")
        self.lblBeamsize60 = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize60.setGeometry(QtCore.QRect(332, 220, 31, 17))
        self.lblBeamsize60.setObjectName("lblBeamsize60")
        self.lblBeamsize80 = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize80.setGeometry(QtCore.QRect(440, 220, 31, 17))
        self.lblBeamsize80.setObjectName("lblBeamsize80")
        self.lblBeamsize100 = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize100.setGeometry(QtCore.QRect(530, 220, 41, 17))
        self.lblBeamsize100.setObjectName("lblBeamsize100")
        self.lblBeamsize = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamsize.setGeometry(QtCore.QRect(366, 175, 201, 20))
        self.lblBeamsize.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblBeamsize.setObjectName("lblBeamsize")
        self.lblIntensity80 = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity80.setGeometry(QtCore.QRect(438, 295, 31, 17))
        self.lblIntensity80.setObjectName("lblIntensity80")
        self.lblIntensity_desc = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity_desc.setGeometry(QtCore.QRect(8, 250, 221, 17))
        self.lblIntensity_desc.setObjectName("lblIntensity_desc")
        self.lblIntensity100 = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity100.setGeometry(QtCore.QRect(528, 295, 41, 17))
        self.lblIntensity100.setObjectName("lblIntensity100")
        self.lblIntensity40 = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity40.setGeometry(QtCore.QRect(220, 295, 31, 17))
        self.lblIntensity40.setObjectName("lblIntensity40")
        self.lblIntensity = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity.setGeometry(QtCore.QRect(364, 250, 201, 20))
        self.lblIntensity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblIntensity.setObjectName("lblIntensity")
        self.sliderIntensity = QtWidgets.QSlider(self.centralwidget)
        self.sliderIntensity.setGeometry(QtCore.QRect(8, 270, 561, 24))
        self.sliderIntensity.setMinimum(0)
        self.sliderIntensity.setMaximum(100)
        self.sliderIntensity.setProperty("value", 20)
        self.sliderIntensity.setOrientation(QtCore.Qt.Horizontal)
        self.sliderIntensity.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderIntensity.setTickInterval(10)
        self.sliderIntensity.setObjectName("sliderIntensity")
        self.lblIntensity0 = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity0.setGeometry(QtCore.QRect(8, 295, 31, 17))
        self.lblIntensity0.setObjectName("lblIntensity0")
        self.lblIntensity20 = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity20.setGeometry(QtCore.QRect(113, 295, 31, 17))
        self.lblIntensity20.setObjectName("lblIntensity20")
        self.lblIntensity60 = QtWidgets.QLabel(self.centralwidget)
        self.lblIntensity60.setGeometry(QtCore.QRect(330, 295, 31, 17))
        self.lblIntensity60.setObjectName("lblIntensity60")
        self.tbOverlay = QtWidgets.QLineEdit(self.centralwidget)
        self.tbOverlay.setGeometry(QtCore.QRect(10, 745, 471, 25))
        self.tbOverlay.setReadOnly(True)
        self.tbOverlay.setObjectName("tbOverlay")
        self.btnBrowseOverlay = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowseOverlay.setGeometry(QtCore.QRect(480, 745, 89, 25))
        self.btnBrowseOverlay.setObjectName("btnBrowseOverlay")
        self.lblOverlay_desc = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay_desc.setGeometry(QtCore.QRect(10, 725, 67, 17))
        self.lblOverlay_desc.setObjectName("lblOverlay_desc")
        self.sliderOverlay = QtWidgets.QSlider(self.centralwidget)
        self.sliderOverlay.setGeometry(QtCore.QRect(10, 785, 561, 24))
        self.sliderOverlay.setMaximum(100)
        self.sliderOverlay.setProperty("value", 25)
        self.sliderOverlay.setOrientation(QtCore.Qt.Horizontal)
        self.sliderOverlay.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderOverlay.setTickInterval(10)
        self.sliderOverlay.setObjectName("sliderOverlay")
        self.lblOverlay40 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay40.setGeometry(QtCore.QRect(222, 810, 31, 17))
        self.lblOverlay40.setObjectName("lblOverlay40")
        self.lblOverlay0 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay0.setGeometry(QtCore.QRect(10, 810, 31, 17))
        self.lblOverlay0.setObjectName("lblOverlay0")
        self.lblOverlay60 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay60.setGeometry(QtCore.QRect(332, 810, 31, 17))
        self.lblOverlay60.setObjectName("lblOverlay60")
        self.lblOverlay20 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay20.setGeometry(QtCore.QRect(115, 810, 31, 17))
        self.lblOverlay20.setObjectName("lblOverlay20")
        self.lblOverlay100 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay100.setGeometry(QtCore.QRect(530, 810, 41, 17))
        self.lblOverlay100.setObjectName("lblOverlay100")
        self.lblOverlay80 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay80.setGeometry(QtCore.QRect(440, 810, 31, 17))
        self.lblOverlay80.setObjectName("lblOverlay80")
        self.lblBeamRadius = QtWidgets.QLabel(self.centralwidget)
        self.lblBeamRadius.setGeometry(QtCore.QRect(10, 80, 561, 71))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.lblBeamRadius.setFont(font)
        self.lblBeamRadius.setAlignment(QtCore.Qt.AlignCenter)
        self.lblBeamRadius.setObjectName("lblBeamRadius")
        BeamsizeMeasurement.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BeamsizeMeasurement)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 586, 22))
        self.menubar.setObjectName("menubar")
        BeamsizeMeasurement.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BeamsizeMeasurement)
        self.statusbar.setObjectName("statusbar")
        BeamsizeMeasurement.setStatusBar(self.statusbar)

        self.retranslateUi(BeamsizeMeasurement)
        QtCore.QMetaObject.connectSlotsByName(BeamsizeMeasurement)

    def retranslateUi(self, BeamsizeMeasurement):
        _translate = QtCore.QCoreApplication.translate
        BeamsizeMeasurement.setWindowTitle(_translate("BeamsizeMeasurement", "Beam size measurement"))
        self.label.setText(_translate("BeamsizeMeasurement", "Green\'s function:"))
        self.btnBrowse.setText(_translate("BeamsizeMeasurement", "Browse"))
        self.gbRadialProfile.setTitle(_translate("BeamsizeMeasurement", "Full radial profile"))
        self.label_24.setText(_translate("BeamsizeMeasurement", "<html><head/><body><p>Negative profile values are<br/>interpreted as zero.</p><p>x &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = Normalized radius<br/>THETA(a)&nbsp; = 0 if x &gt; a<br/>iTHETA(a) = 0 if x &lt; a</p></body></html>"))
        self.tbRadialProfile.setPlaceholderText(_translate("BeamsizeMeasurement", "Python (numpy) expression"))
        self.lblBeamsize_desc.setText(_translate("BeamsizeMeasurement", "Beam size"))
        self.lblBeamsize0.setText(_translate("BeamsizeMeasurement", "0%"))
        self.lblBeamsize20.setText(_translate("BeamsizeMeasurement", "20%"))
        self.lblBeamsize40.setText(_translate("BeamsizeMeasurement", "40%"))
        self.lblBeamsize60.setText(_translate("BeamsizeMeasurement", "60%"))
        self.lblBeamsize80.setText(_translate("BeamsizeMeasurement", "80%"))
        self.lblBeamsize100.setText(_translate("BeamsizeMeasurement", "100%"))
        self.lblBeamsize.setText(_translate("BeamsizeMeasurement", "100%"))
        self.lblIntensity80.setText(_translate("BeamsizeMeasurement", "80%"))
        self.lblIntensity_desc.setText(_translate("BeamsizeMeasurement", "Intensity threshold"))
        self.lblIntensity100.setText(_translate("BeamsizeMeasurement", "100%"))
        self.lblIntensity40.setText(_translate("BeamsizeMeasurement", "40%"))
        self.lblIntensity.setText(_translate("BeamsizeMeasurement", "0%"))
        self.lblIntensity0.setText(_translate("BeamsizeMeasurement", "0%"))
        self.lblIntensity20.setText(_translate("BeamsizeMeasurement", "20%"))
        self.lblIntensity60.setText(_translate("BeamsizeMeasurement", "60%"))
        self.btnBrowseOverlay.setText(_translate("BeamsizeMeasurement", "Browse"))
        self.lblOverlay_desc.setText(_translate("BeamsizeMeasurement", "Overlay:"))
        self.lblOverlay40.setText(_translate("BeamsizeMeasurement", "40%"))
        self.lblOverlay0.setText(_translate("BeamsizeMeasurement", "0%"))
        self.lblOverlay60.setText(_translate("BeamsizeMeasurement", "60%"))
        self.lblOverlay20.setText(_translate("BeamsizeMeasurement", "20%"))
        self.lblOverlay100.setText(_translate("BeamsizeMeasurement", "100%"))
        self.lblOverlay80.setText(_translate("BeamsizeMeasurement", "80%"))
        self.lblBeamRadius.setText(_translate("BeamsizeMeasurement", "N/A"))

