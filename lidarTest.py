import platform
from distance_sensor import *
from xbox360 import Xbox360
from arduino import Arduino, FakeArduino
from PID import PID
from lidar_tools import RMCRpLidar, LidarGUI, RMCHokuyoLidar
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
# import ASUS.GPIO as GPIO

gear = [20, 40, 60, 80, 100]
gearIndex = 0

arduino = None

stillAliveTimer = QtCore.QTimer()
xboxTimer = QtCore.QTimer()
distanceSensorsTimer = QtCore.QTimer()
lidarTimer = QtCore.QTimer()
#CHANGE 3
rockLidarTimer = QtCore.QTimer()

goToTimer = QtCore.QTimer()
feedbackTimer = QtCore.QTimer()

ui = None
mw = None

lidar = None
rock_lidar = None

turn = 0
drive = 0

xboxController = None

safeDistaces = [100, 200, 300, 400, 500, 600, 700]
safeDistacesIndex = 3
distanceSensors = None
shutdownPins = [29, 31]
server = None
PIDs = [None]*2
PIDs[0] = PID(0.1, 0.109, 0.00005)
PIDs[1] = PID(0.1, 0.109, 0.00005)

orientatinPID = PID(2, 0.1, 0)
goToPID = PID(0.015, 1.55, 0)
spinPID = PID(2, 0, 0)

orientatinPID.SetPoint = 0
orientatinPID.setSampleTime(0.2)

goToPID.SetPoint = 0
goToPID.setSampleTime(0.2)

spinPID.SetPoint = 0
spinPID.setSampleTime(0.2)

maxAngleWhenMoving = 30
maxAngle = 5 #deegrees
maxDistance = 100

currentTarget = None
speedLimit = 20

lastKeyDroveMotor = None

tilterPosParam = None
tilterSpeedParam = None

zeroAngleParam = None
maxAngleParam = None
zeroDistanceParam = None
maxTurnParam = None
maxDriveParam = None
arduinoSpeedLimitParam = None

stillAliveTimerParam = None
xboxTimerPar = None
distanceSensorsTimerParam = None
lidarTimerPara = None
goToTimerPara = None
feedbackTimerParam = None


exceedAngleLimit = None
#PID tunings

wheelsParam = None
tilterParam = None
sliderParam = None
augerParam = None

currentLeftDistanceParam = None
currentRightDistanceParam = None


#Feedback from motor driving system
def arduinoFeedback():
    global arduino, feedbackTimer, ui, wheelsParam
    arduino.requestWheelSpeed()
    data = arduino.read(4)
    while data is not None:
        speeds = [0]*4
        for i in range(len(data)):
            if data[i]>126 and data[i]<257:
                speeds[i] = data[i] - 256
            else:
                speeds[i] = data[i]
        if data[0] == 3:#pos feedback
            if data[1] == 10 or data[1] == 20: #front wheels speed
                wheelsParam.setValue(speeds)
            elif data[1] == 5:# la pair
                pass
        data = arduino.read(4)
    # tilterParam.setValue([0,0])
    # sliderParam.setValue(80)

#xbox 360
def initXbox360():
    global xboxController, arduino, xboxTimer, ui
    if xboxController == None:
        xboxController = Xbox360(arduino)
    if xboxController.init() == True:
        xboxTimer.timeout.connect(xboxController.update)
        xboxTimer.start()
        ui.statusBar.setText("Connected to Xbox controller.")
        ui.statusBar.setStyleSheet('color: green')
        return True
    else:
        ui.statusBar.setText("No XBox controller is detected.")
        ui.statusBar.setStyleSheet('color: red')
        xboxController = None
        return False

def quitXbox360():
    global xboxController, xboxTimer
    if xboxTimer.isActive() and xboxController is not None:
        xboxTimer.timeout.disconnect(xboxController.update)
        xboxTimer.stop()
        xboxController.quit()
        xboxController = None
        ui.statusBar.setText("Disconnected from Xbox Controller.")
        ui.statusBar.setStyleSheet('color: green')
    else:
        ui.statusBar.setText("No XBox controller was connected.")
        ui.statusBar.setStyleSheet('color: orange')

