# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/sightlineMappings.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SightlineMappings(object):
    def setupUi(self, SightlineMappings):
        SightlineMappings.setObjectName("SightlineMappings")
        SightlineMappings.resize(666, 450)
        self.verticalLayout = QtWidgets.QVBoxLayout(SightlineMappings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetPlot = QtWidgets.QWidget(SightlineMappings)
        self.widgetPlot.setObjectName("widgetPlot")
        self.verticalLayout.addWidget(self.widgetPlot)
        self.groupBox = QtWidgets.QGroupBox(SightlineMappings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(140, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btnBrowse = QtWidgets.QPushButton(self.groupBox)
        self.btnBrowse.setObjectName("btnBrowse")
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnCalc = QtWidgets.QPushButton(self.groupBox)
        self.btnCalc.setObjectName("btnCalc")
        self.horizontalLayout_2.addWidget(self.btnCalc)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnSave = QtWidgets.QPushButton(self.groupBox)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_3.addWidget(self.btnSave)
        self.btnPlotXS = QtWidgets.QPushButton(self.groupBox)
        self.btnPlotXS.setObjectName("btnPlotXS")
        self.horizontalLayout_3.addWidget(self.btnPlotXS)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btnClose = QtWidgets.QPushButton(SightlineMappings)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout_4.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(SightlineMappings)
        self.btnClose.clicked.connect(SightlineMappings.close)
        QtCore.QMetaObject.connectSlotsByName(SightlineMappings)

    def retranslateUi(self, SightlineMappings):
        _translate = QtCore.QCoreApplication.translate
        SightlineMappings.setWindowTitle(_translate("SightlineMappings", "Sightline mappings"))
        self.groupBox.setTitle(_translate("SightlineMappings", "Sightline mappings"))
        self.label.setText(_translate("SightlineMappings", "Geometry file:"))
        self.btnBrowse.setText(_translate("SightlineMappings", "Browse..."))
        self.btnCalc.setText(_translate("SightlineMappings", "Calculate radial mapping"))
        self.btnSave.setText(_translate("SightlineMappings", "Save radial mapping"))
        self.btnPlotXS.setText(_translate("SightlineMappings", "Plot over cross-section"))
        self.btnClose.setText(_translate("SightlineMappings", "Close"))
