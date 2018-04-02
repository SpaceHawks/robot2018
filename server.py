from PID import PID
from Tests.voice import Voice
from arduino import Arduino
from distance_sensor import *
from interface import *
from xbox360 import Xbox360

voices = Voice("audio")


arduino = Arduino("/dev/ttyS1")
positioning = False
stillAlive = False
gear = [20, 40, 60, 80, 100]
gearIndex = 0
stillAliveTimer =QTimer()
xboxTimer = QTimer()
distanceSensorsTimer = QTimer()
lidarTimer = QTimer()
lidar = None
ui = None
mw = None

turn = 0
drive = 0

xboxController = None


safeDistaces = [100, 200, 300, 400, 500, 600, 700]
safeDistacesIndex = 3
distanceSensors = None
shutdownPins = [29, 31]
server = None
PIDs = [None]*2
PIDs[0] = PID(0.2, 0, 0)
PIDs[1] = PID(0.2, 0, 0)

#tcp
def initTCP():
    global server
    if server == None:
        server = RobotServer()
        server.gotManualMessage.connect(processManualMessage)
        server.gotAutomaticMessage.connect(processAutoMessage)
        server.gotSystemMessage.connect(processSystemMessage)
        server.gotSensorMessage.connect(processSensorMessage)
        server.controllerDisconnected.connect(controllerDisconnected)
        server.tcpServer.newConnection.connect(controllerConnected)

def processManualMessage(message):
    global arduino
    if arduino.writeDirectly(message) is False:
        print("Manual control fail: ", MESAGE_STRUCT.unpack(message))
    else:
        # print("Manual control: ", MESAGE_STRUCT.unpack(message))
        pass

def processAutoMessage(decodedMessage):
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
            decrementDistance()
            s += " Decrement Distance"
        elif decodedMessage[2] == 3:
            incrementDistance()
            s += " Increment Distance"
    print(s)

def processSystemMessage(decodedMessage):
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
    # print(s)

def processSensorMessage(decodedMessage):
    print("processSensorMessage", decodedMessage)

def controllerDisconnected():
    global stillAliveTimer
    voices.play(Voice.DISCONNECTED)
    arduino.stop()
    print("controllerDisconnected: Stopped motors!")
    stillAliveTimer.stop()
    print("scontrollerDisconnected: Stopped tcp")

def controllerConnected():
    global stillAliveTimer
    # voices.play(Voice.CONNECTED)
    stillAliveTimer.timeout.connect(stillAliveCheck)
    stillAliveTimer.start(500)

def stillAliveCheck():
    global stillAlive, arduino
    if stillAlive:
        stillAlive = False
    else:
        arduino.stop()
        print("stillAliveCheck: Lost Controller")

#xbox 360
def initXbox360():
    global xboxController, arduino, xboxTimer
    if xboxController == None:
        xboxController = Xbox360(arduino)
    if xboxController.init() == True:
        # xboxController.motionLeft.connect(lambda: arduino.left(gear[gearIndex]))
        # xboxController.motionRight.connect(lambda: arduino.right(gear[gearIndex]))
        # xboxController.motionUp.connect(lambda: arduino.forward(gear[gearIndex]))
        # xboxController.motionDown.connect(lambda: arduino.backward(gear[gearIndex]))
        # xboxController.motionCenter.connect(arduino.stop)
        xboxTimer.timeout.connect(xboxController.update)
        xboxTimer.start(1)
        #special qconnect here
        return True
    else:
        print("No XBox controller is detected.")
        xboxController = None
        return False

#distance sensor
def updateDistance():
    global distanceSensors, PIDs
    drives = [None]*2 # left and right
    distanceSensors.update()
    dists = [distanceSensors.distances[0], distanceSensors.distances[1]] #left and right
    for i in range(2):
        if dists[i] > 8000:
            pass
        elif dists[i] <= 0:
            print("updateDistance: Sensor 1 failed")
            # voices.play(Voice.DISTANCE_SENSOR_FAILURE)
            stopSafeDistance()
            distanceSensors.stop()
            distanceSensors = None
            return
        elif dists[i] < 1000:
            PIDs[i].update(dists[i])
            drives[i] = int(PIDs[i].output)
            if drives[i] > 100:
                drives[i] = 100
            if drives[i] < -100:
                drives[i] = -100
            drives[i] = - drives[i]
        else:
            print("updateDistance: Got unexpected distance", i, ":", dists[i])
    if drives[0] is not None and drives[1] is not None:
        arduino.tankDrive(drives[0], drives[1])
    else:
        arduino.stop()
    if abs(dists[0] - PIDs[0].SetPoint) < 10 and abs(dists[1] - PIDs[1].SetPoint) < 10:
        print("updateDistance: Arrived", "left dist: ", dists[0], "right dist: ", dists[1], "SetPoint: ", PIDs[0].SetPoint)
        # voices.play(Voice.ARRIVED) #didnt use
        stopSafeDistance()

def initDistanceSensors():
    global shutdownPins, distanceSensors, PIDs, safeDistaces, distanceSensorsTimer
    if distanceSensors == None:
        distanceSensors = DistanceSensors(shutdownPins)
        for i in range(len(PIDs)):
            PIDs[i].SetPoint = safeDistaces[safeDistacesIndex]
            PIDs[i].setSampleTime(0.02)
        distanceSensorsTimer.timeout.connect(updateDistance)

def incrementDistance():
    global safeDistaces, safeDistacesIndex
    if safeDistacesIndex < len(safeDistaces) - 1:
        safeDistacesIndex += 1
        setDistance(safeDistaces[safeDistacesIndex])
    else:
        print("incrementDistance: Robot is already at max distance.")

def decrementDistance():
    global safeDistaces, safeDistacesIndex
    if safeDistacesIndex > 0:
        safeDistacesIndex -= 1
        setDistance(safeDistaces[safeDistacesIndex])
    else:
        print("decrementDistance: Robot is already at min distance.")

def setDistance(newDistance):
    global PIDs
    if newDistance >= 50 and newDistance <= 1000:
        PIDs[0].SetPoint = safeDistaces[newDistance]
        PIDs[1].SetPoint = safeDistaces[newDistance]
        startSafeDistance()
    else:
        print("setDistance: Distance out of range [50, 1000].")

def startSafeDistance():
    global distanceSensors, distanceSensorsTimer, shutdownPins
    if distanceSensors == None:
        initDistanceSensors()
    if not distanceSensorsTimer.isActive():
        distanceSensorsTimer.start(20)
        voices.play(Voice.APPROACH_BIN)

def stopSafeDistance():
    global distanceSensorsTimer, arduino
    if distanceSensorsTimer.isActive():
        distanceSensorsTimer.stop()
        # voices.play(Voice.STOP_APPROACH_BIN)
        arduino.stop()

if __name__ == '__main__':
    print("Running server.py")
    import sys
    app = QCoreApplication(sys.argv)
    if not initXbox360():
        initTCP()
    app.exec_()