#distance sensor
def updateDistance():
    global distanceSensors, PIDs, ui, currentTarget, currentLeftDistanceParam, currentRightDistanceParam
    drives = [None]*2 # left and right
    distanceSensors.update()
    dists = [distanceSensors.distances[0], distanceSensors.distances[1]] #left and right
    currentLeftDistanceParam.setValue(dists[0])
    currentRightDistanceParam.setValue(dists[1])
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
            drives[i] = drives[i]
        else:
            print("updateDistance: Got unexpected distance", i, ":", dists[i])
    if drives[0] is not None and drives[1] is not None:
        arduino.tankDrive(drives[0], drives[1])
    else:
        arduino.stop()
    if abs(dists[0] - PIDs[0].SetPoint) < 5 and abs(dists[1] - PIDs[1].SetPoint) < 5:
        message = "updateDistance: Arrived" + "left dist: " + str(dists[0]) + "right dist: " + str(dists[1]) + "SetPoint: " + str(PIDs[0].SetPoint)
        ui.statusBar.setText(message)
        ui.statusBar.setStyleSheet('color: red')
        stopSafeDistance()
        # ui.arenaWidget.arrive()
        #currentTarget = None

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
    _setDistance(safeDistaces[newDistance])

def _setDistance(newDistance):
    global PIDs
    if newDistance >= 50 and newDistance <= 1000:
        PIDs[0].SetPoint = newDistance
        PIDs[1].SetPoint = newDistance
        startSafeDistance()
        ui.statusBar.setText("New distance:" + str(newDistance))
        ui.statusBar.setStyleSheet('color: yellow')
    else:
        ui.statusBar.setText("Set distance is out of range: " + str(newDistance) + "Only [50, 1000] is accepted!")
        ui.statusBar.setStyleSheet('color: red')

def startSafeDistance(distance = None):
    if distance is not None:
        _setDistance(distance)
    global distanceSensors, distanceSensorsTimer, shutdownPins, arduino
    if distanceSensors == None:
        initDistanceSensors()
    if not distanceSensorsTimer.isActive():
        arduino.setSpeedLimit(15)
        distanceSensorsTimer.start()
        ui.statusBar.setText("Self-alignment started")
        ui.statusBar.setStyleSheet('color: green')
    else:
        ui.statusBar.setText("Self-alignment has already been started")
        ui.statusBar.setStyleSheet('color: orange')

def stopSafeDistance():
    global distanceSensorsTimer, arduino
    if distanceSensorsTimer.isActive():
        distanceSensorsTimer.stop()
        arduino.stop()
        arduino.setSpeedLimit(20)
        ui.statusBar.setText("Stopped Self-alignment")
        ui.statusBar.setStyleSheet('color: orange')
