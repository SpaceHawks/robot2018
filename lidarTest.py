import platform
from distance_sensor import *
from xbox360 import Xbox360
from arduino import Arduino, FakeArduino
from PID import PID
from lidar_tools import RMCRpLidar, LidarGUI, RMCHokuyoLidar
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

gear = [20, 40, 60, 80, 100]
gearIndex = 0

arduino = None

stillAliveTimer = QtCore.QTimer()
xboxTimer = QtCore.QTimer()
distanceSensorsTimer = QtCore.QTimer()
lidarTimer = QtCore.QTimer()
goToTimer = QtCore.QTimer()
correctOrientationTimer = QtCore.QTimer()

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

orientatinPID = PID(1, 0, 0)
goToPID = PID(0.2, 0.15, 0.03)

orientatinPID.SetPoint = 0
orientatinPID.setSampleTime(0.2)
goToPID.SetPoint = 0
goToPID.setSampleTime(0.2)

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
exceedAngleLimit = None
#PID tunings

wheelsParam = None
tilterParam = None
sliderParam = None
augerParam = None



#xbox 360
def initXbox360():
    global xboxController, arduino, xboxTimer, ui
    if xboxController == None:
        xboxController = Xbox360(arduino)
    if xboxController.init() == True:
        xboxTimer.timeout.connect(xboxController.update)
        xboxTimer.start(1)
        ui.statusBar.setText("Connected to Xbox controller.")
        ui.statusBar.setStyleSheet('color: green')
        return True
    else:
        ui.statusBar.setText("No XBox controller is detected.")
        ui.statusBar.setStyleSheet('color: red')
        xboxController = None
        return False

def destroyXbox360():
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

def startSafeDistance():
    global distanceSensors, distanceSensorsTimer, shutdownPins
    if distanceSensors == None:
        initDistanceSensors()
    if not distanceSensorsTimer.isActive():
        distanceSensorsTimer.start(20)
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
        ui.statusBar.setText("Stopped Self-alignment")
        ui.statusBar.setStyleSheet('color: orange')
#lidar gui
def initLidarGui():
    global app, ui, mw, haha, tilterPosParam, tilterSpeedParam, zeroAngleParam, maxAngleParam, zeroDistanceParam, maxTurnParam, maxDriveParam, arduinoSpeedLimitParam, wheelsParam, tilterParam, sliderParam, augerParam
    ui = LidarGUI()
    ui.params.param('Commands', 'XBox Controller On').sigActivated.connect(initXbox360)
    ui.params.param('Commands', 'XBox Controller Off').sigActivated.connect(destroyXbox360)
    ui.params.param('Commands', 'Emergency Stop').sigActivated.connect(emergencyStop)
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

    ui.params.param('Self-Alignment PID', 'Kp').sigValueChanged.connect(lambda param: (PIDs[0].setKp(param.value()), (PIDs[1].setKp(param.value()))))
    ui.params.param('Self-Alignment PID', 'Ki').sigValueChanged.connect(lambda param: (PIDs[0].setKi(param.value()), (PIDs[1].setKi(param.value()))))
    ui.params.param('Self-Alignment PID', 'Kd').sigValueChanged.connect(lambda param: (PIDs[0].setKd(param.value()), (PIDs[1].setKd(param.value()))))
    ui.params.param('Self-Alignment PID', 'Sample Time').sigValueChanged.connect(lambda param: (PIDs[0].setSampleTime(param.value()), (PIDs[1].setSampleTime(param.value()))))
    ui.params.param('Self-Alignment PID', 'Set Distance').sigValueChanged.connect(lambda param: _setDistance(param.value()))
    ui.params.param('Self-Alignment PID', 'Start').sigActivated.connect(startSafeDistance)
    ui.params.param('Self-Alignment PID', 'Stop').sigActivated.connect(stopSafeDistance)

    ui.params.param('Timers', 'stillAliveTimer').sigValueChanged.connect(lambda param: stillAliveTimer.setInterval(param.value()))
    ui.params.param('Timers', 'xboxTimer').sigValueChanged.connect(lambda param: xboxTimer.setInterval(param.value()))
    ui.params.param('Timers', 'distanceSensorsTimer').sigValueChanged.connect(lambda param: distanceSensorsTimer.setInterval(param.value()))
    ui.params.param('Timers', 'lidarTimer').sigValueChanged.connect(lambda param: lidarTimer.setInterval(param.value()))
    ui.params.param('Timers', 'goToTimer').sigValueChanged.connect(lambda param: goToTimer.setInterval(param.value()))
    ui.params.param('Timers', 'correctOrientationTimer').sigValueChanged.connect(lambda param: correctOrientationTimer.setInterval(param.value()))
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

    wheelsParam.setValue([1, 2, 3, 4])
    tilterParam.setValue([50,60])
    sliderParam.setValue(80)

    augerParam.sigForwardClicked.connect(lambda: print("forward"))
    augerParam.sigBackwardClicked.connect(lambda: print("backward"))
    augerParam.sigStopClicked.connect(lambda: print("Auger stop"))

    tilterParam.sigChanged.connect(lambda value: print(value))
    sliderParam.sigChanged.connect(lambda value: print(value))

    ui.showMaximized()
    ui.show()

