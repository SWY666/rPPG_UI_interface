# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'heartrate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1144, 912)
        MainWindow.setMinimumSize(QtCore.QSize(980, 780))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.videoshow = QtWidgets.QLabel(self.centralwidget)
        self.videoshow.setMinimumSize(QtCore.QSize(640, 480))
        self.videoshow.setMaximumSize(QtCore.QSize(640, 480))
        self.videoshow.setText("")
        self.videoshow.setObjectName("videoshow")
        self.verticalLayout_2.addWidget(self.videoshow)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.heartrate_time = QtWidgets.QLabel(self.centralwidget)
        self.heartrate_time.setMaximumSize(QtCore.QSize(150, 35))
        self.heartrate_time.setObjectName("heartrate_time")
        self.verticalLayout.addWidget(self.heartrate_time)
        self.heartrate_output = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heartrate_output.sizePolicy().hasHeightForWidth())
        self.heartrate_output.setSizePolicy(sizePolicy)
        self.heartrate_output.setMaximumSize(QtCore.QSize(80, 35))
        self.heartrate_output.setObjectName("heartrate_output")
        self.verticalLayout.addWidget(self.heartrate_output)
        self.on_time_hr_shower = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.on_time_hr_shower.sizePolicy().hasHeightForWidth())
        self.on_time_hr_shower.setSizePolicy(sizePolicy)
        self.on_time_hr_shower.setMaximumSize(QtCore.QSize(80, 35))
        self.on_time_hr_shower.setObjectName("on_time_hr_shower")
        self.verticalLayout.addWidget(self.on_time_hr_shower)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.video_state = QtWidgets.QLabel(self.centralwidget)
        self.video_state.setMaximumSize(QtCore.QSize(100, 35))
        self.video_state.setObjectName("video_state")
        self.verticalLayout.addWidget(self.video_state)
        self.jindu = QtWidgets.QLabel(self.centralwidget)
        self.jindu.setMaximumSize(QtCore.QSize(100, 35))
        self.jindu.setObjectName("jindu")
        self.verticalLayout.addWidget(self.jindu)
        self.jindu2 = QtWidgets.QLabel(self.centralwidget)
        self.jindu2.setMaximumSize(QtCore.QSize(150, 35))
        self.jindu2.setObjectName("jindu2")
        self.verticalLayout.addWidget(self.jindu2)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.Graphs = QtWidgets.QHBoxLayout()
        self.Graphs.setObjectName("Graphs")
        self.hrsheet = QtWidgets.QLabel(self.centralwidget)
        self.hrsheet.setMinimumSize(QtCore.QSize(50, 300))
        self.hrsheet.setMaximumSize(QtCore.QSize(50, 300))
        self.hrsheet.setObjectName("hrsheet")
        self.Graphs.addWidget(self.hrsheet)
        self.verticalLayout_3.addLayout(self.Graphs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1144, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menuBar)
        self.camera_op = QtWidgets.QAction(MainWindow)
        self.camera_op.setCheckable(True)
        self.camera_op.setObjectName("camera_op")
        self.start = QtWidgets.QAction(MainWindow)
        self.start.setObjectName("start")
        self.exit = QtWidgets.QAction(MainWindow)
        self.exit.setObjectName("exit")
        self.video_option = QtWidgets.QAction(MainWindow)
        self.video_option.setObjectName("video_option")
        self.video_cancel = QtWidgets.QAction(MainWindow)
        self.video_cancel.setObjectName("video_cancel")
        self.detail = QtWidgets.QAction(MainWindow)
        self.detail.setObjectName("detail")
        self.menu.addAction(self.start)
        self.menu.addAction(self.exit)
        self.menu.addAction(self.detail)
        self.menu_2.addAction(self.video_option)
        self.menu_2.addAction(self.video_cancel)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "心率波形查看"))
        self.comboBox.setItemText(1, _translate("MainWindow", "疲劳度查看"))
        self.heartrate_time.setText(_translate("MainWindow", "所在时间段"))
        self.heartrate_output.setText(_translate("MainWindow", "心率"))
        self.on_time_hr_shower.setText(_translate("MainWindow", "实时心率"))
        self.video_state.setText(_translate("MainWindow", "视频处理"))
        self.jindu.setText(_translate("MainWindow", "处理进度"))
        self.jindu2.setText(_translate("MainWindow", "视频处理还未开始"))
        self.hrsheet.setText(_translate("MainWindow", "心率"))
        self.menu.setTitle(_translate("MainWindow", "&摄像头操作"))
        self.menu_2.setTitle(_translate("MainWindow", "&视频操作"))
        self.camera_op.setText(_translate("MainWindow", "摄像头操作"))
        self.camera_op.setToolTip(_translate("MainWindow", "摄像头操作"))
        self.camera_op.setShortcut(_translate("MainWindow", "Alt+S"))
        self.start.setText(_translate("MainWindow", "开始"))
        self.start.setShortcut(_translate("MainWindow", "Alt+S"))
        self.exit.setText(_translate("MainWindow", "结束"))
        self.exit.setShortcut(_translate("MainWindow", "Alt+E"))
        self.video_option.setText(_translate("MainWindow", "开始"))
        self.video_option.setShortcut(_translate("MainWindow", "Alt+V"))
        self.video_cancel.setText(_translate("MainWindow", "提前终止"))
        self.video_cancel.setShortcut(_translate("MainWindow", "Alt+C"))
        self.detail.setText(_translate("MainWindow", "展示细节"))
