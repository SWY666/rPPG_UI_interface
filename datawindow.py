# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'datawindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1031, 792)
        Dialog.setMinimumSize(QtCore.QSize(1031, 792))
        Dialog.setMaximumSize(QtCore.QSize(1920, 1080))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setMinimumSize(QtCore.QSize(500, 250))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(500, 250))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout.addWidget(self.groupBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setMinimumSize(QtCore.QSize(500, 250))
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_5.setMinimumSize(QtCore.QSize(500, 250))
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setMinimumSize(QtCore.QSize(450, 450))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout.addWidget(self.groupBox_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_2.setTitle(_translate("Dialog", "带通滤波后波形(按秒)"))
        self.groupBox.setTitle(_translate("Dialog", "小波变换后波形(按秒)"))
        self.groupBox_4.setTitle(_translate("Dialog", "原始波形(按帧)"))
        self.groupBox_5.setTitle(_translate("Dialog", "count"))
        self.groupBox_3.setTitle(_translate("Dialog", "小波变换后的小波基图（纵轴频率，横轴秒）"))