def initLidar():
    global lidar, lidarTimer, ui, goToTimer
    if platform.system() == "Darwin":
        port = '/dev/tty.SLAB_USBtoUART'
    elif platform.system() == "Linux":
        port = '/dev/ttyUSB0'
    else:
        port = 'COM3'
    # lidar = RMCHokuyoLidar(ui)
    lidar = RMCRpLidar(port, ui)
    correctOrientationTimer.timeout.connect(correctOrientation)
    lidar.lidarStarted.connect(lambda: lidarTimer.start(10))
    # lidar.lidarStarted.connect(goTo)
    lidar.lidarStopped.connect(lidarTimer.stop)
    lidar.lidarStopped.connect(goToTimer.stop)
    lidar.lidarStopped.connect(arduino.stop)
    lidarTimer.timeout.connect(lidar.update)
    ui.arenaWidget.pathAdded.connect(lambda: goToTimer.start(10))
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

#self moving
# def goTo():
#     if goToTimer.isActive():
#         goToTimer.stop()
#     goToTimer.start()

def correctOrientation():
    global arduino, lidar, ui
    if lidar.newPos:
        angleDiff = lidar.angleDiffTo(currentTarget)
        ui.labelAngleError.setText("Angle Error: "+str(int(angleDiff)) + " degrees")
        if abs(angleDiff) > maxAngle: #correct it
            orientatinPID.update(angleDiff)
            speed = orientatinPID.output
            if speed > speedLimit: speed = speedLimit
            if speed < -speedLimit: speed = -speedLimit
            if speed > 0:
                arduino.left(int(speed))
                ui.labelStatus.setText("Left: " + str(int(speed)))
                pass
            else:
                arduino.right(int(-speed))
                ui.labelStatus.setText("Right: " + str(int(-speed)))
                pass
        else: #it's ready
            pass
            ui.labelStatus.setText("See target, stop auto orient")
            correctOrientationTimer.stop()
            goToTimer.start(10)

def goTo():
    global arduino, lidar, ui, currentTarget, goToTimer, speedLimit, exceedAngleLimit
    if currentTarget == None:
        if not ui.arenaWidget.path.empty():
            coordinate = ui.arenaWidget.path.queue[0]
            coordinateItem = ui.arenaWidget.pathPointItems.queue[0]
            coordinateItem.setBrush(pg.mkBrush('g'))
            currentTarget = (coordinate.x(), coordinate.y())
            arduinoSpeedLimitParam.setValue(100)
        else:
            goToTimer.stop()
            arduinoSpeedLimitParam.setValue(20)
    elif lidar.newPos:
        remainDistance, angleDiff, usingTail = lidar.getDriveParams(currentTarget)
        ui.arenaWidget.labelRemainingDistance.setText("Remaining Distance: "+str(int(remainDistance)) + " mm")
        ui.arenaWidget.labelAngleError.setText("Angle Error: "+str(int(angleDiff)) + " degrees")
        if remainDistance < zeroDistanceParam.value():#arrived
            goToPID.clear()
            orientatinPID.clear()
            ui.arenaWidget.labelStatus.setText("Arrived")
            ui.arenaWidget.arrive()
            arduino.stop()
            currentTarget = None
        else: #not arrived yet
            goToPID.update(remainDistance)
            orientatinPID.update(angleDiff)
            drive = -goToPID.output
            turn = -orientatinPID.output
            if drive > maxDriveParam.value(): drive = maxDriveParam.value()
            if drive < -maxDriveParam.value(): drive = -maxDriveParam.value()
            if turn > maxTurnParam.value(): turn = maxTurnParam.value()
            if turn < -maxTurnParam.value(): turn = -maxTurnParam.value()
            if abs(angleDiff) > maxAngleParam.value():
                exceedAngleLimit = True
                arduino.turn(int(turn))
            elif abs(angleDiff) > zeroAngleParam.value():
                if exceedAngleLimit:
                    arduino.turn(int(turn))
                else:
                    arduino.drive(int(drive), int(turn), forced=False, usingTail=usingTail)
            else: #angle diff is zero
                exceedAngleLimit = False
                arduino.drive(int(drive), int(turn), forced=False, usingTail=usingTail)
            ui.arenaWidget.labelStatus.setText("Drive: "+ str(int(drive))+", Turn: "+ str(int(turn)))

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
    ui.arenaWidget.clearPath()
    goToTimer.stop()
    correctOrientationTimer.stop()
    destroyXbox360()
    distanceSensorsTimer.stop()
    arduino.stop()
    ui.statusBar.setText("E-Stop pressed.")
    ui.statusBar.setStyleSheet('color: green')

goToTimer.timeout.connect(goTo)
correctOrientationTimer.timeout.connect(correctOrientation)
if __name__ == '__main__':
    print("Running lidarTest.py")
    app = QtGui.QApplication([""])
    initArduino()
    arduino.setSpeedLimit(20)
    # initXbox360()
    initLidarGui()
    initLidar()
    ui.arenaWidget.keyPressed.connect(keyPressHandler)
    ui.arenaWidget.keyReleased.connect(keyReleaseHandler)
    pg.QtGui.QApplication.exec_()