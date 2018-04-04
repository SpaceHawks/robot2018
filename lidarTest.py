import lidar_tools, platform
if platform.system() == "Linux":
    from distance_sensor import *
    from xbox360 import Xbox360

from arduino import Arduino, FakeArduino
from PID import PID
from lidar_tools import RMCLidar, LidarGUI
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

gear = [20, 40, 60, 80, 100]
gearIndex = 0

arduino = None

stillAliveTimer = QtCore.QTimer()
xboxTimer = QtCore.QTimer()
distanceSensorsTimer = QtCore.QTimer()
lidarTimer = QtCore.QTimer()

ui = None
mw = None

lidar = None

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

goToTimer = QtCore.QTimer()
correctOrientationTimer = QtCore.QTimer()


orientatinPID = PID(1, 0, 0)
goToPID = PID(0.1, 0, 0)

orientatinPID.SetPoint = 0
orientatinPID.setSampleTime(0.2)
goToPID.SetPoint = 0
goToPID.setSampleTime(0.2)

maxAngleWhenMoving = 30
maxAngle = 5 #deegrees
maxDistance = 20

currentTarget = None

#xbox 360
def initXbox360():
    global xboxController, arduino, xboxTimer
    if xboxController == None:
        xboxController = Xbox360(arduino)
    if xboxController.init() == True:
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

def stopSafeDistance():
    global distanceSensorsTimer, arduino
    if distanceSensorsTimer.isActive():
        distanceSensorsTimer.stop()
        arduino.stop()

#lidar gui
def initLidarGui():
    global app, ui, mw
    mw = QtGui.QMainWindow()
    mw.showMaximized()
    view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
    mw.setCentralWidget(view)
    ui = LidarGUI()
    ui.setupUI(view)
    mw.show()
def initLidar():
    global lidar, lidarTimer, ui, goToTimer
    if platform.system() == "Darwin":
        port = '/dev/tty.SLAB_USBtoUART'
    elif platform.system() == "Linux":
        port = '/dev/ttyUSB0'
    else:
        port = 'COM3'
    lidar = RMCLidar(port, ui)
    correctOrientationTimer.timeout.connect(correctOrientation)
    lidar.lidarStarted.connect(lambda: lidarTimer.start(10))
    # lidar.lidarStarted.connect(goTo)
    lidar.lidarStopped.connect(lidarTimer.stop)
    lidarTimer.timeout.connect(lidar.update)
    ui.pathAdded.connect(lambda: goToTimer.start(10))
    ui.pathCleared.connect(clearCurrentTarget)


def clearCurrentTarget():
    global currentTarget, arduino
    currentTarget = None
    arduino.stop()
#arduino
def initArduino():
    global arduino
    global lidar, lidarTimer
    if platform.system() == "Darwin":
        arduino = FakeArduino("/dev/ttyS1")
    else:
        arduino = Arduino("/dev/ttyS1")

#self moving
# def goTo():
#     if goToTimer.isActive():
#         goToTimer.stop()
#     goToTimer.start()

def correctOrientation():
    global arduino, lidar, ui
    if lidar.newPos:
        angleDiff = lidar.angleDiffTo((2000,0))
        if abs(angleDiff) > maxAngle: #correct it
            orientatinPID.update(angleDiff)
            speed = orientatinPID.output
            if speed > 100: speed = 100
            if speed < -100: speed = -100
            if speed > 0:
                # arduino.left(int(speed))
                ui.labelStatus.setText("Left: " + str(int(speed)))
                pass
            else:
                # arduino.right(int(-speed))
                ui.labelStatus.setText("Right: " + str(int(-speed)))
                pass
        else: #it's ready
            pass
            ui.labelStatus.setText("See target, stop auto orient")
            correctOrientationTimer.stop()
            goToTimer.start(10)
def goTo():
    global arduino, lidar, ui, currentTarget, goToTimer
    if currentTarget == None:
        if not ui.path.empty():
            coordinate = ui.path.queue[0]
            currentTarget = (coordinate.x(), coordinate.y())
        else:
            goToTimer.stop()
    elif lidar.newPos:
        angleDiff = lidar.angleDiffTo((2000,0))
        ui.labelStatus.setText(str(int(angleDiff)))
        remainDistance = lidar.robotDistance
        if remainDistance < maxDistance:#arrived
            goToPID.clear()
            orientatinPID.clear()
            ui.labelStatus.setText("Arrived")
            ui.arrive()
            currentTarget = None
        else: #not arrived yet
            if abs(angleDiff) > maxAngleWhenMoving: #correct it
                orientatinPID.clear()
                goToPID.clear()
                goToTimer.stop()
                correctOrientationTimer.start(10)
                ui.labelStatus.setText("Re-orienting")
            else: #it's ready
                goToPID.update(remainDistance)
                orientatinPID.update(angleDiff)
                drive = -goToPID.output
                turn = -orientatinPID.output
                if turn > 100: turn = 100
                if drive > 100: drive = 100
                if turn < -100: turn = -100
                if drive < -100: drive = -100
                # arduino.drive(int(drive), int(turn))
                ui.labelStatus.setText("Drive: "+ str(int(drive))+", Turn: "+ str(int(turn)))

goToTimer.timeout.connect(goTo)
correctOrientationTimer.timeout.connect(correctOrientation)
if __name__ == '__main__':
    print("Running lidarTest.py")
    app = QtGui.QApplication([""])
    initArduino()
    # initXbox360()
    initLidarGui()
    initLidar()
    pg.QtGui.QApplication.exec_()