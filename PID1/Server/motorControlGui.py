# -*- coding: utf-8 -*-
# sudo apt-get install python3 python3-pyqt5 
# to install pyqt5 on rpi3
# Form implementation generated from reading ui file 'motorwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MotorWindow(object):
    def setupUi(self, MotorWindow):
        MotorWindow.setObjectName("MotorWindow")
        MotorWindow.resize(100, 735)
        MotorWindow.setAccessibleName("")
        MotorWindow.setStyleSheet("QLabel{\n"
"    font: 63 14pt \"Yu Gothic UI Semibold\";\n"
"}\n"
"\n"
"QLCDNumber{\n"
"min-height: 50px;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(255, 85, 0, 255), stop:0.497512 rgba(255, 255, 255, 255), stop:1 rgba(255, 85, 0, 255));\n"
"    position: absolute; /* absolutely position 4px from the left and right of the widget. setting margins on the widget should work too... */\n"
"    left: 4px; right: 4px;\n"
"}\n"
"QSlider{\n"
"width: 40px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    height: 20px;\n"
"    size: 40px;\n"
"    background: green;\n"
"    margin: 0 -8px; /* expand outside the groove */\n"
"}\n"
"")
        self.centralWidget = QtWidgets.QWidget(MotorWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.numberDisplayTopLeft = QtWidgets.QLCDNumber(self.centralWidget)
        self.numberDisplayTopLeft.setMidLineWidth(0)
        self.numberDisplayTopLeft.setObjectName("numberDisplayTopLeft")
        self.verticalLayout_4.addWidget(self.numberDisplayTopLeft)
        self.label_9 = QtWidgets.QLabel(self.centralWidget)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_4.addWidget(self.label_9, 0, QtCore.Qt.AlignHCenter)
        self.sliderLeft = QtWidgets.QSlider(self.centralWidget)
        self.sliderLeft.setMinimum(-100)
        self.sliderLeft.setMaximum(100)
        self.sliderLeft.setOrientation(QtCore.Qt.Vertical)
        self.sliderLeft.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderLeft.setTickInterval(10)
        self.sliderLeft.setObjectName("sliderLeft")
        self.verticalLayout_4.addWidget(self.sliderLeft, 0, QtCore.Qt.AlignHCenter)
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter)
        self.numberDisplayBottomRight = QtWidgets.QLCDNumber(self.centralWidget)
        self.numberDisplayBottomRight.setObjectName("numberDisplayBottomRight")
        self.verticalLayout_4.addWidget(self.numberDisplayBottomRight)
        self.label_10 = QtWidgets.QLabel(self.centralWidget)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.numberDisplayTopMiddle = QtWidgets.QLCDNumber(self.centralWidget)
        self.numberDisplayTopMiddle.setObjectName("numberDisplayTopMiddle")
        self.verticalLayout_3.addWidget(self.numberDisplayTopMiddle)
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7, 0, QtCore.Qt.AlignHCenter)
        self.sliderCenter = QtWidgets.QSlider(self.centralWidget)
        self.sliderCenter.setMinimum(-100)
        self.sliderCenter.setMaximum(100)
        self.sliderCenter.setOrientation(QtCore.Qt.Vertical)
        self.sliderCenter.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderCenter.setTickInterval(10)
        self.sliderCenter.setObjectName("sliderCenter")
        self.verticalLayout_3.addWidget(self.sliderCenter, 0, QtCore.Qt.AlignHCenter)
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter)
        self.numberDIsplayBottomMiddle = QtWidgets.QLCDNumber(self.centralWidget)
        self.numberDIsplayBottomMiddle.setObjectName("numberDIsplayBottomMiddle")
        self.verticalLayout_3.addWidget(self.numberDIsplayBottomMiddle)
        self.label_8 = QtWidgets.QLabel(self.centralWidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.numberDisplayTopRight = QtWidgets.QLCDNumber(self.centralWidget)
        self.numberDisplayTopRight.setObjectName("numberDisplayTopRight")
        self.verticalLayout_2.addWidget(self.numberDisplayTopRight)
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter)
        self.sliderRight = QtWidgets.QSlider(self.centralWidget)
        self.sliderRight.setMinimum(-100)
        self.sliderRight.setMaximum(100)
        self.sliderRight.setOrientation(QtCore.Qt.Vertical)
        self.sliderRight.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderRight.setTickInterval(10)
        self.sliderRight.setObjectName("sliderRight")
        self.verticalLayout_2.addWidget(self.sliderRight, 0, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.numberDisplayBottomRight_2 = QtWidgets.QLCDNumber(self.centralWidget)
        self.numberDisplayBottomRight_2.setObjectName("numberDisplayBottomRight_2")
        self.verticalLayout_2.addWidget(self.numberDisplayBottomRight_2)
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonStop = QtWidgets.QPushButton(self.centralWidget)
        self.buttonStop.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";\n"
"width: 100px;\n"
"height:100px;\n"
"background-color: #ff0000;\n"
"color: #ffffff ;")
        self.buttonStop.setObjectName("buttonStop")
        self.horizontalLayout_2.addWidget(self.buttonStop)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        MotorWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MotorWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1002, 26))
        self.menuBar.setObjectName("menuBar")
        MotorWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MotorWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MotorWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MotorWindow)
        self.statusBar.setObjectName("statusBar")
        MotorWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MotorWindow)
        self.toolBar.setObjectName("toolBar")
        MotorWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(MotorWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MotorWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.toolBar_3 = QtWidgets.QToolBar(MotorWindow)
        self.toolBar_3.setObjectName("toolBar_3")
        MotorWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_3)

        self.retranslateUi(MotorWindow)
        QtCore.QMetaObject.connectSlotsByName(MotorWindow)

    def retranslateUi(self, MotorWindow):
        _translate = QtCore.QCoreApplication.translate
        MotorWindow.setWindowTitle(_translate("MotorWindow", "Motor Controller"))
        self.label_9.setText(_translate("MotorWindow", "Set Speed"))
        self.label_4.setText(_translate("MotorWindow", "Left"))
        self.label_10.setText(_translate("MotorWindow", "Current Speed"))
        self.label_7.setText(_translate("MotorWindow", "Set Speed"))
        self.label_3.setText(_translate("MotorWindow", "Master"))
        self.label_8.setText(_translate("MotorWindow", "Current Speed"))
        self.label_5.setText(_translate("MotorWindow", "Set Speed"))
        self.label_2.setText(_translate("MotorWindow", "Right"))
        self.label_6.setText(_translate("MotorWindow", "Current Speed"))
        self.buttonStop.setAccessibleName(_translate("MotorWindow", "stopButton"))
        self.buttonStop.setText(_translate("MotorWindow", "STOP"))
        self.toolBar.setWindowTitle(_translate("MotorWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MotorWindow", "toolBar_2"))
        self.toolBar_3.setWindowTitle(_translate("MotorWindow", "toolBar_3"))