#lidar gui
def initLidarGui():
    global app, ui, mw, haha, tilterPosParam, tilterSpeedParam, zeroAngleParam, maxAngleParam, zeroDistanceParam, maxTurnParam, maxDriveParam, arduinoSpeedLimitParam, wheelsParam, tilterParam, sliderParam, augerParam, currentLeftDistanceParam, currentRightDistanceParam, feedbackTimer
    ui = LidarGUI()
    ui.params.param('Commands', 'XBox Controller On').sigActivated.connect(initXbox360)
    ui.params.param('Commands', 'XBox Controller Off').sigActivated.connect(quitXbox360)
    ui.params.param('Commands', 'Emergency Stop').sigActivated.connect(emergencyStop)
    ui.params.param('Commands', 'Get Path').sigActivated.connect(getPath)
    arduinoSpeedLimitParam = ui.params.param('Arduino Settings', 'Speed Limit')
    arduinoSpeedLimitParam.sigValueChanged.connect(lambda param: arduino.setSpeedLimit(param.value()))
    ui.setWindowTitle("RMC LIDAR Testing Sofware")
    ui.eStopPressed.connect(emergencyStop)
    #PID param
    ui.params.param('Orientation PID', 'Kp').sigValueChanged.connect(lambda param: orientatinPID.setKp(param.value()))
    ui.params.param('Orientation PID', 'Ki').sigValueChanged.connect(lambda param: orientatinPID.setKi(param.value()))
    ui.params.param('Orientation PID', 'Kd').sigValueChanged.connect(lambda param: orientatinPID.setKd(param.value()))
    ui.params.param('Orientation PID', 'Sample Time').sigValueChanged.connect(lambda param: orientatinPID.setSampleTime(param.value()))
    zeroAngleParam = ui.params.param('Orientation PID', 'Zero Angle')
    maxAngleParam = ui.params.param('Orientation PID', 'Max Angle')

    ui.params.param('Distance PID', 'Kp').sigValueChanged.connect(lambda param: goToPID.setKp(param.value()))
    ui.params.param('Distance PID', 'Ki').sigValueChanged.connect(lambda param: goToPID.setKi(param.value()))
    ui.params.param('Distance PID', 'Kd').sigValueChanged.connect(lambda param: goToPID.setKd(param.value()))
    ui.params.param('Distance PID', 'Sample Time').sigValueChanged.connect(
        lambda param: goToPID.setSampleTime(param.value()))
    zeroDistanceParam = ui.params.param('Distance PID', 'Zero Distance')
    maxTurnParam = ui.params.param('Distance PID', 'Max Turn')
    maxDriveParam = ui.params.param('Distance PID', 'Max Drive')

    ui.params.param('Spin PID', 'Kp').sigValueChanged.connect(lambda param: spinPID.setKp(param.value()))
    ui.params.param('Spin PID', 'Ki').sigValueChanged.connect(lambda param: spinPID.setKi(param.value()))
    ui.params.param('Spin PID', 'Kd').sigValueChanged.connect(lambda param: spinPID.setKd(param.value()))
    ui.params.param('Spin PID', 'Sample Time').sigValueChanged.connect(
        lambda param: spinPID.setSampleTime(param.value()))

    ui.params.param('Self-Alignment PID', 'Kp').sigValueChanged.connect(lambda param: (PIDs[0].setKp(param.value()), (PIDs[1].setKp(param.value()))))
    ui.params.param('Self-Alignment PID', 'Ki').sigValueChanged.connect(lambda param: (PIDs[0].setKi(param.value()), (PIDs[1].setKi(param.value()))))
    ui.params.param('Self-Alignment PID', 'Kd').sigValueChanged.connect(lambda param: (PIDs[0].setKd(param.value()), (PIDs[1].setKd(param.value()))))
    ui.params.param('Self-Alignment PID', 'Sample Time').sigValueChanged.connect(lambda param: (PIDs[0].setSampleTime(param.value()), (PIDs[1].setSampleTime(param.value()))))
    ui.params.param('Self-Alignment PID', 'Set Distance').sigValueChanged.connect(lambda param: _setDistance(param.value()))
    currentLeftDistanceParam = ui.params.param('Self-Alignment PID', 'Current Left Distance')
    currentRightDistanceParam = ui.params.param('Self-Alignment PID', 'Current Right Distance')
    ui.params.param('Self-Alignment PID', 'Start').sigActivated.connect(startSafeDistance)
    ui.params.param('Self-Alignment PID', 'Stop').sigActivated.connect(stopSafeDistance)


    #timers
    stillAliveTimerParam = ui.params.param('Timers', 'stillAliveTimer')
    xboxTimerParam = ui.params.param('Timers', 'xboxTimer')
    distanceSensorsTimerParam = ui.params.param('Timers', 'distanceSensorsTimer')
    lidarTimerParam = ui.params.param('Timers', 'lidarTimer')
    goToTimerParam = ui.params.param('Timers', 'goToTimer')
    feedbackTimerParam= ui.params.param('Timers', 'feedbackTimer')

    stillAliveTimerParam.sigValueChanged.connect(lambda param: stillAliveTimer.setInterval(param.value()))
    xboxTimerParam.sigValueChanged.connect(lambda param: xboxTimer.setInterval(param.value()))
    distanceSensorsTimerParam.sigValueChanged.connect(lambda param: distanceSensorsTimer.setInterval(param.value()))
    lidarTimerParam.sigValueChanged.connect(lambda param: lidarTimer.setInterval(param.value()))
    goToTimerParam.sigValueChanged.connect(lambda param: goToTimer.setInterval(param.value()))
    feedbackTimerParam.sigValueChanged.connect(lambda param: feedbackTimer.setInterval(param.value()))

    stillAliveTimerParam.setValue(500)
    xboxTimerParam.setValue(1)
    distanceSensorsTimerParam.setValue(200)
    lidarTimerParam.setValue(10)
    goToTimerParam.setValue(10)
    feedbackTimerParam.setValue(100)


    tilterPosParam = ui.params.param('Mining Controls', 'Tilter Position')
    tilterSpeedParam = ui.params.param('Mining Controls', 'Tilter Speed')
    tilterPosParam.sigValueChanged.connect(lambda param: arduino.tilterPosAndSpeed(tilterPosParam.value(), tilterSpeedParam.value()))
    tilterSpeedParam.sigValueChanged.connect(lambda param: arduino.tilterPosAndSpeed(tilterPosParam.value(), tilterSpeedParam.value()))

    ui.params.param('Mining Controls', 'Forward').sigActivated.connect(arduino.augerForward)
    ui.params.param('Mining Controls', 'Reverse').sigActivated.connect(arduino.augerReverse)
    ui.params.param('Mining Controls', 'Stop').sigActivated.connect(arduino.augerStop)

    wheelsParam = ui.params.param('Arduino Settings', 'Wheel Speed')
    tilterParam = ui.params.param('Arduino Settings', 'Tilter Position')
    sliderParam = ui.params.param('Arduino Settings', 'Slider Position')
    augerParam = ui.params.param('Arduino Settings', 'Auger')
    ui.params.param('Arduino Settings', 'Reset').sigActivated.connect(arduino.reset)
    ui.params.param('Arduino Settings', 'Shutdown Motors').sigActivated.connect(arduino.shutDownWheels)

    augerParam.sigForwardClicked.connect(arduino.augerForward)
    augerParam.sigReverseClicked.connect(arduino.augerReverse)
    augerParam.sigStopClicked.connect(arduino.augerStop)

    tilterParam.sigChanged.connect(lambda value: arduino.tilterPosAndSpeed(value,100))
    sliderParam.sigChanged.connect(lambda value: print(value))

    ui.showMaximized()
    ui.show()

