from interface import *
from UIautoGUI import *
import pygame
from PyQt5.QtCore import QByteArray, QObject, pyqtSignal
import struct


robot = None
gear = [20, 40, 60, 80, 100]
gearIndex = 0
robotAlliveTimer = QtCore.QTimer()
xboxTimer = QtCore.QTimer()

def connect():
    global robot
    if ui.pushButtonConnectDisconnect.text() == "Connect":
        success = False
        robot = RobotClient()
        robot.tcpSocket.connected.connect(robotConnected)
        robot.tcpSocket.disconnected.connect(robotDisconnected)
        ui.labelConnectionStatus.setText("Connecting to robot...")
        ip = ".".join(getIPAddress().split('.')[:3])+'.'
        for i in range(2, 255, 1):
            if robot.connect(ip+str(i), port=1234):
                ui.labelConnectionStatus.setText("Connected @ " + ip + str(i))
                ui.textBrowserNextTasks.append("Connected robot at " + ip + str(i))
                return
        ui.labelConnectionStatus.setText("Could not find robot!")
    else:
        robot.disconnect()

def robotConnected():
    ui.pushButtonConnectDisconnect.setText("Disconnect")
    ui.pushButtonForward.pressed.connect(forward)
    ui.pushButtonForward.released.connect(stop)
    ui.pushButtonBackward.pressed.connect(backward)
    ui.pushButtonBackward.released.connect(stop)
    ui.pushButtonLeft.pressed.connect(left)
    ui.pushButtonLeft.released.connect(stop)
    ui.pushButtonRight.pressed.connect(right)
    ui.pushButtonRight.released.connect(stop)
    ui.pushButtonStop.released.connect(stop)
    ui.pushButtonSpeedUp.released.connect(incrementDrive)
    ui.pushButtonSpeedDown.released.connect(decrementDrive)
    ui.pushButtonForward.setVisible(True)
    ui.pushButtonBackward.setVisible(True)
    ui.pushButtonLeft.setVisible(True)
    ui.pushButtonRight.setVisible(True)
    ui.pushButtonStop.setVisible(True)
    ui.pushButtonSpeedUp.setVisible(True)
    ui.pushButtonSpeedDown.setVisible(True)
    xboxTimer.timeout.connect(loopXbox360Mac)
    if initXbox360():
        xboxTimer.start(50)
    robotAlliveTimer.timeout.connect(robot.stillAlive)
    robotAlliveTimer.start(400)

def robotDisconnected():
    robotAlliveTimer.stop()
    xboxTimer.stop()
    ui.pushButtonConnectDisconnect.setText("Connect")
    ui.labelConnectionStatus.setText("Disconnected")
    ui.textBrowserNextTasks.append("Disconnected robot!")
    hideButtons()

def hideButtons():
    ui.pushButtonForward.setVisible(False)
    ui.pushButtonBackward.setVisible(False)
    ui.pushButtonLeft.setVisible(False)
    ui.pushButtonRight.setVisible(False)
    ui.pushButtonStop.setVisible(False)
    ui.pushButtonSpeedUp.setVisible(False)
    ui.pushButtonSpeedDown.setVisible(False)

