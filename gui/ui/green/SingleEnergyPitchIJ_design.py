# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/green/SingleEnergyPitchIJ.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SingleEnergyPitchIJ(object):
    def setupUi(self, SingleEnergyPitchIJ):
        SingleEnergyPitchIJ.setObjectName("SingleEnergyPitchIJ")
        SingleEnergyPitchIJ.resize(550, 740)
        SingleEnergyPitchIJ.setMinimumSize(QtCore.QSize(550, 740))
        SingleEnergyPitchIJ.setMaximumSize(QtCore.QSize(550, 740))
        self.centralwidget = QtWidgets.QWidget(SingleEnergyPitchIJ)
        self.centralwidget.setObjectName("centralwidget")
        self.sliderEnergy = QtWidgets.QSlider(self.centralwidget)
        self.sliderEnergy.setGeometry(QtCore.QRect(20, 90, 511, 16))
        self.sliderEnergy.setOrientation(QtCore.Qt.Horizontal)
        self.sliderEnergy.setObjectName("sliderEnergy")
        self.lblREEnergy = QtWidgets.QLabel(self.centralwidget)
        self.lblREEnergy.setGeometry(QtCore.QRect(20, 60, 231, 17))
        self.lblREEnergy.setObjectName("lblREEnergy")
        self.lblEnergy = QtWidgets.QLabel(self.centralwidget)
        self.lblEnergy.setGeometry(QtCore.QRect(400, 70, 131, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblEnergy.setFont(font)
        self.lblEnergy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblEnergy.setObjectName("lblEnergy")
        self.lblEnergyMin = QtWidgets.QLabel(self.centralwidget)
        self.lblEnergyMin.setGeometry(QtCore.QRect(20, 110, 67, 17))
        self.lblEnergyMin.setObjectName("lblEnergyMin")
        self.lblEnergyMax = QtWidgets.QLabel(self.centralwidget)
        self.lblEnergyMax.setGeometry(QtCore.QRect(460, 110, 67, 17))
        self.lblEnergyMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblEnergyMax.setObjectName("lblEnergyMax")
        self.widgetDistPlot = QtWidgets.QWidget(self.centralwidget)
        self.widgetDistPlot.setGeometry(QtCore.QRect(10, 170, 531, 271))
        self.widgetDistPlot.setObjectName("widgetDistPlot")
        self.sliderPitchAngle = QtWidgets.QSlider(self.centralwidget)
        self.sliderPitchAngle.setGeometry(QtCore.QRect(20, 490, 511, 16))
        self.sliderPitchAngle.setMinimum(1)
        self.sliderPitchAngle.setMaximum(200)
        self.sliderPitchAngle.setSingleStep(1)
        self.sliderPitchAngle.setProperty("value", 70)
        self.sliderPitchAngle.setOrientation(QtCore.Qt.Horizontal)
        self.sliderPitchAngle.setObjectName("sliderPitchAngle")
        self.lblREPitchAngle = QtWidgets.QLabel(self.centralwidget)
        self.lblREPitchAngle.setGeometry(QtCore.QRect(20, 460, 161, 17))
        self.lblREPitchAngle.setObjectName("lblREPitchAngle")
        self.lblPitchAngleMin = QtWidgets.QLabel(self.centralwidget)
        self.lblPitchAngleMin.setGeometry(QtCore.QRect(20, 510, 67, 17))
        self.lblPitchAngleMin.setObjectName("lblPitchAngleMin")
        self.lblPitchAngleMax = QtWidgets.QLabel(self.centralwidget)
        self.lblPitchAngleMax.setGeometry(QtCore.QRect(460, 510, 67, 17))
        self.lblPitchAngleMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPitchAngleMax.setObjectName("lblPitchAngleMax")
        self.tbFilename = QtWidgets.QLineEdit(self.centralwidget)
        self.tbFilename.setGeometry(QtCore.QRect(20, 30, 431, 25))
        self.tbFilename.setReadOnly(True)
        self.tbFilename.setObjectName("tbFilename")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 10, 121, 17))
        self.label_6.setObjectName("label_6")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(450, 30, 89, 25))
        self.btnBrowse.setObjectName("btnBrowse")
        self.lblPitchAngle = QtWidgets.QLabel(self.centralwidget)
        self.lblPitchAngle.setGeometry(QtCore.QRect(460, 460, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblPitchAngle.setFont(font)
        self.lblPitchAngle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPitchAngle.setObjectName("lblPitchAngle")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 140, 121, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lblDomPitch = QtWidgets.QLabel(self.centralwidget)
        self.lblDomPitch.setGeometry(QtCore.QRect(386, 140, 141, 20))
        self.lblDomPitch.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDomPitch.setObjectName("lblDomPitch")
        self.lblOverlay = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay.setGeometry(QtCore.QRect(20, 590, 67, 17))
        self.lblOverlay.setObjectName("lblOverlay")
        self.tbOverlay = QtWidgets.QLineEdit(self.centralwidget)
        self.tbOverlay.setGeometry(QtCore.QRect(20, 610, 431, 25))
        self.tbOverlay.setReadOnly(True)
        self.tbOverlay.setObjectName("tbOverlay")
        self.btnBrowseOverlay = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowseOverlay.setGeometry(QtCore.QRect(450, 610, 89, 25))
        self.btnBrowseOverlay.setObjectName("btnBrowseOverlay")
        self.sliderOverlay = QtWidgets.QSlider(self.centralwidget)
        self.sliderOverlay.setGeometry(QtCore.QRect(20, 644, 511, 24))
        self.sliderOverlay.setMaximum(100)
        self.sliderOverlay.setProperty("value", 50)
        self.sliderOverlay.setOrientation(QtCore.Qt.Horizontal)
        self.sliderOverlay.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderOverlay.setTickInterval(5)
        self.sliderOverlay.setObjectName("sliderOverlay")
        self.lblOverlayMin = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlayMin.setGeometry(QtCore.QRect(20, 670, 67, 17))
        self.lblOverlayMin.setObjectName("lblOverlayMin")
        self.lblOverlayMax = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlayMax.setGeometry(QtCore.QRect(470, 670, 67, 17))
        self.lblOverlayMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblOverlayMax.setObjectName("lblOverlayMax")
        self.lblOverlay25 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay25.setGeometry(QtCore.QRect(140, 670, 67, 17))
        self.lblOverlay25.setObjectName("lblOverlay25")
        self.lblOverlay50 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay50.setGeometry(QtCore.QRect(262, 670, 67, 17))
        self.lblOverlay50.setObjectName("lblOverlay50")
        self.lblOverlay75 = QtWidgets.QLabel(self.centralwidget)
        self.lblOverlay75.setGeometry(QtCore.QRect(390, 670, 67, 17))
        self.lblOverlay75.setObjectName("lblOverlay75")
        self.btnSaveImage = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveImage.setGeometry(QtCore.QRect(20, 550, 151, 27))
        self.btnSaveImage.setObjectName("btnSaveImage")
        self.btnSaveSuper = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveSuper.setGeometry(QtCore.QRect(390, 550, 151, 27))
        self.btnSaveSuper.setObjectName("btnSaveSuper")
        self.btnSaveBoth = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveBoth.setGeometry(QtCore.QRect(210, 550, 141, 27))
        self.btnSaveBoth.setObjectName("btnSaveBoth")
        SingleEnergyPitchIJ.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SingleEnergyPitchIJ)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 24))
        self.menubar.setObjectName("menubar")
        SingleEnergyPitchIJ.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SingleEnergyPitchIJ)
        self.statusbar.setObjectName("statusbar")
        SingleEnergyPitchIJ.setStatusBar(self.statusbar)

        self.retranslateUi(SingleEnergyPitchIJ)
        QtCore.QMetaObject.connectSlotsByName(SingleEnergyPitchIJ)

    def retranslateUi(self, SingleEnergyPitchIJ):
        _translate = QtCore.QCoreApplication.translate
        SingleEnergyPitchIJ.setWindowTitle(_translate("SingleEnergyPitchIJ", "Single-energy, pitch, image"))
        self.lblREEnergy.setText(_translate("SingleEnergyPitchIJ", "Runaway energy"))
        self.lblEnergy.setText(_translate("SingleEnergyPitchIJ", "N/A"))
        self.lblEnergyMin.setText(_translate("SingleEnergyPitchIJ", "0"))
        self.lblEnergyMax.setText(_translate("SingleEnergyPitchIJ", "∞"))
        self.lblREPitchAngle.setText(_translate("SingleEnergyPitchIJ", "Pitch angle parameter"))
        self.lblPitchAngleMin.setText(_translate("SingleEnergyPitchIJ", "1"))
        self.lblPitchAngleMax.setText(_translate("SingleEnergyPitchIJ", "200"))
        self.label_6.setText(_translate("SingleEnergyPitchIJ", "Green\'s function"))
        self.btnBrowse.setText(_translate("SingleEnergyPitchIJ", "Browse"))
        self.lblPitchAngle.setText(_translate("SingleEnergyPitchIJ", "70"))
        self.label.setText(_translate("SingleEnergyPitchIJ", "Super particle"))
        self.lblDomPitch.setText(_translate("SingleEnergyPitchIJ", "N/A"))
        self.lblOverlay.setText(_translate("SingleEnergyPitchIJ", "Overlay"))
        self.btnBrowseOverlay.setText(_translate("SingleEnergyPitchIJ", "Browse"))
        self.lblOverlayMin.setText(_translate("SingleEnergyPitchIJ", "0%"))
        self.lblOverlayMax.setText(_translate("SingleEnergyPitchIJ", "100%"))
        self.lblOverlay25.setText(_translate("SingleEnergyPitchIJ", "25%"))
        self.lblOverlay50.setText(_translate("SingleEnergyPitchIJ", "50%"))
        self.lblOverlay75.setText(_translate("SingleEnergyPitchIJ", "75%"))
        self.btnSaveImage.setText(_translate("SingleEnergyPitchIJ", "Save image"))
        self.btnSaveSuper.setText(_translate("SingleEnergyPitchIJ", "Save super-particle"))
        self.btnSaveBoth.setText(_translate("SingleEnergyPitchIJ", "Save both"))