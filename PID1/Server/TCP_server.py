from tcp import Controller
from time import sleep
from arduino import Arduino
from timer import Timer
import RPi.GPIO as GPIO
from queue import Queue
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

q = Queue()
pc = Controller("192.168.2.104")
arduino = Arduino(i2cAddress = 7)
pc.start()
timer = Timer()
         

while 1:
    commands = pc.getNewCommands()
    if  commands is not None:
        for command in commands:
            if arduino.write(1, list(command)) is False:
                print("Failed at",command)