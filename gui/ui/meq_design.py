# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/meq.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MeqWindow(object):
    def setupUi(self, MeqWindow):
        MeqWindow.setObjectName("MeqWindow")
        MeqWindow.resize(635, 857)
        self.centralwidget = QtWidgets.QWidget(MeqWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tbMeqFile = QtWidgets.QLineEdit(self.centralwidget)
        self.tbMeqFile.setGeometry(QtCore.QRect(190, 20, 351, 28))
        self.tbMeqFile.setObjectName("tbMeqFile")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 171, 28))
        self.label.setObjectName("label")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(540, 20, 84, 28))
        self.btnBrowse.setObjectName("btnBrowse")
        self.gbMetadata = QtWidgets.QGroupBox(self.centralwidget)
        self.gbMetadata.setEnabled(False)
        self.gbMetadata.setGeometry(QtCore.QRect(10, 60, 611, 381))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbMetadata.setFont(font)
        self.gbMetadata.setObjectName("gbMetadata")
        self.tbName = QtWidgets.QLineEdit(self.gbMetadata)
        self.tbName.setGeometry(QtCore.QRect(60, 40, 541, 28))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setBold(False)
        font.setWeight(50)
        self.tbName.setFont(font)
        self.tbName.setObjectName("tbName")
        self.label_2 = QtWidgets.QLabel(self.gbMetadata)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 51, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tbDescription = QtWidgets.QPlainTextEdit(self.gbMetadata)
        self.tbDescription.setGeometry(QtCore.QRect(10, 100, 591, 271))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.tbDescription.setFont(font)
        self.tbDescription.setPlainText("")
        self.tbDescription.setObjectName("tbDescription")
        self.label_3 = QtWidgets.QLabel(self.gbMetadata)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 91, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.btnSaveMetadata = QtWidgets.QPushButton(self.gbMetadata)
        self.btnSaveMetadata.setEnabled(False)
        self.btnSaveMetadata.setGeometry(QtCore.QRect(470, 70, 131, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSaveMetadata.setFont(font)
        self.btnSaveMetadata.setObjectName("btnSaveMetadata")
        self.gbPlot = QtWidgets.QGroupBox(self.centralwidget)
        self.gbPlot.setEnabled(False)
        self.gbPlot.setGeometry(QtCore.QRect(10, 450, 301, 241))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbPlot.setFont(font)
        self.gbPlot.setObjectName("gbPlot")
        self.cbBphi = QtWidgets.QCheckBox(self.gbPlot)
        self.cbBphi.setGeometry(QtCore.QRect(10, 50, 281, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbBphi.setFont(font)
        self.cbBphi.setObjectName("cbBphi")
        self.cbBr = QtWidgets.QCheckBox(self.gbPlot)
        self.cbBr.setGeometry(QtCore.QRect(10, 70, 131, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbBr.setFont(font)
        self.cbBr.setChecked(False)
        self.cbBr.setObjectName("cbBr")
        self.cbBz = QtWidgets.QCheckBox(self.gbPlot)
        self.cbBz.setGeometry(QtCore.QRect(10, 90, 171, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbBz.setFont(font)
        self.cbBz.setChecked(False)
        self.cbBz.setObjectName("cbBz")
        self.label_7 = QtWidgets.QLabel(self.gbPlot)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 121, 20))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.gbPlot)
        self.label_8.setGeometry(QtCore.QRect(10, 120, 81, 20))
        self.label_8.setObjectName("label_8")
        self.cbWall = QtWidgets.QCheckBox(self.gbPlot)
        self.cbWall.setGeometry(QtCore.QRect(10, 140, 271, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbWall.setFont(font)
        self.cbWall.setChecked(True)
        self.cbWall.setObjectName("cbWall")
        self.cbSeparatrix = QtWidgets.QCheckBox(self.gbPlot)
        self.cbSeparatrix.setGeometry(QtCore.QRect(10, 160, 91, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbSeparatrix.setFont(font)
        self.cbSeparatrix.setChecked(True)
        self.cbSeparatrix.setObjectName("cbSeparatrix")
        self.cbFlux = QtWidgets.QCheckBox(self.gbPlot)
        self.cbFlux.setGeometry(QtCore.QRect(10, 180, 131, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbFlux.setFont(font)
        self.cbFlux.setChecked(True)
        self.cbFlux.setObjectName("cbFlux")
        self.cbMaxis = QtWidgets.QCheckBox(self.gbPlot)
        self.cbMaxis.setGeometry(QtCore.QRect(10, 200, 141, 26))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbMaxis.setFont(font)
        self.cbMaxis.setChecked(True)
        self.cbMaxis.setObjectName("cbMaxis")
        self.lblMaxis = QtWidgets.QLabel(self.gbPlot)
        self.lblMaxis.setGeometry(QtCore.QRect(140, 200, 151, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lblMaxis.setFont(font)
        self.lblMaxis.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblMaxis.setObjectName("lblMaxis")
        self.gbOrbits = QtWidgets.QGroupBox(self.centralwidget)
        self.gbOrbits.setEnabled(False)
        self.gbOrbits.setGeometry(QtCore.QRect(320, 450, 301, 281))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gbOrbits.setFont(font)
        self.gbOrbits.setObjectName("gbOrbits")
        self.btnClearOrbits = QtWidgets.QPushButton(self.gbOrbits)
        self.btnClearOrbits.setGeometry(QtCore.QRect(10, 240, 281, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnClearOrbits.setFont(font)
        self.btnClearOrbits.setObjectName("btnClearOrbits")
        self.btnGCOrbit = QtWidgets.QPushButton(self.gbOrbits)
        self.btnGCOrbit.setGeometry(QtCore.QRect(10, 30, 281, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnGCOrbit.setFont(font)
        self.btnGCOrbit.setObjectName("btnGCOrbit")
        self.btnParticleOrbit = QtWidgets.QPushButton(self.gbOrbits)
        self.btnParticleOrbit.setGeometry(QtCore.QRect(10, 60, 281, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnParticleOrbit.setFont(font)
        self.btnParticleOrbit.setObjectName("btnParticleOrbit")
        self.label_4 = QtWidgets.QLabel(self.gbOrbits)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 131, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.gbOrbits)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 141, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.gbOrbits)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 131, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.dsbRadius = QtWidgets.QDoubleSpinBox(self.gbOrbits)
        self.dsbRadius.setGeometry(QtCore.QRect(160, 100, 131, 29))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dsbRadius.setFont(font)
        self.dsbRadius.setDecimals(3)
        self.dsbRadius.setSingleStep(0.01)
        self.dsbRadius.setObjectName("dsbRadius")
        self.dsbMomentum = QtWidgets.QDoubleSpinBox(self.gbOrbits)
        self.dsbMomentum.setGeometry(QtCore.QRect(160, 130, 131, 29))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dsbMomentum.setFont(font)
        self.dsbMomentum.setMinimum(0.1)
        self.dsbMomentum.setProperty("value", 15.0)
        self.dsbMomentum.setObjectName("dsbMomentum")
        self.dsbPitch = QtWidgets.QDoubleSpinBox(self.gbOrbits)
        self.dsbPitch.setGeometry(QtCore.QRect(160, 160, 131, 29))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dsbPitch.setFont(font)
        self.dsbPitch.setDecimals(3)
        self.dsbPitch.setMaximum(1.56)
        self.dsbPitch.setSingleStep(0.01)
        self.dsbPitch.setProperty("value", 0.1)
        self.dsbPitch.setObjectName("dsbPitch")
        self.cbReverseOrbit = QtWidgets.QCheckBox(self.gbOrbits)
        self.cbReverseOrbit.setGeometry(QtCore.QRect(10, 190, 281, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cbReverseOrbit.setFont(font)
        self.cbReverseOrbit.setObjectName("cbReverseOrbit")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 780, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 700, 63, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 720, 63, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 740, 111, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.lblBComp = QtWidgets.QLabel(self.centralwidget)
        self.lblBComp.setGeometry(QtCore.QRect(130, 740, 491, 20))
        self.lblBComp.setObjectName("lblBComp")
        self.lblBStrength = QtWidgets.QLabel(self.centralwidget)
        self.lblBStrength.setGeometry(QtCore.QRect(130, 720, 491, 20))
        self.lblBStrength.setObjectName("lblBStrength")
        self.lblSampledB = QtWidgets.QLabel(self.centralwidget)
        self.lblSampledB.setGeometry(QtCore.QRect(130, 700, 481, 20))
        self.lblSampledB.setObjectName("lblSampledB")
        MeqWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MeqWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 635, 22))
        self.menubar.setObjectName("menubar")
        MeqWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MeqWindow)
        self.statusbar.setObjectName("statusbar")
        MeqWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MeqWindow)
        QtCore.QMetaObject.connectSlotsByName(MeqWindow)

    def retranslateUi(self, MeqWindow):
        _translate = QtCore.QCoreApplication.translate
        MeqWindow.setWindowTitle(_translate("MeqWindow", "SOFT Magnetic Equilibrium Viewier"))
        self.label.setText(_translate("MeqWindow", "Magnetic Equilibrium File:"))
        self.btnBrowse.setText(_translate("MeqWindow", "Browse..."))
        self.gbMetadata.setTitle(_translate("MeqWindow", "Metadata"))
        self.tbName.setPlaceholderText(_translate("MeqWindow", "Name of magnetic equilibrium"))
        self.label_2.setText(_translate("MeqWindow", "Name:"))
        self.tbDescription.setPlaceholderText(_translate("MeqWindow", "Description of magnetic equilibrium"))
        self.label_3.setText(_translate("MeqWindow", "Description:"))
        self.btnSaveMetadata.setText(_translate("MeqWindow", "Save metadata"))
        self.gbPlot.setTitle(_translate("MeqWindow", "Plot"))
        self.cbBphi.setText(_translate("MeqWindow", "Toroidal field (Bphi)"))
        self.cbBr.setText(_translate("MeqWindow", "Radial field (Br)"))
        self.cbBz.setText(_translate("MeqWindow", "Vertical field (Bz)"))
        self.label_7.setText(_translate("MeqWindow", "Magnetic fields"))
        self.label_8.setText(_translate("MeqWindow", "Overlays"))
        self.cbWall.setText(_translate("MeqWindow", "Vacuum vessel"))
        self.cbSeparatrix.setText(_translate("MeqWindow", "Separatrix"))
        self.cbFlux.setText(_translate("MeqWindow", "Flux surfaces"))
        self.cbMaxis.setText(_translate("MeqWindow", "Magnetic axis"))
        self.lblMaxis.setText(_translate("MeqWindow", "(?, ?)"))
        self.gbOrbits.setTitle(_translate("MeqWindow", "Runaway Electron Orbits"))
        self.btnClearOrbits.setText(_translate("MeqWindow", "Clear"))
        self.btnGCOrbit.setText(_translate("MeqWindow", "Guiding-center orbit"))
        self.btnParticleOrbit.setText(_translate("MeqWindow", "Particle orbit"))
        self.label_4.setText(_translate("MeqWindow", "Radial position (m):"))
        self.label_5.setText(_translate("MeqWindow", "Momentum (MeV/c):"))
        self.label_6.setText(_translate("MeqWindow", "Pitch angle (rad):"))
        self.cbReverseOrbit.setText(_translate("MeqWindow", "Reverse current direction"))
        self.label_9.setText(_translate("MeqWindow", "Click on plot to get magnetic field strength!"))
        self.label_10.setText(_translate("MeqWindow", "(R,Z) ="))
        self.label_11.setText(_translate("MeqWindow", "B = "))
        self.label_12.setText(_translate("MeqWindow", "(Br, Bphi, Bz) ="))
        self.lblBComp.setText(_translate("MeqWindow", "(0, 0, 0) T"))
        self.lblBStrength.setText(_translate("MeqWindow", "0 T"))
        self.lblSampledB.setText(_translate("MeqWindow", "(0, 0) m"))

