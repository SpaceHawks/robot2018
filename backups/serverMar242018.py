import pygame

from PID import PID
from Tests.voice import Voice
from arduino import Arduino
from distance_sensor import *
from interface import *

voices = Voice("audio")

gear = [20, 40, 60, 80, 100]
gearIndex = 0

arduino = Arduino("/dev/ttyS1")
positioning = False
stillAlive = False
timer = QTimer()
xboxTimer = QTimer()
lastTurn = 0
lastDrive = 0


distanceSensorsTimer = QTimer()
safeDistaces = [100, 200, 300, 400, 500, 600, 700]
safeDistacesIndex = 3
distanceSensors = None

pid = None
pid2 = None

def gotManualMessageSplot(message):
    if arduino.writeDirectly(message) is False:
        print("Manual control fail: ", MESAGE_STRUCT.unpack(message))
    else:
        print("Manual control: ", MESAGE_STRUCT.unpack(message))

def gotAutomaticMessageSplot(decodedMessage):
    global positioning
    s = "Partial autonomy - "
    if decodedMessage[1] == 5:
        s += " Positioning for dumping: "
        if decodedMessage[2] == 0:
            stopSafeDistance()
            s += "OFF."
        elif decodedMessage[2] == 1:
            startSafeDistance()
            s += "ON."
        elif decodedMessage[2] == 2:
            decrementSafeDistance()
            s += " Decrement Distance"
        elif decodedMessage[2] == 3:
            incrementSafeDistance()
            s += " Increment Distance"
    print(s)

def gotSystemMessageSplot(decodedMessage):
    global positioning, stillAlive
    s = "System: - "
    if decodedMessage[1] == 0:
        s += " E-Stop: Hit"
        arduino.stop()
        positioning = False
        print(s)
    elif decodedMessage[1] == 5:
        s += " still alive"
        stillAlive = True

def gotSensorMessageSplot(decodedMessage):
    print("slot sensor ", decodedMessage)

def controllerDisconnectedSlot():
    voices.play(Voice.DISCONNECTED)
    arduino.stop()
    print("stop arduino")
    global timer
    timer.stop()
    print("stop timer")

def controllerConnectedSlot():
    voices.play(Voice.CONNECTED)
    global timer
    timer.start(500)

def haveHeardFromControllerSlot():
    global stillAlive
    if stillAlive:
        stillAlive = False
    else:
        arduino.stop()
        print("lost controller")

def incrementDrive():
    global gearIndex
    if gearIndex < 4:
        gearIndex += 1
    startSafeDistance()

def decrementDrive():
    global gearIndex
    if gearIndex > 0:
        gearIndex -= 1
    startSafeDistance()

def initXbox360():
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.joystick.init()
    pygame.display.set_mode((1, 1))
    #pygame.display.set_mode((1,1), pygame.HWSURFACE | pygame.DOUBLEBUF)
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

def loopXbox360Tinker():
    "Opens a window and prints events to the terminal. Closes on ESC or QUIT."
    global lastTurn, lastDrive
    for event in pygame.event.get():
        #print(event)
        # KEPT BC ITS A WAY TO STOP PROGRAM
        if event.type == pygame.QUIT:
            print("Received event 'Quit', exiting.")
            #pygame.display.quit()
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
            # for left analog stick; forward and backward motion -- full speed
            #print("axis", event.axis, "value", event.value)
            if event.axis == 1 or event.axis == 3:
                #print("axis 1 and  3")
                pass
            else:
                if event.axis == 0:  # left x
                    lastTurn = int(100 * event.value)
                    if lastTurn < 12 and lastTurn > -22:
                        lastTurn = 0
                elif event.axis == 4:  # right y
                    lastDrive = -int(100 * event.value)
                    if abs(lastDrive) < 12:
                        lastDrive = 0
                elif event.axis == 2:  # trigger left
                    lastDrive = int(abs(50 * (event.value + 1)))
                    if lastDrive == 0:
                        lastTurn = 0
                    else:
                        lastTurn = -100
                elif event.axis == 5:  # trigger right
                    lastDrive = int(abs(50 * (event.value + 1)))
                    if lastDrive == 0:
                        lastTurn = 0
                    else:
                        lastTurn = 100
                else:
                    pass
                #print(lastDrive, lastTurn)
                arduino.drive(lastDrive, lastTurn)

        elif event.type == pygame.JOYBUTTONDOWN:
            # print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"pressed.")
            if event.button == 0: #decrementSafeDistance safe distance
                decrementSafeDistance()
            if event.button == 1: #stop safe distance
                stopSafeDistance()
            if event.button == 2: #start safe distance
                startSafeDistance()
            if event.button == 3: #incrementSafeDistance safe distance
                incrementSafeDistance()
            if event.button == 4:
                decrementDrive()
            if event.button == 5:
                incrementDrive()
        elif event.type == pygame.JOYBUTTONUP:
            # print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"released.")
            if event.button >= 0 and event.button <= 3:
                arduino.stop()
        elif event.type == pygame.JOYHATMOTION:
            # print ("Joystick '",joysticks[event.joy].get_name(),"' D-Pad",event.hat," moved.")
            if event.value == (1, 0):
                arduino.right(gear[gearIndex])
            if event.value == (-1, 0):
                arduino.left(gear[gearIndex])
            if event.value == (0, -1):
                arduino.backward(gear[gearIndex])
            if event.value == (0, 1):
                arduino.forward(gear[gearIndex])
            if event.value == (0, 0):
                arduino.stop()

