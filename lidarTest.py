from arduino import Arduino
from distance_sensor import *
from PID import PID
from xbox360 import Xbox360

from lidar_tools import *
from rplidar import RPLidar
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

gear = [20, 40, 60, 80, 100]
gearIndex = 0

arduino = Arduino("/dev/ttyS1")

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
    ui.buttonConnectDisconnect.clicked.connect(connectDisconnect)
    mw.show()

def connectDisconnect():
    global lidar, ui
    if ui.buttonConnectDisconnect.text() == "Connect":
        if lidar == None and initLidar() == True:
            ui.buttonConnectDisconnect.setText("Disconnect")
    else:
        stopLidar()
        ui.buttonConnectDisconnect.setText("Connect")

def stopLidar():
    global lidarTimer, lidar
    lidarTimer.stop()
    if lidar is not None:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        lidar = None

def initLidar():
    global lidar, lidarTimer, ui
    try:
        # lidar = RPLidar('/dev/tty.SLAB_USBtoUART')
        lidar = RPLidar('/dev/ttyUSB0')
        info = lidar.get_info()
        print(info)
        health = lidar.get_health()
        print(health)
        iterator = lidar.iter_scans(max_buf_meas=2000)
        next(iterator)
        next(iterator)
        next(iterator)
        ui.iterator = iterator
        ui.lidarFailed.connect(stopLidar)
        lidarTimer.timeout.connect(ui.update)
        lidarTimer.start(1)  # update frequency
        return True
    except:
        print("Lidar failed, Check connection!")
        stopLidar()
        return False

goToTimer = QtCore.QTimer()
correctOrientationTimer = QtCore.QTimer()

maxAngle = 5 #deegrees

orientatinPID = PID(1, 0, 0)
goToPID = PID(0.1, 0, 0)

orientatinPID.SetPoint = 0
orientatinPID.setSampleTime(0.2)
goToPID.SetPoint = 0
goToPID.setSampleTime(0.2)

def goTo():
    if goToTimer.isActive():
        goToTimer.stop()
    correctOrientationTimer.start()

def correctOrientation():
    global arduino
    angleDiff = 30 #robot orientation - dest orientation
    if abs(angleDiff) > maxAngle: #correct it
        orientatinPID.update(angleDiff)
        speed = orientatinPID.output
        if speed > 100: speed = 100
        if speed < -100: speed = -100
        if speed > 0: arduino.right(abs(speed))
        else: arduino.left(abs(speed))
    else: #it's ready
        correctOrientationTimer.stop()
        goToTimer.start(10)

maxAngleWhenMoving = 10
maxDistance = 20
def _goTo():
    global arduino
    angleDiff = 30 #robot orientation - dest orientation
    remainDistance = 20
    if remainDistance < maxDistance:#arrived
        goToPID.clear()
        orientatinPID.clear()
        print("arrived")
    else: #not arrived yet
        if abs(angleDiff) > maxAngleWhenMoving: #correct it
            orientatinPID.clear()
            goToPID.clear()
            goToTimer.stop()
            correctOrientationTimer.start(10)
        else: #it's ready
            goToPID.update(remainDistance)
            orientatinPID.update(angleDiff)
            drive = goToPID.output
            turn = orientatinPID.output
            if turn > 100: turn = 100
            if drive > 100: drive = 100
            if turn < -100: turn = -100
            if drive < -100: drive = -100
            arduino.drive(drive, turn)

goToTimer.timeout.connect(_goTo)
correctOrientationTimer.timeout.connect(correctOrientation)
if __name__ == '__main__':
    print("Running lidarTest.py")
    app = QtGui.QApplication([""])
    initXbox360()
    initLidarGui()
    pg.QtGui.QApplication.exec_()