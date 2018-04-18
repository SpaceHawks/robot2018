import pygame, platform
#from PyQt5.QtCore import QObject, QtCore.pyqtSignal, QCoreApplication
from pyqtgraph.Qt import QtCore
import os

positioning = False
stillAlive = False

class Xbox360(QtCore.QObject):
    #button pressed
    APressed = QtCore.pyqtSignal()
    BPressed = QtCore.pyqtSignal()
    XPressed = QtCore.pyqtSignal()
    YPressed = QtCore.pyqtSignal()
    backPressed = QtCore.pyqtSignal()
    startPressed = QtCore.pyqtSignal()
    leftBumperPressed = QtCore.pyqtSignal()
    rightBumperPressed = QtCore.pyqtSignal()
    leftJoyButtonPressed = QtCore.pyqtSignal()
    rightJoyButtonPressed = QtCore.pyqtSignal()

    #button released
    AReleased = QtCore.pyqtSignal()
    BReleased = QtCore.pyqtSignal()
    XReleased = QtCore.pyqtSignal()
    YReleased = QtCore.pyqtSignal()
    backReleased = QtCore.pyqtSignal()
    startReleased = QtCore.pyqtSignal()
    leftBumperReleased = QtCore.pyqtSignal()
    rightBumperReleased = QtCore.pyqtSignal()
    leftJoyButtonReleased = QtCore.pyqtSignal()
    rightJoyButtonReleased = QtCore.pyqtSignal()

    #motion button pressed
    motionUp = QtCore.pyqtSignal()
    motionDown = QtCore.pyqtSignal()
    motionLeft = QtCore.pyqtSignal()
    motionRight = QtCore.pyqtSignal()
    motionCenter = QtCore.pyqtSignal() #no motion button is pressed

    #Joystick movement
    leftJoystickHorizontalMove = QtCore.pyqtSignal(int)
    leftJoystickVerticalMove = QtCore.pyqtSignal(int)
    rightJoystickHorizontalMove = QtCore.pyqtSignal(int)
    rightJoystickVerticalMove = QtCore.pyqtSignal(int)
    leftTriggerMove = QtCore.pyqtSignal(int)
    rightTriggerMove = QtCore.pyqtSignal(int)
    # Mac
    # LTHUMBX = 0
    # LTHUMBY = 1
    # RTHUMBX = 2
    # RTHUMBY = 3
    # RTRIGGER = 4
    # LTRIGGER = 5
    # A = 6
    # B = 7
    # X = 8
    # Y = 9
    # LB = 10
    # RB = 11
    # BACK = 12
    # START = 13
    # XBOX = 14
    # LEFTTHUMB = 15
    # RIGHTTHUMB = 16
    # DPAD = 17
    if platform.system() == 'Linux':
        A = 0
        B = 1
        X = 2
        Y = 3
        LEFT_BUMP = 4
        RIGHT_BUMP = 5
        BACK = 6
        START = 7
        LEFT_STICK_BTN = 9
        RIGHT_STICK_BTN = 10

        LEFT_STICK_X = 0
        LEFT_STICK_Y = 1
        RIGHT_STICK_X = 3
        RIGHT_STICK_Y = 4
        LEFT_TRIGGER = 2
        RIGHT_TRIGGER = 5

        RIGHT = (1, 0)
        LEFT = (-1, 0)
        DOWN = (0, -1)
        UP = (0, 1)
        CENTER = (0, 0)
    elif platform.system() == 'Darwin':
        A = 0
        B = 1
        X = 2
        Y = 3
        LEFT_BUMP = 4
        RIGHT_BUMP = 5
        BACK = 6
        START = 7
        LEFT_STICK_BTN = 9
        RIGHT_STICK_BTN = 10

        LEFT_STICK_X = 0
        LEFT_STICK_Y = 1
        RIGHT_STICK_X = 3
        RIGHT_STICK_Y = 4
        LEFT_TRIGGER = 2
        RIGHT_TRIGGER = 5

        RIGHT = (1, 0)
        LEFT = (-1, 0)
        DOWN = (0, -1)
        UP = (0, 1)
        CENTER = (0, 0)
    elif platform.system() == 'Windows':
        A = 0
        B = 1
        X = 2
        Y = 3
        LEFT_BUMP = 4
        RIGHT_BUMP = 5
        BACK = 6
        START = 7
        LEFT_STICK_BTN = 9
        RIGHT_STICK_BTN = 10

        LEFT_STICK_X = 0
        LEFT_STICK_Y = 1
        RIGHT_STICK_X = 3
        RIGHT_STICK_Y = 4
        LEFT_TRIGGER = 2
        RIGHT_TRIGGER = 5

        RIGHT = (1, 0)
        LEFT = (-1, 0)
        DOWN = (0, -1)
        UP = (0, 1)
        CENTER = (0, 0)
    def __init__(self, arduino):
        super(Xbox360, self).__init__()
        self.gear = [20, 40, 60, 80, 100]
        self.gearIndex = 0
        self.arduino = arduino
        self.drive = 0
        self.turn = 0


    def init(self):
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.joystick.init()
        pygame.display.set_mode((1, 1))
        joytickCount = pygame.joystick.get_count()
        if joytickCount < 1:
            pygame.joystick.quit()
            return False
        self.joysticks = []
        for i in range(0, joytickCount):
            self.joysticks.append(pygame.joystick.Joystick(i))
            self.joysticks[-1].init()
            print("Detected joystick '", self.joysticks[-1].get_name(), "'")
        clock = pygame.time.Clock()
        clock.tick(60)  # how fast it updates
        return True
    def update(self):
        "Opens a window and prints events to the terminal. Closes on ESC or QUIT."
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == self.LEFT_STICK_X:
                    self.updateTurn(int(100 * event.value))

                elif event.axis == self.LEFT_STICK_Y:
                    pass

                elif event.axis == self.RIGHT_STICK_X:
                    pass

                elif event.axis == self.RIGHT_STICK_Y:
                    self.updateDrive(int(-100 * event.value))

                elif event.axis == self.LEFT_TRIGGER:
                    self.arduino.left(int(abs(50 * (event.value + 1))))

                elif event.axis == self.RIGHT_TRIGGER:
                    self.arduino.right(int(abs(50 * (event.value + 1))))

                else:
                    print("Unknown joy axis detected")
            elif event.type == pygame.JOYBUTTONDOWN:
                # print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"pressed.")
                if event.button == self.A:
                    self.APressed.emit()
                if event.button == self.B:
                    self.BPressed.emit()
                if event.button == self.X:
                    self.XPressed.emit()
                if event.button == self.Y:
                    self.YPressed.emit()
                if event.button == self.LEFT_BUMP:
                    self.leftBumperPressed.emit()
                if event.button == self.RIGHT_BUMP:
                    self.rightBumperPressed.emit()
                if event.button == self.BACK:
                    self.backPressed.emit()
                if event.button == self.START:
                    self.startPressed.emit()
                if event.button == self.LEFT_STICK_BTN:
                    self.leftJoyButtonPressed.emit()
                if event.button == self.RIGHT_STICK_BTN:
                    self.rightJoyButtonPressed.emit()
            elif event.type == pygame.JOYBUTTONUP:
                # print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"released.")
                if event.button == self.A:
                    self.AReleased.emit()
                if event.button == self.B:
                    self.BReleased.emit()
                if event.button == self.X:
                    self.XReleased.emit()
                if event.button == self.Y:
                    self.YReleased.emit()
                if event.button == self.LEFT_BUMP:
                    self.decrementDrive()
                    self.leftBumperReleased.emit()
                if event.button == self.RIGHT_BUMP:
                    self.incrementDrive()
                    self.rightBumperReleased.emit()
                if event.button == self.BACK:
                    self.backReleased.emit()
                if event.button == self.START:
                    self.startReleased.emit()
                if event.button == self.LEFT_STICK_BTN:
                    self.leftJoyButtonReleased.emit()
                if event.button == self.RIGHT_STICK_BTN:
                    self.rightJoyButtonReleased.emit()
            elif event.type == pygame.JOYHATMOTION:
                # print ("Joystick '",joysticks[event.joy].get_name(),"' D-Pad",event.hat," moved.")
                if event.value == self.RIGHT:
                    self.arduino.right(self.gear[self.gearIndex])
                    self.motionRight.emit()
                if event.value == self.LEFT:
                    self.arduino.left(self.gear[self.gearIndex])
                    self.motionLeft.emit()
                if event.value == self.DOWN:
                    self.arduino.backward(self.gear[self.gearIndex])
                    self.motionDown.emit()
                if event.value == self.UP:
                    self.arduino.forward(self.gear[self.gearIndex])
                    self.motionUp.emit()
                if event.value == self.CENTER:
                    self.arduino.stop()
                    self.motionCenter.emit()
    def quit(self):
        for joystick in self.joysticks:
            joystick.quit()
        pygame.joystick.quit()
    def incrementDrive(self):
        if self.gearIndex < 4:
            self.gearIndex += 1
    def decrementDrive(self):
        if self.gearIndex > 0:
            self.gearIndex -= 1
    def updateDrive(self, value):
        self.drive = value
        if abs(value) < 12:
            self.drive = 0
        self.arduino.drive(self.drive, self.turn)
    def updateTurn(self, value):
        self.turn = value
        if self.turn < 12 and self.turn > -22:
            self.turn = 0
        self.arduino.drive(self.drive, self.turn)
