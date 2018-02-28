import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from tcp import Robot
from manualGUI import Ui_Manual
import pygame
from pygame.locals import *
import _thread



gear = [20, 40, 60, 80, 100]
gearIndex = 0
robot = Robot(ipAddress = "192.168.2.105")
timer = QtCore.QTimer()
timer.timeout.connect(robot.stillAlive)


def connect():
    global timer
    robot.start()
    #robot.stillAlive()
    timer.start(500)

def disconnect():
    pass

def forward(speed = None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(speed)
    animateTurn(0)
    robot.drive(drive = speed, turn = 0)

def backward(speed = None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(-speed)
    animateTurn(0)
    robot.drive(drive = -speed, turn = 0)

def right(speed = None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(speed)
    animateTurn(100)
    robot.drive(drive = speed, turn = 100)

def left(speed = None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(speed)
    animateTurn(-100)
    robot.drive(drive = speed, turn = -100)

def stop():
    animateDrive(0)
    animateTurn(0)
    robot.drive(drive = 0, turn = 0)

def animateDrive(drive):
    ui.blank_6.setText(str(drive))
    ui.verticalSlider.setValue(drive)
     
def animateTurn(turn):
    ui.blank_5.setText(str(turn))
    ui.horizontalSlider_5.setValue(turn)

def incrementDrive():
    global gearIndex
    if gearIndex < 4:
        gearIndex+=1

def decrementDrive():
    global gearIndex
    if gearIndex > 0:
        gearIndex-=1

def connectSignalAndSlot():
    ui.forwardButton.pressed.connect(forward)
    ui.forwardButton.released.connect(stop)
    ui.backButton.pressed.connect(backward)
    ui.backButton.released.connect(stop)
    ui.rightButton.pressed.connect(right)
    ui.rightButton.released.connect(stop)
    ui.leftButton.pressed.connect(left)
    ui.leftButton.released.connect(stop)
    ui.stopButton.pressed.connect(robot.stopAll)
    #ui.verticalSlider.valueChanged.connect(lambda: setDrive(ui.verticalSlider.value()))
    #ui.horizontalSlider_5.valueChanged.connect(lambda: setTurn(ui.horizontalSlider_5.value()))

def xbox360():
    "Opens a window and prints events to the terminal. Closes on ESC or QUIT."
    pygame.init()
    #screen = pygame.display.set_mode((40, 40))
    pygame.display.set_caption("JOYTEST")
    clock = pygame.time.Clock()
    joysticks = []
    drive = 40

    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print ("Detected joystick '",joysticks[-1].get_name(),"'")
    while 1:
        clock.tick(60) #how fast it updates
        for event in pygame.event.get():
            #KEPT BC ITS A WAY TO STOP PROGRAM
            if event.type == QUIT:
                print ("Received event 'Quit', exiting.")
                pygame.display.quit()
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                print ("Escape key pressed, exiting.")
                pygame.display.quit()
                return
                #COMMENTED OUT BC USE OF KEYBOARD
                #    elif event.type == KEYDOWN:
                #         print ("Keydown,",event.key)
                # elif event.type == KEYUP:
                #         print ("Keyup,",event.key)
                #elif event.type == MOUSEMOTION:
                    #       print "Mouse movement detected."
                # elif event.type == MOUSEBUTTONDOWN:
                #        print ("Mouse button",event.button,"down at",pygame.mouse.get_pos())
                #elif event.type == MOUSEBUTTONUP:
                    #       print ("Mouse button",event.button,"up at",pygame.mouse.get_pos())
                #Will work on once I know what it's inputting for left, right, down etc
                #elif event.type == JOYAXISMOTION:
                    #       print ("Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion.")
                    #      print ("direction", ("%.3f" % event.value ))
            elif event.type == JOYAXISMOTION:
                #for left analog stick; forward and backward motion -- full speed
                if event.axis == 2:
                    if event.value < -1:
                        stop()
                    elif event.value > 0:
                        left(int(abs(100*event.value)))
                    elif event.value < 0:
                        right(int(abs(100*event.value)))
                    else:
                        stop()
   
            elif event.type == JOYBUTTONDOWN:
                #print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"pressed.")
                if event.button == 0:
                    backward()
                if event.button == 1:
                    right()
                if event.button == 2:
                    left()
                if event.button == 3:
                    forward()
                if event.button == 4:
                    decrementDrive()
                if event.button == 5:
                    incrementDrive()
            elif event.type == JOYBUTTONUP:
                #print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"released.")
                if event.button >= 0 and event.button <=3:
                    stop()
            elif event.type == JOYHATMOTION:
                #print ("Joystick '",joysticks[event.joy].get_name(),"' D-Pad",event.hat," moved.")
                if event.value == (1,0):
                    right()    
                if event.value == (-1,0):
                    left()   
                if event.value == (0,-1):
                    backward()   
                if event.value == (0,1):
                    forward()    
                if event.value == (0,0):
                    stop()   
            elif event.type == JOYBUTTONUP:
                pass
app = QtWidgets.QApplication(sys.argv)
gui = QtWidgets.QMainWindow()
ui = Ui_Manual()
ui.setupUi(gui)
connectSignalAndSlot()
connect()
_thread.start_new_thread(xbox360,())
gui.show()
sys.exit(app.exec_())