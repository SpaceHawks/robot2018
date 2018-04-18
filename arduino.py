"""commands:
1: drive motors
"""
from serial import Serial
from pyqtgraph.Qt import QtGui, QtCore# (the example applies equally well to PySide)

class Arduino():
    """
    An interface with Arduino, which is attached to the RPi by the serial pins.
    """
    def __init__(self, serialPort):
        self.serialPort = Serial(serialPort, baudrate=115200, timeout=3.0)
        self.lastMessage = None

    def write(self, message, forced = False):
        message.append((256 - sum(message)) % 256)
        self.writeDirectly(message, forced)

    def writeDirectly(self, message, forced = False):
        if forced or self.lastMessage != message:
            self.serialPort.write(message)
            self.lastMessage = message

    def read(self, numBytes):
        return None

    def motor(self, device, value1, value2, forced=False):
        if value1 < 0: value1 += 256
        if value2 < 0: value2 += 256
        self.write([1, device, value1, value2], forced=forced)

    def drive(self, drive, turn, forced=False, usingTail=False):
        if usingTail:
            drive = -drive
            turn = -turn
        self.motor(10, drive, turn, forced=forced)

    def tankDrive(self, leftSpeed, rightSpeed, forced=False, usingTail=False):
        if usingTail:
            leftSpeed, rightSpeed = -rightSpeed, -leftSpeed
        self.motor(11, leftSpeed, rightSpeed, forced=forced)

    def stop(self):
        self.drive(0, 0, forced=True)

    def turn(self, direction, forced=False, usingTail=False):
        speed = abs(direction)
        if direction > 0:
            self.right(speed, forced, usingTail)
        else:
            self.left(speed, forced, usingTail)

    def left(self, speed, forced=False, usingTail=False):
        self.drive(speed, -100, forced=forced, usingTail=usingTail)

    def right(self, speed, forced=False, usingTail=False):
        self.drive(speed, 100, forced=forced, usingTail=usingTail)

    def forward(self, speed, forced=False, usingTail=False):
        self.drive(speed, 0, forced=forced, usingTail=usingTail)

    def backward(self, speed, forced=False, usingTail=False):
        self.drive(-speed, 0, forced=forced, usingTail=usingTail)

    def setSpeedLimit(self, speed):
        self.write([0, 10, speed, 0], forced=True)

    def augerForward(self, forced=False):
        self.motor(8, 1, 0, forced=forced)

    def augerReverse(self, forced=False):
        self.motor(8, 1, 1, forced=forced)

    def augerStop(self, forced=False):
        self.motor(8, 0, 0, forced=forced)

    def tilterPosAndSpeed(self, pos, speed, forced=False):
        self.motor(5, pos, speed, forced=forced)

    def tilterStop(self):
        pass

class FakeArduino():
    """
    An interface with Arduino, which is attached to the RPi by the serial pins.
    """

    def __init__(self, serialPort):
        print("Init FakeArduino:", serialPort)

    def write(self, message, forced = False):
        print("FakeArduino -> write(",message,")")
        return True

    def writeDirectly(self, message, forced = False):
        print("FakeArduino -> writeDirectly(",message,")")
        return True

    def read(self, numBytes):
        print("FakeArduino -> read()")
        return None

    def motor(self, device, value1, value2, forced = False):
        print("FakeArduino -> motor(", device, value1, value2, ")")
        return True

    def drive(self, drive, turn, forced = False, usingTail = False):
        print("FakeArduino -> drive(", drive, turn, ")")
        return True

    def tankDrive(self, leftSpeed, rightSpeed, forced = False, usingTail = False):
        print("FakeArduino -> tankDrive(", leftSpeed, rightSpeed, ")")
        return True

    def stop(self):
        print("FakeArduino -> stop()")
        return True

    def left(self, speed, forced = False, usingTail = False):
        print("FakeArduino -> left(", speed,")")
        return True

    def right(self, speed, forced = False, usingTail = False):
        print("FakeArduino -> right(", speed,")")
        return True

    def forward(self, speed, forced = False, usingTail = False):
        print("FakeArduino -> forward(", speed,")")
        return True

    def backward(self, speed, forced = False, usingTail = False):
        print("FakeArduino -> backward(", speed,")")
        return True

    def setSpeedLimit(self, speed):
        print("FakeArduino -> setSpeedLimit(", speed,")")
        return True

    def augerForward(self, forced=False):
        print("FakeArduino -> augerForward()")
        return True
    def augerReverse(self, forced=False):
        print("FakeArduino -> augerReverse()")
        return True
    def augerStop(self, forced=False):
        print("FakeArduino -> augerStop()")
        return True
    def tilterPosAndSpeed(self, pos, speed, forced=False):
        print("FakeArduino -> tilterPosAndSpeed(",pos,",", speed,")")
        return True
    def tilterStop(self):
        print("FakeArduino -> tilterStop()")
        return True

class Task():
    completed = QtCore.pyqtSignal()
    abandoned = QtCore.pyqtSignal()
    def __init__(self, arduino):
        self.arduino = arduino
        self.setSliderPos = None
        self.setTilterPos = None

    def update(self, currentSliderPos, currentTilterPos):
        if currentSliderPos == self.setSliderPos and currentTilterPos == self.currentTilterPos:
            self.completed.emit()
    def execute(self):
        self.arduino.tilerPos()
