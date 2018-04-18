#!/usr/bin/python3
# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import platform
import time
if platform.system() == "Linux":
    from distance_sensor import *
    import VL53L0X
    import ASUS.GPIO as GPIO
    class DistanceSensors:
        def __init__(self, shutdownPins):
            self.shutdownPins = shutdownPins
            GPIO.setwarnings(False)

            # Setup GPIO for shutdown pins on each VL53L0X
            GPIO.setmode(GPIO.BOARD)
            for pin in self.shutdownPins:
                GPIO.setup(pin, GPIO.OUT)

            # Set all shutdown pins low to turn off each VL53L0X
            for pin in self.shutdownPins:
                GPIO.output(pin, GPIO.LOW)

            # Keep all low for 500 ms or so to make sure they reset
            time.sleep(0.50)

            # Create one object per VL53L0X passing the address to give to
            # each.
            self.sensors = list()
            sensorAddress = 0x2B
            for i in range(len(self.shutdownPins)):
                tof = VL53L0X.VL53L0X(address=sensorAddress)
                self.sensors.append(tof)
                sensorAddress +=2

            for i in range(len(self.shutdownPins)):
                GPIO.output(self.shutdownPins[i], GPIO.HIGH)
                time.sleep(0.50)
                self.sensors[i].start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

            self.timing = self.sensors[0].get_timing()
            if (self.timing < 20000):
                self.timing = 20000
            print ("Timing %d ms" % (self.timing/1000))
            self.distances = [None]*len(self.shutdownPins)


        def update(self):
            for i in range(len(self.sensors)):
                self.distances[i]= self.sensors[i].get_distance()
            #print(self.distances)
            time.sleep(self.timing/1000000.00)

        def stop(self):
            for i in range(len(self.sensors)):
                self.sensors[i].stop_ranging()
                GPIO.output(self.shutdownPins[i], GPIO.LOW)
else:
    class DistanceSensors:
        def __init__(self, shutdownPins):
            print("Init distance sensors with shutdown pins:", shutdownPins)
            self.shutdownPins = shutdownPins
            self.distances = [1] * len(self.shutdownPins)

        def update(self):
            print("update distance sensors")

        def stop(self):
            print("Stopped distance sensors")