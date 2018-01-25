from arduino import *
import time
from Hieu4 import Ui_MainWindow
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
def drive(speed): #Calling for left motor
    ui.blank_5.setText(str(sliderValue_5))
    timer.reset()
    print("Hieu")
    while(timer.getTime()<2):
        if(GPIO.input(4) == 1):
            arduino.motor(1, sliderValue_5)
            arduino.motor(2, 0)
            time.sleep(0.03)
            break
        else:
            time.sleep(0.01)

def turn(speed): #Calling for right motor
    ui.blank_6.setText(str(sliderValue_6))
    timer.reset()
    while(timer.getTime()<2):
        if(GPIO.input(4) == 1):
            arduino.motor(2, speed)
            time.sleep(0.03)
            break
        else:
            time.sleep(0.01)

##def motorMaster(speed): #Calling for both motor 
 ##   ui.numberDisplayTopMiddle.display(speed)
   ## ui.sliderLeft.setValue(speed)
   ## ui.sliderRight.setValue(speed)
    ##motorLeft(speed)
    ##motorRight(speed)

def stop():
    ui.blank_5.setText(0)

    
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.horizontalSlider_1.valueChanged.connect(lambda: motorMaster(ui.sliderCenter.value())) #function for center slider
ui.horizontalSlider_2.valueChanged.connect(lambda: motorMaster(ui.sliderCenter.value())) #function for center slider
ui.horizontalSlider_3.valueChanged.connect(lambda: motorMaster(ui.sliderCenter.value())) #function for center slider
ui.horizontalSlider_4.valueChanged.connect(lambda: motorMaster(ui.sliderCenter.value())) #function for center slider
ui.verticalSlider.valueChanged.connect(lambda:  ui.horizontalSlider_5.setValue(sliderValue_5)) #function for left slider
ui.horizontalSlider_5.valueChanged.connect(lambda: ui.blank_6.setText(str(sliderValue_6))) #function for right slider
ui.stopButton.clicked.connect(stop) #Set speed to zero
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