#CHANGE 1
def initRpLidar():
    global rockLidarTimer, ui, goToTimer, rock_lidar, lidar
    if platform.system() == "Darwin":
        port = '/dev/tty.SLAB_USBtoUART'
    elif platform.system() == "Linux":
        port = '/dev/ttyUSB0'
    else:
        port = 'COM3'
    rock_lidar = RMCRpLidar(port, ui)
    rock_lidar._setHokuyoLidar(lidar)
    rock_lidar.lidarStarted.connect(lambda: rockLidarTimer.start())
    rock_lidar.lidarStopped.connect(rockLidarTimer.stop)
    rockLidarTimer.timeout.connect(rock_lidar.detectRocks)

def initLidar():
    global lidar, lidarTimer, ui, goToTimer
    if platform.system() == "Darwin":
        port = '/dev/tty.SLAB_USBtoUART'
    elif platform.system() == "Linux":
        port = '/dev/ttyUSB0'
    else:
        port = 'COM3'
    lidar = RMCHokuyoLidar(ui)
    lidar.lidarStarted.connect(lambda: lidarTimer.start())
    lidar.lidarStopped.connect(lidarTimer.stop)
    lidar.lidarStopped.connect(goToTimer.stop)
    lidar.lidarStopped.connect(arduino.stop)
    lidarTimer.timeout.connect(lidar.update)
    ui.arenaWidget.pathAdded.connect(lambda: goToTimer.start())
    ui.arenaWidget.pathCleared.connect(clearCurrentTarget)

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

def goTo():
    global arduino, lidar, ui, currentTarget, goToTimer, speedLimit, exceedAngleLimit, spinPID
    if currentTarget == None:
        if not ui.arenaWidget.path.empty():
            coordinate = ui.arenaWidget.path.queue[0]
            coordinateItem = ui.arenaWidget.pathPointItems.queue[0]
            coordinateItem.setBrush(pg.mkBrush('g'))
            currentTarget = (coordinate.x(), coordinate.y())
            arduinoSpeedLimitParam.setValue(15)
        else:
            arduino.stop()
            goToTimer.stop()
            arduinoSpeedLimitParam.setValue(20)
    elif currentTarget[0] == 0 and currentTarget[1] == 0: #check for Bin closeliness
        goToTimer.stop()
        goToPID.clear()
        orientatinPID.clear()
        spinPID.clear()
        ui.arenaWidget.labelStatus.setText("Self-Alignment activated")
        arduino.stop()
        startSafeDistance(distance=100)
    elif lidar.newPos:
        nextRemainDistance, angleDiff, usingTail = lidar.getDriveParams(currentTarget)
        remainDistance = lidar.distanceAlong(ui.arenaWidget.path.queue)
        ui.arenaWidget.labelRemainingDistance.setText("Remaining Distance: "+str(int(remainDistance)) + " mm")
        ui.arenaWidget.labelAngleError.setText("Angle Error: "+str(int(angleDiff)) + " degrees")
        ui.arenaWidget.labelXY.setText("(x,y): "+str(lidar.getXY()))
        ui.arenaWidget.labelOrientation.setText("Orientation: "+str(lidar.robotOrientation) + " degrees")
        if nextRemainDistance < zeroDistanceParam.value():#arrived
            # goToPID.clear()
            # orientatinPID.clear()
            # spinPID.clear()
            ui.arenaWidget.labelStatus.setText("Arrived")
            ui.arenaWidget.arrive()
            # arduino.stop()
            currentTarget = None
        else: #not arrived yet
            if abs(angleDiff) > maxAngleParam.value():
                exceedAngleLimit = True
                goToPID.clear()
                orientatinPID.clear()
            elif abs(angleDiff) < zeroAngleParam.value():
                exceedAngleLimit = False
                spinPID.clear()
            else:
                pass
            if exceedAngleLimit: #spin
                spinPID.update(angleDiff)
                turn = bound(-spinPID.output, -maxTurnParam.value(), maxTurnParam.value())
                arduino.turn(turn)
                ui.arenaWidget.labelStatus.setText("Spin: "+str(turn))
            else:
                goToPID.update(remainDistance)
                orientatinPID.update(angleDiff)
                drive = bound(-goToPID.output, -maxDriveParam.value(), maxDriveParam.value())
                turn = bound(-orientatinPID.output, -maxTurnParam.value(), maxTurnParam.value())
                arduino.drive(drive, turn, forced=False, usingTail=usingTail)
                ui.arenaWidget.labelStatus.setText("Drive: "+ str(drive)+", Turn: "+ str(turn))
    else:
        pass
