# import pyqtgraph.examples
# pyqtgraph.examples.run()

# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Update a simp
le plot as rapidly as possible to measure speed.
"""


from pyqtgraph.Qt import QtGui, QtCore# (the example applies equally well to PySide)
import pyqtgraph as pg
import numpy as np
from rplidar import RPLidar


def markerDirection(firstPoint, lastPoint):
    direction = np.degrees(np.arctan2(lastPoint[1] - firstPoint[1], lastPoint[0] - firstPoint[0])) + 90 #maker slope angle + 90
    return standardizeAngle(direction)

def directionFromMidMarkerToOrigin(firstPoint, lastPoint):
    midX = (firstPoint[0] + lastPoint[0])/2
    midY = (firstPoint[1] + lastPoint[1])/2
    return np.degrees(np.arctan2(-midY, -midX))

def distanceFromMidMarkerToOrigin(firstPoint, lastPoint):
    midX = (firstPoint[0] + lastPoint[0])/2
    midY = (firstPoint[1] + lastPoint[1])/2
    return np.sqrt(midX*midX+midY*midY)

def standardizeAngle(angle): #only degrees
    angle %= 360
    if angle > 180:
        angle -=360
    return angle

def transform(firstPoint, lastPoint):
    markerDir = markerDirection(firstPoint, lastPoint)
    midMakerDir = directionFromMidMarkerToOrigin(firstPoint, lastPoint)
    distance = distanceFromMidMarkerToOrigin(firstPoint, lastPoint)
    return distance, markerDir - midMakerDir, markerDir #distance, angle and robot orientation

def radTodydx(rad):
    return np.tan(rad)

def getBrushes(array, numColor):
    brushes = []
    for i in range(len(array)):
        brushes.append(pg.intColor(array[i], numColor))
    return brushes

def is_number(s):
    try:
        n = float(s)
        return n
    except ValueError:
        return False

class Robot(pg.GraphicsObject):
    def __init__(self, parent = None):
        pg.GraphicsObject.__init__(self, parent)
        self.length = 1000
        self.width = 500
        self.penWidth = 50;
        self.line = QtCore.QLineF(0, 0, self.length/2, 0)
        self.target = None
        self.origin = QtCore.QPointF(0,0)
        self.pen = pg.mkPen(0)

    def boundingRect(self):
        return QtCore.QRectF(-self.length/2 - self.penWidth / 2, -self.width/2 - self.penWidth / 2,
                      self.length + self.penWidth, self.width + self.penWidth);

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawRect(self.boundingRect());
        painter.drawLine(self.line)
        arcBound = QtCore.QRectF(-3000, -3000, 6000, 6000)
        painter.drawArc(arcBound, 45 * 16,270 * 16)

    def blind(self, isBlind):
        if isBlind:
            self.pen = pg.mkPen(0)
        else:
            self.pen = pg.mkPen(50)

class Arena(pg.GraphicsObject):
    def __init__(self, parent = None):
        pg.GraphicsObject.__init__(self, parent)
        self.arenaLength = 7380
        self.arenaWidth = 3780
        self.dumpLength = 1830
        self.obsFieldLength = 2940
        self.mineLength = 2940

        self.binLength = 1575
        self.binWidth = 457

        self.penWidth = 50
        self.target = None
        self.origin = QtCore.QPointF(0,0)

    def boundingRect(self):
        return QtCore.QRectF(0, -self.arenaWidth/2 - self.penWidth / 2,
                      self.arenaLength + self.penWidth, self.arenaWidth + self.penWidth);

    def paint(self, painter, option, widget):
        #Draw arena walls
        painter.setPen(pg.mkPen(20))
        painter.drawRect(self.boundingRect());

        # Draw collection bin
        binRect = QtCore.QRectF(-self.binWidth, -self.binLength/2, self.binWidth, self.binLength)
        painter.drawRect(binRect);

        # Draw lines
        dumpObsLine = QtCore.QLineF(self.dumpLength , self.arenaWidth/2, self.dumpLength , -self.arenaWidth/2)
        painter.drawLine(dumpObsLine)

        # Draw lines
        dumpObsLine = QtCore.QLineF(self.dumpLength + self.obsFieldLength, self.arenaWidth/2, self.dumpLength +self.obsFieldLength, -self.arenaWidth/2)
        painter.drawLine(dumpObsLine)

class LidarGUI(QtCore.QObject):
    #
    # ﻿#cross hair
    # vLine = pg.InfiniteLine(angle=90, movable=False)
    # hLine = pg.InfiniteLine(angle=0, movable=False)
    # p1.addItem(vLine, ignoreBounds=True)
    # p1.addItem(hLine, ignoreBounds=True)
    #
    #
    # vb = p1.vb
    #
    # def mouseMoved(evt):
    #     pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    #     if p1.sceneBoundingRect().contains(pos):
    #         mousePoint = vb.mapSceneToView(pos)
    #         index = int(mousePoint.x())
    #         if index > 0 and index < len(data1):
    #             label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
    #         vLine.setPos(mousePoint.x())
    #         hLine.setPos(mousePoint.y())

    # Scatter Plot example for clicked event
    # Text Item for text
    lidarFailed = QtCore.pyqtSignal()
    def __init__(self):
        super(LidarGUI, self).__init__()
        self.plots = []
        self.curves = []
        self.lineEdits = [None]*8
        self.labels = [None]*8
        self.checkBoxes = [None]*5
        self.labelStatus = None
        self.labelSystemStatus = None

    def setupUI(self, view):
        self.labelStatus = QtGui.QLabel("Status Status Status Status", view)
        self.labelSystemStatus = QtGui.QLabel("labelSystemStatus", view)
        self.labelStatus.setStyleSheet("QLabel {color : green; }");
        self.labelSystemStatus.setStyleSheet("QLabel {color : green; }");
        self.labelStatus.move(500, 100)
        self.labelSystemStatus.move(200,100)

        self.buttonConnectDisconnect = QtGui.QPushButton("Connect", view)
        self.buttonPauseResume = QtGui.QPushButton("Pause", view)
        down = 500
        #init line edits
        for i in range(len(self.lineEdits)):
            self.lineEdits[i] = QtGui.QLineEdit("", view)
            self.labels[i] = QtGui.QLabel("Change me!", view)
            self.labels[i].move(70, i*25 + down)
            self.labels[i].setStyleSheet("QLabel {color : green; }");
            self.lineEdits[i].move(220, i*25 + down)
        #init checkboxes
        for i in range(len(self.checkBoxes)):
            self.checkBoxes[i] = QtGui.QCheckBox(view)
            self.checkBoxes[i].setText("Radio 1")
            self.checkBoxes[i].move(475, i*25 + down)
            self.checkBoxes[i].setStyleSheet("QCheckBox {color : green; }");

            # gridLayout.addWidget(radio1, 1, 2, 1, 1)

        self.buttonPauseResume.move(350, down)
        self.buttonConnectDisconnect.move(350, down + 25)
        #init brush combobox
        self.comboBox = pg.ComboBox(view)
        self.comboBox.addItem("brushesMarkerLengthFilter")
        self.comboBox.addItem("brushesAveFilter")
        self.comboBox.move(70, 175 + down)

        for _ in range(3):
            self.addPlot(view)

        self.plots[0].setAspectLocked()
        self.plots[0].addLine(x=0, pen=0.2)
        self.plots[0].addLine(y=0, pen=0.2)
        for r in range(1000, 10001, 1000):
            circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            circle.setPen(pg.mkPen(0.2))
            self.plots[0].addItem(circle)
        self.robot = Robot()
        self.arena = Arena()
        self.plots[1].addItem(self.robot)
        self.plots[1].addItem(self.arena)
        self.plots[1].setAspectLocked()
        self.robot.setPos(200,300)
        self.robot.setRotation(30)

        self.plots[2].setXRange(0, 360, padding=0)
        self.plots[2].setYRange(0, 50, padding=0)


    def addPlot(self, view):
        self.plots.append(view.addPlot())
        self.curves.append(pg.ScatterPlotItem(size=5, pen=pg.mkPen(None)))
        self.plots[-1].addItem(self.curves[-1])

    def setRobotPos(self, distance, angle, robotOrientation):
        self.robot.blind(False)
        self.robot.setPos(distance*np.cos(np.radians(angle)), distance*np.sin(np.radians(angle)))
        self.robot.setRotation(robotOrientation)

class RMCLidar(QtCore.QObject):
    paras = ["ANGLE_GAP",
           "DIFF_GAP",
           "AVE_ANGLE_GAP",
           "AVE_GAP_DX_DY",
           "AVE_DIST_GAP",
           "MARKER_LENGTH_MIN",
           "MARKER_LENGTH_MAX",
           "MARKER_QUALITY_MAX"]
    ANGLE_GAP = 0
    DIFF_GAP = 1
    AVE_ANGLE_GAP = 2
    AVE_GAP_DX_DY = 3
    AVE_DIST_GAP = 4
    MARKER_LENGTH_MIN = 5
    MARKER_LENGTH_MAX = 6
    MARKER_QUALITY_MAX = 7
    flags = [
           "DEBUG_MODE",
            "SHOW_RAW_DATA",
            "SHOW_ROBOT_POS",
           "PRINT_RAW_DATA",
           "IS_ACTIVE"
            ]
    DEBUG_MODE = 0
    SHOW_RAW_DATA = 1
    SHOW_ROBOT_POS = 2
    PRINT_RAW_DATA = 3
    IS_ACTIVE = 4

    lidarFailed = QtCore.pyqtSignal()
    lidarStopped = QtCore.pyqtSignal()
    lidarStarted = QtCore.pyqtSignal()
    def __init__(self, port, ui = None):
        super(RMCLidar, self).__init__()
        self.ui = ui
        self.port = port
        self.p = [None]*10
        self.p[self.ANGLE_GAP] = 3.0
        self.p[self.DIFF_GAP] = 0.5
        self.p[self.AVE_ANGLE_GAP] = np.radians(12)
        self.p[self.AVE_GAP_DX_DY] = radTodydx(self.p[self.AVE_ANGLE_GAP])
        self.p[self.AVE_DIST_GAP] = 50
        self.p[self.MARKER_LENGTH_MIN] = 750
        self.p[self.MARKER_LENGTH_MAX] = 920
        self.p[self.MARKER_QUALITY_MAX] = 1
        self.f = [None] * 10
        self.f[self.DEBUG_MODE] = True
        self.f[self.SHOW_RAW_DATA] = True
        self.f[self.SHOW_ROBOT_POS] = True
        self.f[self.PRINT_RAW_DATA] = False
        self.f[self.IS_ACTIVE] = True

        self.iterator = None
        self.scan = None

        self.robotDistance = 0
        self.robotAngle = 0
        self.robotOrientation = 0
        self.newPos = False

        self.lidarFailed.connect(self.stopLidar)
        self.lidar = None

        self.setupGUI()

        self.lastClicked = []
        self.lastText = []

    def init(self):
        try:
            self.lidar = RPLidar(self.port)
            print(self.lidar.get_info())
            print(self.lidar.get_health())
            self.iterator = self.lidar.iter_scans(max_buf_meas=2000)
            for i in range(3):
                next(self.iterator)
            return True
        except:
            print("Lidat init failed")
            self.lidarFailed.emit()
            return False

    def _update(self):
        if self.scan is not None:
            # make polar data
            scanLength = len(self.scan[0])
            quality = np.array(self.scan[0])
            angle = np.array(self.scan[1])
            distance = np.array(self.scan[2])
            rad = np.deg2rad(angle)
            x = distance * np.cos(rad)
            y = distance * np.sin(rad)
            dy = np.diff(y)
            dy = np.append(dy, y[0] - y[-1])
            dx = np.diff(x)
            dx = np.append(dx, x[0] - x[-1])
            dd = np.sqrt(dy * dy + dx * dx)
            dydx = dy / dx
            dydxAngle = np.arctan2(dy, dx)

            # angle gap
            angleFilter = np.zeros(scanLength)
            region = 0
            for i in range(scanLength - 1):  # make sure data points in continous angles are in one group.
                angleFilter[i] = region
                if angle[i + 1] - angle[i] > self.p[self.ANGLE_GAP]:
                    region += 1

            for i in range(-1, scanLength - 1, 1):  # connect 2 ends of circle
                angleFilter[i] = region
                if angle[i + 1] - angle[i] > self.p[self.ANGLE_GAP]:
                    break

            aveFilter = np.zeros(scanLength)
            region = 1
            sumDx = 0
            sumDy = 0
            sumAngle = 0
            sumDist = 0
            count = 0
            dontIncease = False
            for i in range(scanLength):  # could add distance between points
                if angleFilter[i] != angleFilter[i - 1]:  # new region
                    count = 1
                    sumDydx = dydx[i]
                    sumAngle = dydxAngle[i]
                    sumDist = dd[i]
                    # if not dontIncease:
                    region += 1
                    # dontIncease = False
                    aveFilter[i] = region
                else:  # same region
                    if count == 0:
                        count = 1
                        sumDydx = dydx[i]
                        sumAngle = dydxAngle[i]
                        sumDist = dd[i]
                        region += 1
                        aveFilter[i] = region  # in the same subregion
                    else:
                        aveDydx = sumDydx / count
                        aveAngle = sumAngle / count
                        aveDist = sumDist / count
                        if (abs(aveDist - dd[i]) < self.p[self.AVE_DIST_GAP] and (abs(aveDydx - dydx[i]) < self.p[self.AVE_GAP_DX_DY] or abs(
                                    aveAngle - dydxAngle[i]) < self.p[self.AVE_ANGLE_GAP])):  # yes straight line
                            sumDydx += dydx[i]
                            sumAngle += dydxAngle[i]
                            sumDist += dd[i]
                            count += 1
                            aveFilter[i] = region
                        else:
                            count = 0
                            aveFilter[i] = region  # in the same subregion
                            region += 1
                            dontIncease = True

            sum = 0
            SumQuality = 0
            SumDistance = 0
            count = 0
            markerLength = np.zeros(scanLength)
            markerNum = 1

            for i in range(scanLength - 1):
                if aveFilter[i] == aveFilter[i + 1]:
                    sum += dd[i]
                    SumQuality += quality[i]
                    SumDistance += distance[i]
                    count += 1
                    markerLength[i] = 0
                else:
                    if count < 5:
                        sum = 0
                        SumQuality = 0
                        SumDistance = 0
                        count = 0
                    else:
                        if sum > self.p[self.MARKER_LENGTH_MIN] and sum < self.p[self.MARKER_LENGTH_MAX]:
                            if SumQuality // count > self.p[self.MARKER_QUALITY_MAX] - SumDistance // count // 500:
                                for j in range(count + 1):
                                    markerLength[i - j] = markerNum
                                markerNum += 1
                        sum = 0
                        count = 0
            for i in range(-1, scanLength - 1):
                if aveFilter[i] == aveFilter[i + 1]:
                    sum += dd[i]
                    SumQuality += quality[i]
                    SumDistance += distance[i]
                    count += 1
                    markerLength[i] = 0
                else:
                    if count < 5:

                        break
                    else:
                        if sum > self.p[self.MARKER_LENGTH_MIN] and sum < self.p[self.MARKER_LENGTH_MAX]:
                            if SumQuality // count > self.p[self.MARKER_QUALITY_MAX] - SumDistance // count // 500:
                                for j in range(count + 1):
                                    markerLength[i - j] = markerNum
                                markerNum += 1
                        break

            # display robot pos
            unique, indices, count = np.unique(markerLength, return_index=True, return_counts=True)
            if len(unique) == 2:
                firstPointIndex = indices[1]
                lastPointIndex = firstPointIndex + count[1] - 1
                self.robotDistance, self.robotAngle, self.robotOrientation = transform(
                    (x[firstPointIndex], y[firstPointIndex]),
                    (x[lastPointIndex], y[lastPointIndex]))
                self.newPos = True
            else:

                pass
                # self.robot.blind(True)

            #display data
            if self.f[self.DEBUG_MODE] and self.ui is not None:
                comboBoxValue = self.ui.comboBox.value()
                if self.f[self.SHOW_RAW_DATA]:
                    if comboBoxValue == "brushesMarkerLengthFilter":
                        for i in range(len(markerLength)):
                            if markerLength[i] != 0:
                                markerLength[i] = quality[i]
                        brushes = getBrushes(markerLength, 100)
                    elif comboBoxValue == "brushesAveFilter":
                        brushes = getBrushes(aveFilter, 5)
                    self.ui.curves[0].setData(x=x, y=y, data=quality)  # polar
                    self.ui.curves[2].setData(x=angle, y=quality)
                    self.ui.curves[0].setBrush(brushes)
                    self.ui.curves[2].setBrush(brushes)
                if self.f[self.PRINT_RAW_DATA]:
                    print("ave gap: ", self.p[self.AVE_GAP_DX_DY])
                    print("ave aveAngleGap: ", self.p[self.AVE_ANGLE_GAP])
                    print("Angle", "Quality", "Distance", "Angle Filter", "dydx", "dydxAngle", "aveFilter",
                          "makerDistFilter", sep='\t\t\t\t')
                    for i in range(scanLength):
                        pass
                        print(round(angle[i],2), round(quality[i],2), round(distance[i],2), round(angleFilter[i],2), round(dydx[i],2), round(dydxAngle[i],2), round(aveFilter[i],2), round(markerLength[i],2), sep='\t\t\t\t')
                    print("End")
                if self.f[self.SHOW_ROBOT_POS]:
                    self.ui.setRobotPos(self.robotDistance, self.robotAngle, self.robotOrientation)

    ## Make all plots clickable

    def clicked(self, plot, points):
        for p in self.lastClicked:
            p.resetPen()
        for p in points:
            text = pg.TextItem(anchor=(0, 0))
            self.ui.plots[0].addItem(text)
            text.setText(str(p.data()))
            text.setPos(p.pos().x(), p.pos().y())
        self.lastClicked = points

    def update(self):
        if self.f[self.IS_ACTIVE]:
            self.scan = next(self.iterator)
            self._update()
        else:
            next(self.iterator)

    def getPos(self):
        if self.newPos:
            self.newPos = False
            return self.robotDistance, self.robotAngle, self.robotOrientation
        else:
            return None

    def stopLidar(self):
        if self.lidar is not None:
            self.lidar.stop()
            self.lidar.stop_motor()
            self.lidar.disconnect()
            self.lidar = None

    def angleDiffTo(self, point):
        robotX = self.robotDistance*np.cos(self.robotAngle)
        robotY = self.robotDistance*np.sin(self.robotAngle)
        targetOrientation = np.degrees(np.arctan2(point[1] - robotY,point[0] - robotX))
        return self.robotOrientation - targetOrientation

    def changeParameter0(self, value):
        self.changeParameter(0, value)
    def changeParameter1(self, value):
        self.changeParameter(1, value)
    def changeParameter2(self, value):
        self.changeParameter(2, value)
    def changeParameter3(self, value):
        self.changeParameter(3, value)
    def changeParameter4(self, value):
        self.changeParameter(4, value)
    def changeParameter5(self, value):
        self.changeParameter(5, value)
    def changeParameter6(self, value):
        self.changeParameter(6, value)
    def changeParameter7(self, value):
        self.changeParameter(7, value)
    def changeParameter(self, index, value):
        value = is_number(value)
        if value != False:
            print('Updated',self.paras[index],'to', value)
            self.p[index] = value
            self._update()

    def setShowRobotPos(self, state):
        self.f[self.SHOW_ROBOT_POS] = state
        if state == 2:
            self.ui.checkBoxes[self.DEBUG_MODE].setCheckState(2)

    def setPrintRawData(self, state):
        self.f[self.PRINT_RAW_DATA] = state
        if state == 2:
            self.ui.checkBoxes[self.DEBUG_MODE].setCheckState(2)

    def setIsActive(self, state):
        self.f[self.IS_ACTIVE] = state

    def setDebugMode(self, state):
        print(state)
        self.f[self.DEBUG_MODE] = state
        if state == 0:
            self.ui.checkBoxes[self.SHOW_ROBOT_POS].setCheckState(0)
            self.ui.checkBoxes[self.SHOW_RAW_DATA].setCheckState(0)
            self.ui.checkBoxes[self.PRINT_RAW_DATA].setCheckState(0)

    def setShowRawData(self, state):
        self.f[self.SHOW_RAW_DATA] = state
        if state == 0:
            self.lastText = []
            for p in self.ui.curves[0].points():
                text = pg.TextItem(anchor=(0, 0))
                self.ui.plots[0].addItem(text)
                text.setText(str(p.data()))
                text.setPos(p.pos().x(), p.pos().y())
                self.lastText.append(text)
        elif state == 2:
            self.ui.checkBoxes[self.DEBUG_MODE].setCheckState(2)
            for text in self.lastText:
                # text.remove()
                # self.ui.curves[0].clear()
                self.ui.plots[0].removeItem(text)

    def pauseResume(self):
        currentText = self.ui.buttonPauseResume.text()
        if currentText == 'Pause':
            # self.ui.checkBoxes[0].setChecked(False)
            self.ui.buttonPauseResume.setText('Resume')
        elif currentText == 'Resume':
            # self.ui.checkBoxes[0].setChecked(True)
            self.ui.buttonPauseResume.setText('Pause')

    def connectDisconnect(self):
        currentText = self.ui.buttonConnectDisconnect.text()
        if currentText == 'Connect':
            if self.init():
                self.ui.buttonConnectDisconnect.setText('Disconnect')
                self.lidarStarted.emit()
            #do pause stuff
        elif currentText == 'Disconnect':
            self.stopLidar()
            self.ui.buttonConnectDisconnect.setText('Connect')
            self.lidarStopped.emit()
            #do resume stuff

    def setupGUI(self):
        for i, name in enumerate(self.paras):
            self.ui.labels[i].setText(name)
            self.ui.lineEdits[i].setText(str(round(self.p[i], 3)))
        for i, name in enumerate(self.flags):
            self.ui.checkBoxes[i].setText(name)
        self.ui.lineEdits[0].textChanged.connect(self.changeParameter0)
        self.ui.lineEdits[1].textChanged.connect(self.changeParameter1)
        self.ui.lineEdits[2].textChanged.connect(self.changeParameter2)
        self.ui.lineEdits[3].textChanged.connect(self.changeParameter3)
        self.ui.lineEdits[4].textChanged.connect(self.changeParameter4)
        self.ui.lineEdits[5].textChanged.connect(self.changeParameter5)
        self.ui.lineEdits[7].textChanged.connect(self.changeParameter7)

        for i in range(len(self.flags)):
            self.ui.checkBoxes[i].setChecked(self.f[i])
        self.ui.checkBoxes[self.DEBUG_MODE].stateChanged.connect(self.setDebugMode)
        self.ui.checkBoxes[self.SHOW_RAW_DATA].stateChanged.connect(self.setShowRawData)
        self.ui.checkBoxes[self.SHOW_ROBOT_POS].stateChanged.connect(self.setShowRobotPos)
        self.ui.checkBoxes[self.PRINT_RAW_DATA].stateChanged.connect(self.setPrintRawData)
        self.ui.checkBoxes[self.IS_ACTIVE].stateChanged.connect(self.setIsActive)
        self.ui.buttonConnectDisconnect.clicked.connect(self.connectDisconnect)
        self.ui.buttonPauseResume.clicked.connect(self.pauseResume)
        self.ui.curves[0].sigClicked.connect(self.clicked)

