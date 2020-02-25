# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/sightlineMappingsView.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SightlineMappingsView(object):
    def setupUi(self, SightlineMappingsView):
        SightlineMappingsView.setObjectName("SightlineMappingsView")
        SightlineMappingsView.resize(510, 655)
        self.verticalLayout = QtWidgets.QVBoxLayout(SightlineMappingsView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(SightlineMappingsView)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnClose = QtWidgets.QPushButton(SightlineMappingsView)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SightlineMappingsView)
        self.btnClose.clicked.connect(SightlineMappingsView.close)
        QtCore.QMetaObject.connectSlotsByName(SightlineMappingsView)

    def retranslateUi(self, SightlineMappingsView):
        _translate = QtCore.QCoreApplication.translate
        SightlineMappingsView.setWindowTitle(_translate("SightlineMappingsView", "Dialog"))
        self.btnClose.setText(_translate("SightlineMappingsView", "Close"))
