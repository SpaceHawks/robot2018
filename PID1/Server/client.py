"""
Commands:
    1: drive motors

"""
from gui import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from tcp import Robot


app = QtWidgets.QApplication(sys.argv)
gui = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
robot = Robot(ipAddress = "192.168.0.6")

pressedButton = 0

def initGUI():    
    ui.setupUi(gui)
    #guiTimer = QtCore.QTimer()
    #guiTimer.timeout.connect(updateRobotInfo)
    #guiTimer.start(1000)
    #commandTimer = QtCore.QTimer()
    #commandTimer.timeout.connect(tcpTest)
    #commandTimer.start(1000)

    #Connect signals
    ui.pushButtonForward.pressed.connect(forwardPressed)
    ui.pushButtonForward.released.connect(forwardReleased)
    ui.pushButtonReverse.pressed.connect(reversePressed)
    ui.pushButtonReverse.released.connect(reverseReleased)
    ui.pushButtonStop.pressed.connect(stop)
    ui.actionConnect.triggered.connect(connect)
    ui.sliderSpeedControl.valueChanged.connect(lineEditUpdateSpeed)
    app.aboutToQuit.connect(close)

    currentSliderValue = str(ui.sliderSpeedControl.value())
    ui.lineEditMotorSpeed.setText(currentSliderValue)

    gui.show()
    sys.exit(app.exec_())

def lineEditUpdateSpeed(speed):
    speed = str(speed)
    ui.lineEditMotorSpeed.setText(speed)
    if pressedButton == -1:
        reversePressed()
    elif pressedButton == 1:
        forwardPressed()
    else:
        pass

def forwardPressed():
    global pressedButton
    value = ui.sliderSpeedControl.value()
    robot.motor(device = 1, value = value)
    pressedButton = 1

def reversePressed():
    global pressedButton
    value = ui.sliderSpeedControl.value()
    robot.motor(device = 1, value = -value)
    pressedButton = -1

def forwardReleased():
    if not ui.checkBoxStickyMode.isChecked():
        stop()

def reverseReleased():
    if not ui.checkBoxStickyMode.isChecked():
        stop()  

def connect():
    robot.start()

def stop():
    global pressedButton
    robot.motor(device = 1, value = 0)
    pressedButton = 0

def close():
    stop()
    robot.stop()
    app.exit()
    sys.exit()

initGUI()