from clive import Pathfinding
def getPath():
    pathFinder = Pathfinding()
    #robotPos = lidar.robotPos
    robotPos = (2000,0)
    obstacleList = ui.arenaWidget.obstaclesCoord
    print("robotPos: ", robotPos)
    print("obstacleList: ", obstacleList)
    pathFinder.setData(True,robotPos,len(obstacleList),obstacleList)
    path = [robotPos]
    path += pathFinder.getData()
    path.insert(0, (0,robotPos[1]))
    path.append((6000,path[-1][1]))
    #path = [(0,0),(100,100),(300,200),(500,700),(900,1000)]
    ui.arenaWidget.addPaths(path)

def bound(value, lowerLimit, upperimit):
    if value > upperLimit: return upperLimit
    elif value < lowerLimit: return lowerLimit
    else: return int(value)

def keyPressHandler(event):
    global lastKeyDroveMotor
    if not event.isAutoRepeat():
        key = event.key()
        if key == pg.QtCore.Qt.Key_Up or key == pg.QtCore.Qt.Key_W:
            arduino.forward(20)
        elif key == pg.QtCore.Qt.Key_Down or key == pg.QtCore.Qt.Key_S:
            arduino.backward(20)
        elif key == pg.QtCore.Qt.Key_Left or key == pg.QtCore.Qt.Key_A:
            arduino.left(20)
        elif key == pg.QtCore.Qt.Key_Right or key == pg.QtCore.Qt.Key_D:
            arduino.right(20)
        elif key == pg.QtCore.Qt.Key_C:
            ui.arenaWidget.clearObstacle()
        elif key == pg.QtCore.Qt.Key_X:
            ui.arenaWidget.clearPath()
        elif key == pg.QtCore.Qt.Key_O:
            ui.arenaWidget.drawingMode = "obstacle"
        elif key == pg.QtCore.Qt.Key_Escape:
            ui.arenaWidget.drawingMode = "none"
        lastKeyDroveMotor = key

def keyReleaseHandler(event):
    global lastKeyDroveMotor
    if not event.isAutoRepeat():
        key = event.key()
        if key == lastKeyDroveMotor:
            if key == pg.QtCore.Qt.Key_Up or key == pg.QtCore.Qt.Key_W:
                arduino.stop()
            elif key == pg.QtCore.Qt.Key_Down or key == pg.QtCore.Qt.Key_S:
                arduino.stop()
            elif key == pg.QtCore.Qt.Key_Left or key == pg.QtCore.Qt.Key_A:
                arduino.stop()
            elif key == pg.QtCore.Qt.Key_Right or key == pg.QtCore.Qt.Key_D:
                arduino.stop()

def emergencyStop():
    stillAliveTimer.stop()
    xboxTimer.stop()
    distanceSensorsTimer.stop()
    lidarTimer.stop()
    goToTimer.stop()
    feedbackTimer.stop()
    ui.arenaWidget.clearPath()
    quitXbox360()
    arduino.stop()
    ui.statusBar.setText("E-Stop pressed.")
    ui.statusBar.setStyleSheet('color: green')

if __name__ == '__main__':
    print("Running lidarTest.py")
    app = QtGui.QApplication([""])
    initArduino()
    arduino.setSpeedLimit(20)
    initLidarGui()
    initLidar()
    initRpLidar()
    goToTimer.timeout.connect(goTo)
    feedbackTimer.timeout.connect(arduinoFeedback)
    ui.arenaWidget.keyPressed.connect(keyPressHandler)
    ui.arenaWidget.keyReleased.connect(keyReleaseHandler)
    # feedbackTimer.start()#miliseconds
    pg.QtGui.QApplication.exec_()
