# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(693, 551)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.448, y1:0.556318, x2:0, y2:0, stop:0 rgba(0, 0, 0, 234), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(255, 255, 255);")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(120, 0, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0.517413 rgba(0, 0, 0, 217), stop:1 rgba(255, 255, 255, 255));")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.forwardButton = QtWidgets.QPushButton(self.centralWidget)
        self.forwardButton.setGeometry(QtCore.QRect(110, 190, 61, 61))
        self.forwardButton.setMouseTracking(False)
        self.forwardButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"border-color: none;")
        self.forwardButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/pi/Desktop/Pic/fwdButton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.forwardButton.setIcon(icon)
        self.forwardButton.setIconSize(QtCore.QSize(60, 60))
        self.forwardButton.setObjectName("forwardButton")
        self.backButton = QtWidgets.QPushButton(self.centralWidget)
        self.backButton.setGeometry(QtCore.QRect(110, 350, 61, 61))
        self.backButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"border-color: transparent;")
        self.backButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("/home/pi/Desktop/Pic/downButton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon1)
        self.backButton.setIconSize(QtCore.QSize(60, 60))
        self.backButton.setObjectName("backButton")
        self.leftButton = QtWidgets.QPushButton(self.centralWidget)
        self.leftButton.setGeometry(QtCore.QRect(20, 270, 71, 61))
        self.leftButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"border-color: transparent;")
        self.leftButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("/home/pi/Desktop/Pic/leftButton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftButton.setIcon(icon2)
        self.leftButton.setIconSize(QtCore.QSize(60, 60))
        self.leftButton.setObjectName("leftButton")
        self.rightButton = QtWidgets.QPushButton(self.centralWidget)
        self.rightButton.setGeometry(QtCore.QRect(190, 270, 71, 61))
        self.rightButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"border-color: transparent;")
        self.rightButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("/home/pi/Desktop/Pic/rightButton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rightButton.setIcon(icon3)
        self.rightButton.setIconSize(QtCore.QSize(60, 60))
        self.rightButton.setObjectName("rightButton")
        self.StickyButton = QtWidgets.QRadioButton(self.centralWidget)
        self.StickyButton.setGeometry(QtCore.QRect(574, 30, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.StickyButton.setFont(font)
        self.StickyButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"border-color: transparent;")
        self.StickyButton.setObjectName("StickyButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 40, 82, 135))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.blank_1 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.blank_1.setFont(font)
        self.blank_1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.blank_1.setObjectName("blank_1")
        self.verticalLayout.addWidget(self.blank_1)
        self.blank_2 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.blank_2.setFont(font)
        self.blank_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.blank_2.setObjectName("blank_2")
        self.verticalLayout.addWidget(self.blank_2)
        self.blank_3 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.blank_3.setFont(font)
        self.blank_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.blank_3.setObjectName("blank_3")
        self.verticalLayout.addWidget(self.blank_3)
        self.blank_4 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.blank_4.setFont(font)
        self.blank_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.blank_4.setObjectName("blank_4")
        self.verticalLayout.addWidget(self.blank_4)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(230, 40, 221, 121))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalSlider_1 = QtWidgets.QSlider(self.layoutWidget1)
        self.horizontalSlider_1.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0 rgba(27, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.horizontalSlider_1.setMinimum(-100)
        self.horizontalSlider_1.setMaximum(100)
        self.horizontalSlider_1.setSingleStep(5)
        self.horizontalSlider_1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_1.setObjectName("horizontalSlider_1")
        self.verticalLayout_2.addWidget(self.horizontalSlider_1)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.layoutWidget1)
        self.horizontalSlider_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0 rgba(27, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"selection-color: rgb(255, 0, 0);")
        self.horizontalSlider_2.setMinimum(-100)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setSingleStep(5)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalLayout_2.addWidget(self.horizontalSlider_2)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.layoutWidget1)
        self.horizontalSlider_3.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0 rgba(27, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.horizontalSlider_3.setMinimum(-100)
        self.horizontalSlider_3.setSingleStep(5)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.verticalLayout_2.addWidget(self.horizontalSlider_3)
        self.horizontalSlider_4 = QtWidgets.QSlider(self.layoutWidget1)
        self.horizontalSlider_4.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0 rgba(27, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.horizontalSlider_4.setMinimum(-100)
        self.horizontalSlider_4.setMaximum(100)
        self.horizontalSlider_4.setSingleStep(5)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.verticalLayout_2.addWidget(self.horizontalSlider_4)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(26, 44, 91, 131))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0.517413 rgba(0, 0, 0, 217), stop:1 rgba(255, 255, 255, 255));")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0.348259 rgba(27, 0, 0, 252), stop:1 rgba(255, 255, 255, 255));")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0.348259 rgba(27, 0, 0, 252), stop:1 rgba(255, 255, 255, 255));")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0.348259 rgba(27, 0, 0, 252), stop:1 rgba(255, 255, 255, 255));")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.verticalSlider = QtWidgets.QSlider(self.centralWidget)
        self.verticalSlider.setGeometry(QtCore.QRect(600, 200, 21, 181))
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setSingleStep(5)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(490, 400, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0.517413 rgba(0, 0, 0, 217), stop:1 rgba(255, 255, 255, 255));")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_turning = QtWidgets.QLabel(self.centralWidget)
        self.label_turning.setGeometry(QtCore.QRect(260, 420, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_turning.setFont(font)
        self.label_turning.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0.517413 rgba(0, 0, 0, 217), stop:1 rgba(255, 255, 255, 255));")
        self.label_turning.setAlignment(QtCore.Qt.AlignCenter)
        self.label_turning.setObjectName("label_turning")
        self.horizontalSlider_5 = QtWidgets.QSlider(self.centralWidget)
        self.horizontalSlider_5.setGeometry(QtCore.QRect(240, 380, 219, 22))
        self.horizontalSlider_5.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.960015, y1:1, x2:1, y2:0, stop:0 rgba(27, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.horizontalSlider_5.setMinimum(-100)
        self.horizontalSlider_5.setMaximum(100)
        self.horizontalSlider_5.setSingleStep(5)
        self.horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_5.setObjectName("horizontalSlider_5")
        self.stopButton = QtWidgets.QPushButton(self.centralWidget)
        self.stopButton.setGeometry(QtCore.QRect(340, 190, 131, 111))
        self.stopButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"border-color: transparent;")
        self.stopButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("/home/pi/Desktop/Pic/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon4)
        self.stopButton.setIconSize(QtCore.QSize(100, 100))
        self.stopButton.setObjectName("stopButton")
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(350, 310, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"border-color: transparent;\n"
"color: rgb(255, 0, 0);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.blank_5 = QtWidgets.QLineEdit(self.centralWidget)
        self.blank_5.setGeometry(QtCore.QRect(390, 420, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.blank_5.setFont(font)
        self.blank_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.blank_5.setObjectName("blank_5")
        self.blank_6 = QtWidgets.QLineEdit(self.centralWidget)
        self.blank_6.setGeometry(QtCore.QRect(620, 400, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.blank_6.setFont(font)
        self.blank_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.blank_6.setObjectName("blank_6")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 693, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuLofty = QtWidgets.QMenu(self.menuBar)
        self.menuLofty.setObjectName("menuLofty")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuLofty.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Motor Speed"))
        self.StickyButton.setText(_translate("MainWindow", "Sticky"))
        self.label_2.setText(_translate("MainWindow", "Motor 1"))
        self.label_3.setText(_translate("MainWindow", "Motor 2"))
        self.label_5.setText(_translate("MainWindow", "Motor 3"))
        self.label_7.setText(_translate("MainWindow", "Motor 4"))
        self.label_4.setText(_translate("MainWindow", "Drive speed"))
        self.label_turning.setText(_translate("MainWindow", "turning speed"))
        self.label_6.setText(_translate("MainWindow", "STOP!"))
        self.menuLofty.setTitle(_translate("MainWindow", "Lofty"))


        
#directional funcitons
def sticky():
    stickyValue = ui.StickyButton.isChecked()

def forwardPressed():
    # if sticky button is not pressed do dis
    print("fwd pressed")
    lastPress = 1
def forwardReleased():
    if ui.StickyButton.isChecked():
        print("sticky is checked fwd button")
    else:
        print("Hieu said to print unchecked")

    # does something when it is releeased and not pressed
def reverse():
    if ui.StickyButton.isChecked()== True:
        print("sticky on R")
    else:
        print("sticky off R")

def right():
    if ui.StickyButton.isChecked() == True:
        print("sticky on Rt")
    else:
        print("sticky off rt")
    
def left():
    if ui.StickyButton.isChecked() == True:
        print("sticky on Left")
    else:
        print("sticky off Left")

def sliderDisplay_1():
    sliderValue_1 = ui.horizontalSlider_1.value()
    if sliderValue_1 >= -10 and sliderValue_1 <= 10:
        sliderValue_1 = 0
        ui.horizontalSlider_1.setValue(sliderValue_1)
        
    ui.blank_1.setText(str(sliderValue_1))
    print(sliderValue_1)
def sliderDisplay_2():
    sliderValue_2 = ui.horizontalSlider_2.value()
    if sliderValue_2 >= -10 and sliderValue_2 <= 10:
        sliderValue_2 = 0
        ui.horizontalSlider_2.setValue(sliderValue_2)
        
    ui.blank_2.setText(str(sliderValue_2))
    print(sliderValue_2)
def sliderDisplay_3():
    sliderValue_3 = ui.horizontalSlider_3.value()
    if sliderValue_3 >= -10 and sliderValue_3 <= 10:
        sliderValue_3 = 0
        ui.horizontalSlider_3.setValue(sliderValue_3)
        
    ui.blank_3.setText(str(sliderValue_3))
    print(sliderValue_3)
def sliderDisplay_4():
    sliderValue_4 = ui.horizontalSlider_4.value()
    if sliderValue_4 >= -10 and sliderValue_4 <= 10:
        sliderValue_4 = 0
        ui.horizontalSlider_4.setValue(sliderValue_4)
        
    ui.blank_4.setText(str(sliderValue_4))
    print(sliderValue_4)
    
def sliderDisplay_5():
    sliderValue_5 = ui.horizontalSlider_5.value()
    if sliderValue_5 >= -10 and sliderValue_5 <= 10:
        sliderValue_5 = 0
        ui.horizontalSlider_5.setValue(sliderValue_5)
        
    ui.blank_5.setText(str(sliderValue_5))
    print(sliderValue_5)

    
def sliderDisplay_6():
    sliderValue_6 = ui.verticalSlider.value()
    if sliderValue_6 >= -10 and sliderValue_6 <= 10:
        sliderValue_6 = 0
        ui.verticalSlider.setValue(sliderValue_6)
        
    ui.blank_6.setText(str(sliderValue_6))
    print(sliderValue_6)

from arduino import *
arduino = Arduino(i2cAddress = 7)

def forward(speed):
    arduino.motor(1, speed)
    arduino.motor(2, 0)
    
def backward(speed):
    arduino.motor(1, -speed)
    arduino.motor(2, 0)

def right(speed):
    arduino.motor(1, speed)
    arduino.motor(2, 100)
def left(speed):
    arduino.motor(1, speed)
    arduino.motor(2, -100)
    
def setDrive(speed): #Calling for left motor
    if ui.StickyButton.isChecked():
        arduino.motor(1, speed)
        ui.blank_6.setText(str(speed))
    
def stop():
    arduino.motor(1, 0)
    ui.blank_6.setText(str(0))
    ui.verticalSlider.setValue(0)
    ui.blank_5.setText(str(0))
    ui.horizontalSlider_5.setValue(0)


def pause():
    if not ui.StickyButton.isChecked():
        arduino.motor(1, 0)
    
def setTurn(speed):
    ui.blank_5.setText(str(speed))
    arduino.motor(2, speed)

        
#initialize the main window gui
import sys
lastPressed = 0
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
MainWindow.setMouseTracking(True)
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
#connects buttons to funtions
ui.forwardButton.pressed.connect(lambda: forward(ui.verticalSlider.value()))
ui.forwardButton.released.connect(pause)
ui.backButton.pressed.connect(lambda: backward(ui.verticalSlider.value()))
ui.backButton.released.connect(pause)
ui.rightButton.pressed.connect(lambda: right(ui.verticalSlider.value()))
ui.rightButton.released.connect(pause)
ui.leftButton.pressed.connect(lambda: left(ui.verticalSlider.value()))
ui.leftButton.released.connect(pause)
ui.stopButton.pressed.connect(stop)
ui.horizontalSlider_1.valueChanged.connect(sliderDisplay_1)
ui.horizontalSlider_2.valueChanged.connect(sliderDisplay_2)
ui.horizontalSlider_3.valueChanged.connect(sliderDisplay_3)
ui.horizontalSlider_4.valueChanged.connect(sliderDisplay_4)

#Turn Control
ui.horizontalSlider_5.valueChanged.connect(lambda: setTurn(ui.horizontalSlider_5.value()))

#Drive Control
ui.verticalSlider.valueChanged.connect(lambda: setDrive(ui.verticalSlider.value()))#ui.verticalSlider.value()))

ui.StickyButton.toggled.connect(sticky)
#from PySide import QtGui
#point = QtGui.QCursor().pos()
#print ("x: %s; y: %s") % (point.x(), point.y())
MainWindow.show()
sys.exit(app.exec_())