def distanceSensorLoop():
    global distanceSensors, pid, pid2
    driveLeft = None
    driveRight = None
    distanceSensors.update()
    dist1 = distanceSensors.distances[0]
    dist2 = distanceSensors.distances[1]
    if dist1 > 8000:
        pass
        # print("No object seen from sensor 1")
        #voices.play(Voice.TOO_FAR)
    elif dist1 <= 0:
        print("Sensor 1 failed")
        voices.play(Voice.DISTANCE_SENSOR_FAILURE)
        arduino.tankDrive(0,0)
        distanceSensorsTimer.stop()
    elif dist1 < 1000:
        pid.update(dist1)
        driveLeft = int(pid.output)
        if driveLeft > 100:
            driveLeft = 100
        if driveLeft < -100:
            driveLeft = -100
        driveLeft = - driveLeft #
        # print("sensor1", dist1, driveLeft)
    else:
        pass
    if dist2 > 8000:
        pass
        # print("No object seen from sensor 2")
        #voices.play(Voice.TOO_FAR)
    elif dist2 <= 0:
        print("Sensor 2 failed")
        voices.play(Voice.DISTANCE_SENSOR_FAILURE)
        arduino.tankDrive(0,0)
        distanceSensorsTimer.stop()
    elif dist2 < 1000:
        pid2.update(dist2)
        driveRight = int(pid2.output)
        if driveRight > 100:
            driveRight = 100
        if driveRight < -100:
            driveRight = -100
        driveRight = - driveRight #
        # print("sensor2", dist2, driveRight)
    else:
        pass
    if driveLeft is not None and driveRight is not None:
        arduino.tankDrive(driveLeft, driveRight)
    else:
        arduino.tankDrive(0, 0)
    if dist1 == pid.SetPoint and dist2 == pid2.SetPoint:
        voices.play(Voice.ARRIVED) #didnt use
        distanceSensorsTimer.stop()
        arduino.tankDrive(0,0)

def initDistanceSensors(shutdownPins):
    global distanceSensors, pid, pid2
    distanceSensors = DistanceSensors(shutdownPins)
    pid = PID(0.2, 0, 0)
    pid.SetPoint = safeDistaces[safeDistacesIndex]
    pid.setSampleTime(0.02)
    pid2 = PID(0.2, 0, 0)
    pid2.SetPoint = safeDistaces[safeDistacesIndex]
    pid2.setSampleTime(0.02)

def incrementSafeDistance():
    global safeDistaces, safeDistacesIndex, pid
    if pid is not None:
        if safeDistacesIndex < len(safeDistaces) - 1:
            safeDistacesIndex += 1
            pid.SetPoint = safeDistaces[safeDistacesIndex]
            pid2.SetPoint = safeDistaces[safeDistacesIndex]
            startSafeDistance()
    else:
        print("pid is None. incrementSafeDistance() did nothing.")

def decrementSafeDistance():
    global safeDistaces, safeDistacesIndex, pid
    if pid is not None:
        if safeDistacesIndex > 0:
            safeDistacesIndex -= 1
            pid.SetPoint = safeDistaces[safeDistacesIndex]
            pid2.SetPoint = safeDistaces[safeDistacesIndex]
            startSafeDistance()
    else:
        print("pid is None. decrementSafeDistance() did nothing.")

def startSafeDistance():
    global distanceSensors, distanceSensorsTimer
    if distanceSensors == None:
        initDistanceSensors([29, 31])
        distanceSensorsTimer.timeout.connect(distanceSensorLoop)
    if not distanceSensorsTimer.isActive():
        distanceSensorsTimer.start(20)
        voices.play(Voice.APPROACH_BIN)

def stopSafeDistance():
    global distanceSensors, distanceSensorsTimer
    if distanceSensors != None and distanceSensorsTimer.isActive():
        distanceSensorsTimer.stop()
        voices.play(Voice.STOP_APPROACH_BIN)
        arduino.drive(0, 0)


if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)
    timer.timeout.connect(haveHeardFromControllerSlot)
    if initXbox360():
        xboxTimer.timeout.connect(loopXbox360Tinker)
        xboxTimer.start(50)
    else:
        server = RobotServer()
        server.gotManualMessage.connect(gotManualMessageSplot)
        server.gotAutomaticMessage.connect(gotAutomaticMessageSplot)
        server.gotSystemMessage.connect(gotSystemMessageSplot)
        server.gotSensorMessage.connect(gotSensorMessageSplot)
        server.controllerDisconnected.connect(controllerDisconnectedSlot)
        server.tcpServer.newConnection.connect(controllerConnectedSlot)
    app.exec()
