# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/hn/Desktop/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(763, 267)
        MainWindow.setStyleSheet("QPushButton{\n"
"    color: green;\n"
"    background-color: white;\n"
"    border-style: solid;\n"
"    border-width:1px;\n"
"    border-radius:50px;\n"
"    border-color: green;\n"
"    max-width:100px;\n"
"    max-height:100px;\n"
"    min-width:100px;\n"
"    min-height:100px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton[stay=true]{\n"
"    color: white;\n"
"    background-color: green;\n"
"}\n"
"QPushButton:released{\n"
"    background-color: red;\n"
"}\n"
"\n"
"\n"
"#pushButtonStop{\n"
"    color: red;\n"
"    background-color: white;\n"
"    border-color: red;\n"
"}\n"
"\n"
"#pushButtonStop:pressed, #pushButtonStop[stay=true]{\n"
"    color: white;\n"
"    background-color: red;\n"
"}\n"
"\n"
"")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonReverse = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonReverse.setEnabled(True)
        self.pushButtonReverse.setStyleSheet("")
        self.pushButtonReverse.setObjectName("pushButtonReverse")
        self.gridLayout.addWidget(self.pushButtonReverse, 2, 2, 1, 1)
        self.comboBoxTargetDevice = QtWidgets.QComboBox(self.centralWidget)
        self.comboBoxTargetDevice.setStyleSheet("max-width: 200px;")
        self.comboBoxTargetDevice.setObjectName("comboBoxTargetDevice")
        self.gridLayout.addWidget(self.comboBoxTargetDevice, 0, 1, 1, 1)
        self.pushButtonStop = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonStop.setAutoFillBackground(False)
        self.pushButtonStop.setStyleSheet("")
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.gridLayout.addWidget(self.pushButtonStop, 2, 3, 1, 1)
        self.pushButtonForward = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonForward.setStyleSheet("")
        self.pushButtonForward.setObjectName("pushButtonForward")
        self.gridLayout.addWidget(self.pushButtonForward, 2, 4, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelMotor = QtWidgets.QLabel(self.centralWidget)
        self.labelMotor.setObjectName("labelMotor")
        self.horizontalLayout.addWidget(self.labelMotor)
        self.sliderSpeedControl = QtWidgets.QSlider(self.centralWidget)
        self.sliderSpeedControl.setMaximum(127)
        self.sliderSpeedControl.setProperty("value", 20)
        self.sliderSpeedControl.setOrientation(QtCore.Qt.Horizontal)
        self.sliderSpeedControl.setObjectName("sliderSpeedControl")
        self.horizontalLayout.addWidget(self.sliderSpeedControl)
        self.lineEditMotorSpeed = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEditMotorSpeed.setStyleSheet("max-width:25px;")
        self.lineEditMotorSpeed.setObjectName("lineEditMotorSpeed")
        self.horizontalLayout.addWidget(self.lineEditMotorSpeed)
        self.checkBoxStickyMode = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBoxStickyMode.setObjectName("checkBoxStickyMode")
        self.horizontalLayout.addWidget(self.checkBoxStickyMode)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 763, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuConnection = QtWidgets.QMenu(self.menuBar)
        self.menuConnection.setObjectName("menuConnection")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionDevices = QtWidgets.QAction(MainWindow)
        self.actionDevices.setObjectName("actionDevices")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/disconnected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDisconnect.setIcon(icon)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionConnect = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/connected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/connected.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionConnect.setIcon(icon1)
        self.actionConnect.setObjectName("actionConnect")
        self.menuConnection.addAction(self.actionConnect)
        self.menuConnection.addAction(self.actionDisconnect)
        self.menuBar.addAction(self.menuConnection.menuAction())
        self.mainToolBar.addAction(self.actionConnect)
        self.mainToolBar.addAction(self.actionDisconnect)

        self.retranslateUi(MainWindow)
        self.sliderSpeedControl.rangeChanged['int','int'].connect(self.lineEditMotorSpeed.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonReverse.setText(_translate("MainWindow", "Reverse"))
        self.pushButtonStop.setText(_translate("MainWindow", "Stop"))
        self.pushButtonForward.setText(_translate("MainWindow", "Forward"))
        self.labelMotor.setText(_translate("MainWindow", "Motor Speed"))
        self.checkBoxStickyMode.setText(_translate("MainWindow", "Sticky Mode"))
        self.menuConnection.setTitle(_translate("MainWindow", "Connection"))
        self.actionDevices.setText(_translate("MainWindow", "Devices"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
    def printsomething():
        print("hieu haha")
#import hieu_rc

