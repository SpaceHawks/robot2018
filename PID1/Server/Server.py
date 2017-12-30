from arduino import *
import time
from motorControlGui import Ui_MotorWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
arduino = Arduino(i2cAddress = 7)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

import time
"""This is a timer, which keep track of elapsed time in miliseconds. It allows programmers to time many operations simultaneously."""

class Timer:
    def __init__(self):
        """"Constructor. Initilizes/resets a new timer."""
        # Your global variable is here

        self.reset()

    def reset(self):
        """Sets current time to be start time."""
        self.startTime = time.time()

    def getTime(self):
        """Gets the time elapsed since the last start time.
        return The elapsed time in miliseconds.
        """
        return (time.time() - self.startTime)
timer=Timer()
def motorLeft(speed): #Calling for left motor
    ui.numberDisplayTopLeft.display(speed)
    timer.reset()
    while(timer.getTime()<2):
        if(GPIO.input(4) == 1):
            arduino.motor(3, speed)
            time.sleep(0.03)
            break
        else:
            time.sleep(0.01)

def motorRight(speed): #Calling for right motor
    ui.numberDisplayTopRight.display(speed)
    timer.reset()
    while(timer.getTime()<2):
        if(GPIO.input(4) == 1):
            arduino.motor(1, speed)
            time.sleep(0.03)
            break
        else:
            time.sleep(0.01)

def motorMaster(speed): #Calling for both motor 
    ui.numberDisplayTopMiddle.display(speed)
    ui.sliderLeft.setValue(speed)
    ui.sliderRight.setValue(speed)
    motorLeft(speed)
    motorRight(speed)

def stop():
    ui.sliderCenter.setValue(0)
    motorMaster(0)

    
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MotorWindow()
ui.setupUi(MainWindow)
ui.sliderLeft.sliderReleased.connect(lambda: motorLeft(ui.sliderLeft.value())) #function for left slider
ui.sliderRight.sliderReleased.connect(lambda: motorRight(ui.sliderRight.value())) #function for right slider
ui.sliderCenter.sliderReleased.connect(lambda: motorMaster(ui.sliderCenter.value())) #function for center slider
ui.buttonStop.clicked.connect(stop) #Set speed to zero
MainWindow.show()


"""while True:
    for i in range(0, 100, 1):
        timer.reset()
        while(timer.getTime()<2):
            if(GPIO.input(4) == 1):
                arduino.motor(1, i)
                time.sleep(0.03)
                break
            else:
                time.sleep(0.01)
        timer.reset()
        while(timer.getTime()<2):
            if(GPIO.input(4) == 1):
                data = arduino.read(4)
                if data[0] == 1:
                    ui.numberDisplayBottomLeft.display(data[2])
                elif data[0] == 2:
                    ui.numberDisplayBottomRight.display(data[2])
               
                time.sleep(0.03)
                break
            else:
                time.sleep(0.01)"""
#arduino.write(4, [1,34,56])

sys.exit(app.exec_())