def forward(speed=None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(speed)
    animateTurn(0)
    robot.drive(drive=speed, turn=0)

def backward(speed=None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(-speed)
    animateTurn(0)
    robot.drive(drive=-speed, turn=0)

def right(speed=None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(speed)
    animateTurn(100)
    robot.drive(drive=speed, turn=100)

def left(speed=None):
    if speed == None:
        speed = gear[gearIndex]
    animateDrive(speed)
    animateTurn(-100)
    robot.drive(drive=speed, turn=-100)

def stop():
    animateDrive(0)
    animateTurn(0)
    robot.drive(drive=0, turn=0)

def drive(drive, turn):
    animateDrive(drive)
    animateTurn(turn)
    robot.drive(drive=drive, turn=turn)

def animateDrive(drive):
    pass

def animateTurn(turn):
    pass

def incrementDrive():
    global gearIndex
    if gearIndex < 4:
        gearIndex += 1

def decrementDrive():
    global gearIndex
    if gearIndex > 0:
        gearIndex -= 1

def initXbox360():
    pygame.joystick.init()
    clock = pygame.time.Clock()
    clock.tick(60)  # how fast it updates
    joytickCount = pygame.joystick.get_count()
    if joytickCount < 1:
        pygame.joystick.quit()
        return False
    joysticks = []
    for i in range(0, joytickCount):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print("Detected joystick '", joysticks[-1].get_name(), "'")
    return True

def loopXbox360():
    "Opens a window and prints events to the terminal. Closes on ESC or QUIT."
    global robot
    for event in pygame.event.get():
        # KEPT BC ITS A WAY TO STOP PROGRAM
        if event.type == pygame.QUIT:
            print("Received event 'Quit', exiting.")
            pygame.display.quit()
            return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Escape key pressed, exiting.")
            pygame.display.quit()
            return
            # COMMENTED OUT BC USE OF KEYBOARD
            #    elif event.type == KEYDOWN:
            #         print ("Keydown,",event.key)
            # elif event.type == KEYUP:
            #         print ("Keyup,",event.key)
            # elif event.type == MOUSEMOTION:
            #       print "Mouse movement detected."
            # elif event.type == MOUSEBUTTONDOWN:
            #        print ("Mouse button",event.button,"down at",pygame.mouse.get_pos())
            # elif event.type == MOUSEBUTTONUP:
            #       print ("Mouse button",event.button,"up at",pygame.mouse.get_pos())
            # Will work on once I know what it's inputting for left, right, down etc
            # elif event.type == JOYAXISMOTION:
            #       print ("Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion.")
            #      print ("direction", ("%.3f" % event.value ))
        elif event.type == pygame.JOYAXISMOTION:
            # for left analog stick; forward and backward motion -- full speed
            if event.axis == 2:
                if event.value < -1:
                    stop()
                elif event.value > 0:
                    left(int(abs(100 * event.value)))
                elif event.value < 0:
                    right(int(abs(100 * event.value)))
                else:
                    stop()

        elif event.type == pygame.JOYBUTTONDOWN:
            # print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"pressed.")
            if event.button == 0:
                robot.decreaseDistanceToBin()
            if event.button == 1:
                robot.approachBin(True)
            if event.button == 2:
                robot.approachBin(False)
            if event.button == 3:
                robot.increaseDistanceToBin()
            if event.button == 4:
                decrementDrive()
            if event.button == 5:
                incrementDrive()
        elif event.type == pygame.JOYBUTTONUP:
            # print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"released.")
            if event.button >= 0 and event.button <= 3:
                stop()
        elif event.type == pygame.JOYHATMOTION:
            # print ("Joystick '",joysticks[event.joy].get_name(),"' D-Pad",event.hat," moved.")
            if event.value == (1, 0):
                right()
            if event.value == (-1, 0):
                left()
            if event.value == (0, -1):
                backward()
            if event.value == (0, 1):
                forward()
            if event.value == (0, 0):
                stop()
        elif event.type == pygame.JOYBUTTONUP:
            pass

lastDrive = 0
lastTurn = 0

def customSetupUI():
    pass

def printIP(ip):
    print(ip)

def loopXbox360Mac():
    global lastDrive, lastTurn
    "Opens a window and prints events to the terminal. Closes on ESC or QUIT."
    for event in pygame.event.get():
        # KEPT BC ITS A WAY TO STOP PROGRAM
        if event.type == pygame.QUIT:
            print("Received event 'Quit', exiting.")
            pygame.display.quit()
            return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Escape key pressed, exiting.")
            pygame.display.quit()
            return
            # COMMENTED OUT BC USE OF KEYBOARD
            #    elif event.type == KEYDOWN:
            #         print ("Keydown,",event.key)
            # elif event.type == KEYUP:
            #         print ("Keyup,",event.key)
            # elif event.type == MOUSEMOTION:
            #       print "Mouse movement detected."
            # elif event.type == MOUSEBUTTONDOWN:
            #        print ("Mouse button",event.button,"down at",pygame.mouse.get_pos())
            # elif event.type == MOUSEBUTTONUP:
            #       print ("Mouse button",event.button,"up at",pygame.mouse.get_pos())
            # Will work on once I know what it's inputting for left, right, down etc
            # elif event.type == JOYAXISMOTION:
            #       print ("Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion.")
            #      print ("direction", ("%.3f" % event.value ))
        elif event.type == pygame.JOYAXISMOTION:
            # for left analog stick; forward and backward motion -- full speed
            #print("axis", event.axis, "value", event.value)
            if event.axis == 1 or event.axis == 2:
                pass
            else:
                if event.axis == 0: #left x
                    lastTurn = int(100 * event.value)
                    if lastTurn < 12 and lastTurn > -22:
                        lastTurn = 0
                elif event.axis == 3:  # right y
                    lastDrive = -int(100 * event.value)
                    if abs(lastDrive)<12:
                        lastDrive = 0
                elif event.axis == 4:  # trigger y
                    lastDrive = int(abs(50 * (event.value+1)))
                    if lastDrive == 0:
                        lastTurn = 0
                    else:
                        lastTurn = -100
                elif event.axis == 5:  # trigger y
                    lastDrive = int(abs(50 * (event.value+1)))
                    if lastDrive == 0:
                        lastTurn = 0
                    else:
                        lastTurn = 100
                else:
                    pass
                print(lastDrive, lastTurn)
                drive(lastDrive, lastTurn)



            # if event.axis == 2:
            #     if event.value < -1:
            #         stop()
            #     elif event.value > 0:
            #         left(int(abs(100 * event.value)))
            #     elif event.value < 0:
            #         right(int(abs(100 * event.value)))
            #     else:
            #         stop()

        elif event.type == pygame.JOYBUTTONDOWN:
            print ("Joystick button",event.button,"pressed.")
            if event.button == 11 or event.button == 1:
                backward()
            if event.button == 12 or event.button == 3:
                right()
            if event.button == 13 or event.button == 2:
                left()
            if event.button == 14 or event.button == 0:
                forward()
            if event.button == 8:
                decrementDrive()
            if event.button == 9:
                incrementDrive()
        elif event.type == pygame.JOYBUTTONUP:
            # print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"released.")
            if (event.button >= 0 and event.button <= 3) or (event.button >= 11 and event.button <= 14):
                stop()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    customSetupUI()
    ui.pushButtonConnectDisconnect.clicked.connect(connect)
    MainWindow.show()
    sys.exit(app.exec_())