# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/distfunc.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DistfuncUI(object):
    def setupUi(self, DistfuncUI):
        DistfuncUI.setObjectName("DistfuncUI")
        DistfuncUI.resize(610, 934)
        self.centralwidget = QtWidgets.QWidget(DistfuncUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lblFileName = QtWidgets.QLabel(self.groupBox)
        self.lblFileName.setObjectName("lblFileName")
        self.horizontalLayout_2.addWidget(self.lblFileName)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.lblDistType = QtWidgets.QLabel(self.groupBox)
        self.lblDistType.setObjectName("lblDistType")
        self.horizontalLayout_3.addWidget(self.lblDistType)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.lblNRadii = QtWidgets.QLabel(self.groupBox)
        self.lblNRadii.setObjectName("lblNRadii")
        self.horizontalLayout_9.addWidget(self.lblNRadii)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_10.addWidget(self.label_12)
        self.lblNMomentum = QtWidgets.QLabel(self.groupBox)
        self.lblNMomentum.setObjectName("lblNMomentum")
        self.horizontalLayout_10.addWidget(self.lblNMomentum)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_12.addWidget(self.label_11)
        self.lblMaxP = QtWidgets.QLabel(self.groupBox)
        self.lblMaxP.setObjectName("lblMaxP")
        self.horizontalLayout_12.addWidget(self.lblMaxP)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.rbDist1D = QtWidgets.QRadioButton(self.groupBox_3)
        self.rbDist1D.setChecked(True)
        self.rbDist1D.setObjectName("rbDist1D")
        self.horizontalLayout_16.addWidget(self.rbDist1D)
        self.rbCumCurrent = QtWidgets.QRadioButton(self.groupBox_3)
        self.rbCumCurrent.setObjectName("rbCumCurrent")
        self.horizontalLayout_16.addWidget(self.rbCumCurrent)
        self.verticalLayout_4.addLayout(self.horizontalLayout_16)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rbDistParPerp = QtWidgets.QRadioButton(self.groupBox_3)
        self.rbDistParPerp.setCheckable(True)
        self.rbDistParPerp.setChecked(False)
        self.rbDistParPerp.setObjectName("rbDistParPerp")
        self.horizontalLayout.addWidget(self.rbDistParPerp)
        self.rbDistPXi = QtWidgets.QRadioButton(self.groupBox_3)
        self.rbDistPXi.setObjectName("rbDistPXi")
        self.horizontalLayout.addWidget(self.rbDistPXi)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.gbMoments = QtWidgets.QGroupBox(self.centralwidget)
        self.gbMoments.setEnabled(False)
        self.gbMoments.setCheckable(True)
        self.gbMoments.setChecked(False)
        self.gbMoments.setObjectName("gbMoments")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.gbMoments)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.cbVolumeElement = QtWidgets.QCheckBox(self.gbMoments)
        self.cbVolumeElement.setChecked(True)
        self.cbVolumeElement.setObjectName("cbVolumeElement")
        self.verticalLayout_5.addWidget(self.cbVolumeElement)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.rbSynchrotron = QtWidgets.QRadioButton(self.gbMoments)
        self.rbSynchrotron.setChecked(True)
        self.rbSynchrotron.setObjectName("rbSynchrotron")
        self.horizontalLayout_8.addWidget(self.rbSynchrotron)
        self.lblSynchB0 = QtWidgets.QLabel(self.gbMoments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSynchB0.sizePolicy().hasHeightForWidth())
        self.lblSynchB0.setSizePolicy(sizePolicy)
        self.lblSynchB0.setObjectName("lblSynchB0")
        self.horizontalLayout_8.addWidget(self.lblSynchB0)
        self.sbSynchMagneticField = QtWidgets.QDoubleSpinBox(self.gbMoments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbSynchMagneticField.sizePolicy().hasHeightForWidth())
        self.sbSynchMagneticField.setSizePolicy(sizePolicy)
        self.sbSynchMagneticField.setSuffix("")
        self.sbSynchMagneticField.setMinimum(0.1)
        self.sbSynchMagneticField.setMaximum(100.0)
        self.sbSynchMagneticField.setSingleStep(0.1)
        self.sbSynchMagneticField.setProperty("value", 3.1)
        self.sbSynchMagneticField.setObjectName("sbSynchMagneticField")
        self.horizontalLayout_8.addWidget(self.sbSynchMagneticField)
        self.lblSynchWavelength = QtWidgets.QLabel(self.gbMoments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSynchWavelength.sizePolicy().hasHeightForWidth())
        self.lblSynchWavelength.setSizePolicy(sizePolicy)
        self.lblSynchWavelength.setObjectName("lblSynchWavelength")
        self.horizontalLayout_8.addWidget(self.lblSynchWavelength)
        self.sbSynchWavelength = QtWidgets.QSpinBox(self.gbMoments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbSynchWavelength.sizePolicy().hasHeightForWidth())
        self.sbSynchWavelength.setSizePolicy(sizePolicy)
        self.sbSynchWavelength.setMinimum(50)
        self.sbSynchWavelength.setMaximum(20000)
        self.sbSynchWavelength.setSingleStep(50)
        self.sbSynchWavelength.setProperty("value", 900)
        self.sbSynchWavelength.setObjectName("sbSynchWavelength")
        self.horizontalLayout_8.addWidget(self.sbSynchWavelength)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.rbRunaway = QtWidgets.QRadioButton(self.gbMoments)
        self.rbRunaway.setObjectName("rbRunaway")
        self.horizontalLayout_14.addWidget(self.rbRunaway)
        self.lblRunawayPc = QtWidgets.QLabel(self.gbMoments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRunawayPc.sizePolicy().hasHeightForWidth())
        self.lblRunawayPc.setSizePolicy(sizePolicy)
        self.lblRunawayPc.setObjectName("lblRunawayPc")
        self.horizontalLayout_14.addWidget(self.lblRunawayPc)
        self.tbRunawayPc = QtWidgets.QLineEdit(self.gbMoments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbRunawayPc.sizePolicy().hasHeightForWidth())
        self.tbRunawayPc.setSizePolicy(sizePolicy)
        self.tbRunawayPc.setObjectName("tbRunawayPc")
        self.horizontalLayout_14.addWidget(self.tbRunawayPc)
        self.verticalLayout_5.addLayout(self.horizontalLayout_14)
        self.verticalLayout.addWidget(self.gbMoments)
        self.btnPlotNow = QtWidgets.QPushButton(self.centralwidget)
        self.btnPlotNow.setObjectName("btnPlotNow")
        self.verticalLayout.addWidget(self.btnPlotNow)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lblRadius = QtWidgets.QLabel(self.centralwidget)
        self.lblRadius.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblRadius.setObjectName("lblRadius")
        self.horizontalLayout_4.addWidget(self.lblRadius)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.sliderRadius = QtWidgets.QSlider(self.centralwidget)
        self.sliderRadius.setOrientation(QtCore.Qt.Horizontal)
        self.sliderRadius.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderRadius.setTickInterval(1)
        self.sliderRadius.setObjectName("sliderRadius")
        self.verticalLayout.addWidget(self.sliderRadius)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tbMinY = QtWidgets.QLineEdit(self.centralwidget)
        self.tbMinY.setObjectName("tbMinY")
        self.horizontalLayout_5.addWidget(self.tbMinY)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.tbMaxY = QtWidgets.QLineEdit(self.centralwidget)
        self.tbMaxY.setObjectName("tbMaxY")
        self.horizontalLayout_5.addWidget(self.tbMaxY)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.btnAutomaticY = QtWidgets.QPushButton(self.centralwidget)
        self.btnAutomaticY.setObjectName("btnAutomaticY")
        self.horizontalLayout_6.addWidget(self.btnAutomaticY)
        self.btnUpdateYAxis = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdateYAxis.setObjectName("btnUpdateYAxis")
        self.horizontalLayout_6.addWidget(self.btnUpdateYAxis)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btnKeepDistribution = QtWidgets.QPushButton(self.groupBox_2)
        self.btnKeepDistribution.setObjectName("btnKeepDistribution")
        self.horizontalLayout_7.addWidget(self.btnKeepDistribution)
        self.btnClearKeptDistributions = QtWidgets.QPushButton(self.groupBox_2)
        self.btnClearKeptDistributions.setObjectName("btnClearKeptDistributions")
        self.horizontalLayout_7.addWidget(self.btnClearKeptDistributions)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.btnPlotRadprof = QtWidgets.QPushButton(self.groupBox_2)
        self.btnPlotRadprof.setObjectName("btnPlotRadprof")
        self.horizontalLayout_11.addWidget(self.btnPlotRadprof)
        self.btnPlotCurrent = QtWidgets.QPushButton(self.groupBox_2)
        self.btnPlotCurrent.setObjectName("btnPlotCurrent")
        self.horizontalLayout_11.addWidget(self.btnPlotCurrent)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.btnMomentProfile = QtWidgets.QPushButton(self.groupBox_2)
        self.btnMomentProfile.setEnabled(False)
        self.btnMomentProfile.setObjectName("btnMomentProfile")
        self.horizontalLayout_13.addWidget(self.btnMomentProfile)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.btnAnalysePitch = QtWidgets.QPushButton(self.groupBox_2)
        self.btnAnalysePitch.setObjectName("btnAnalysePitch")
        self.horizontalLayout_15.addWidget(self.btnAnalysePitch)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        DistfuncUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DistfuncUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 610, 24))
        self.menubar.setObjectName("menubar")
        DistfuncUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DistfuncUI)
        self.statusbar.setObjectName("statusbar")
        DistfuncUI.setStatusBar(self.statusbar)

        self.retranslateUi(DistfuncUI)
        QtCore.QMetaObject.connectSlotsByName(DistfuncUI)

    def retranslateUi(self, DistfuncUI):
        _translate = QtCore.QCoreApplication.translate
        DistfuncUI.setWindowTitle(_translate("DistfuncUI", "Distribution Function Viewer"))
        self.groupBox.setTitle(_translate("DistfuncUI", "Details"))
        self.label_3.setText(_translate("DistfuncUI", "File name:"))
        self.lblFileName.setText(_translate("DistfuncUI", "N/A"))
        self.label_6.setText(_translate("DistfuncUI", "Function type:"))
        self.lblDistType.setText(_translate("DistfuncUI", "N/A"))
        self.label_10.setText(_translate("DistfuncUI", "No. of radial points:"))
        self.lblNRadii.setText(_translate("DistfuncUI", "N/A"))
        self.label_12.setText(_translate("DistfuncUI", "No. of momentum points:"))
        self.lblNMomentum.setText(_translate("DistfuncUI", "N/A"))
        self.label_11.setText(_translate("DistfuncUI", "Maximum momentum:"))
        self.lblMaxP.setText(_translate("DistfuncUI", "N/A"))
        self.groupBox_3.setTitle(_translate("DistfuncUI", "Plot options"))
        self.label_2.setText(_translate("DistfuncUI", "1D distribution function"))
        self.rbDist1D.setText(_translate("DistfuncUI", "Angle-averaged distribution"))
        self.rbCumCurrent.setText(_translate("DistfuncUI", "Cumulative current density"))
        self.label.setText(_translate("DistfuncUI", "2D distribution function"))
        self.rbDistParPerp.setText(_translate("DistfuncUI", "Parallel/perpendicular"))
        self.rbDistPXi.setText(_translate("DistfuncUI", "Momentum/pitch"))
        self.gbMoments.setTitle(_translate("DistfuncUI", "Moments"))
        self.cbVolumeElement.setText(_translate("DistfuncUI", "Momentum-space volume element"))
        self.rbSynchrotron.setText(_translate("DistfuncUI", "Synchrotron"))
        self.lblSynchB0.setText(_translate("DistfuncUI", "B0 (T):"))
        self.lblSynchWavelength.setText(_translate("DistfuncUI", "Wavelength (nm):"))
        self.rbRunaway.setText(_translate("DistfuncUI", "Runaway density"))
        self.lblRunawayPc.setText(_translate("DistfuncUI", "Critical momentum:"))
        self.tbRunawayPc.setText(_translate("DistfuncUI", "1"))
        self.btnPlotNow.setText(_translate("DistfuncUI", "Plot with current settings"))
        self.label_4.setText(_translate("DistfuncUI", "Minor radius (r)"))
        self.lblRadius.setText(_translate("DistfuncUI", "0"))
        self.label_5.setText(_translate("DistfuncUI", "Y-scale"))
        self.tbMinY.setText(_translate("DistfuncUI", "1e-20"))
        self.tbMinY.setPlaceholderText(_translate("DistfuncUI", "Lower limit (e.g. 1e-20)"))
        self.label_7.setText(_translate("DistfuncUI", "to"))
        self.tbMaxY.setText(_translate("DistfuncUI", "1"))
        self.tbMaxY.setPlaceholderText(_translate("DistfuncUI", "Upper limit (i.e. 1)"))
        self.btnAutomaticY.setText(_translate("DistfuncUI", "Set automatically"))
        self.btnUpdateYAxis.setText(_translate("DistfuncUI", "Update axis scale"))
        self.groupBox_2.setTitle(_translate("DistfuncUI", "Tools"))
        self.btnKeepDistribution.setText(_translate("DistfuncUI", "Keep current distribution"))
        self.btnClearKeptDistributions.setText(_translate("DistfuncUI", "Clear kept distributions"))
        self.btnPlotRadprof.setText(_translate("DistfuncUI", "Plot radial density"))
        self.btnPlotCurrent.setText(_translate("DistfuncUI", "Plot current density"))
        self.btnMomentProfile.setText(_translate("DistfuncUI", "Plot profile of selected moment"))
        self.btnAnalysePitch.setText(_translate("DistfuncUI", "Analyse pitch distribution"))
