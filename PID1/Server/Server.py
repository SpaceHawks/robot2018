from arduino import *
import time
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

timer = Timer()
while True:
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
                print(arduino.read(4))
                time.sleep(0.03)
                break
            else:
                time.sleep(0.01)
#arduino.write(4, [1,34,56])