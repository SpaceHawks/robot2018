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
from queue import Queue
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from RMCParameter import *
# from hokuyolx import HokuyoLX



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

def distanceBetween(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return np.sqrt(dx*dx+dy*dy)

def xy(distance, angle):# degrees
    return (distance*np.cos(np.radians(angle)), distance*np.sin(np.radians(angle)))

def orientation(tail, head):
    return np.degrees(np.arctan2(head[1] - tail[1], head[0] - tail[0]))

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
        self.penWidth = 4
        self.line = QtCore.QLineF(0, 0, self.length, 0)
        self.target = None
        self.origin = QtCore.QPointF(0,0)
        self.pen = pg.mkPen(0)
        self.brush = pg.mkBrush(0)
        self.pen.setWidth(self.penWidth)
        self.centerRadius = 100
        self.centerCircleBound = QtCore.QRectF(-self.centerRadius, -self.centerRadius, self.centerRadius*2, self.centerRadius*2)


    def boundingRect(self):
        return QtCore.QRectF(-self.length/2 - self.penWidth / 2, -self.width/2 - self.penWidth / 2,
                      self.length + self.penWidth, self.width + self.penWidth);

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        # painter.setBrush(self.brush)
        painter.drawRect(self.boundingRect());
        painter.drawLine(self.line)
        painter.drawEllipse(self.centerCircleBound)
        # painter.drawArc(arcBound, 45 * 16,270 * 16)

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

class QualityPlotWidget(pg.GraphicsLayoutWidget):
    def __init__(self):
        pg.GraphicsLayoutWidget.__init__(self)
        self.polarPlot = self.addPlot()
        self.polarCurve = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None))
        self.polarPlot.addItem(self.polarCurve)

        self.qualityPlot = self.addPlot()
        self.qualityCurve = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None))
        self.qualityPlot.addItem(self.qualityCurve)

        self.polarPlot.setAspectLocked()
        self.polarPlot.addLine(x=0, pen=0.2)
        self.polarPlot.addLine(y=0, pen=0.2)
        for r in range(1000, 6001, 1000):
            circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            circle.setPen(pg.mkPen(0.2))
            self.polarPlot.addItem(circle)
            mark = pg.TextItem(anchor=(0, 0))
            mark.setText(str(r) + " mm")
            self.polarPlot.addItem(mark)
            mark.setPos(0, r)
        for angle in range(0, 360, 30):
            p1 = QtCore.QPointF(0,0)
            p2 = xy(6000, angle)
            p2 = QtCore.QPointF(p2[0], p2[1])
            line = QtGui.QGraphicsLineItem(QtCore.QLineF(p1, p2))
            line.setPen(pg.mkPen(pg.mkPen(0.2)))
            self.polarPlot.addItem(line)
            mark = pg.TextItem(anchor=(0,0))
            mark.setText(str(angle))
            self.polarPlot.addItem(mark)
            mark.setPos(p2.x(), p2.y())

        self.qualityPlot.setXRange(0, 360, padding=0)
        self.qualityPlot.setYRange(0, 50, padding=0)

        # self.splitter = QtGui.QSplitter()
        # self.splitter.setOrientation(QtCore.Qt.Vertical)
        # self.layout.addWidget(self.splitter)

    def setBrush(self, brush):
        self.polarCurve.setBrush(brush)
        self.qualityCurve.setBrush(brush)

class ArenaWidget(pg.GraphicsLayoutWidget):
    pathCleared = QtCore.pyqtSignal()
    pathAdded = QtCore.pyqtSignal()
    keyPressed = QtCore.pyqtSignal(QtGui.QKeyEvent)
    keyReleased = QtCore.pyqtSignal(QtGui.QKeyEvent)

    def __init__(self):
        pg.GraphicsLayoutWidget.__init__(self)
        self.path = Queue()
        self.pathPointItems = Queue()
        self.pathLinkItems = Queue()
        self.plot = self.addPlot()
        self.robot = Robot()
        self.arena = Arena()
        self.plot.addItem(self.robot)
        self.plot.addItem(self.arena)
        self.plot.setAspectLocked()
        self.robot.setPos(200,300)
        self.robot.setRotation(30)
        self.scene().sigMouseClicked.connect(self.onClick)
        self.pointRadius = 50

        self.labelRemainingDistance = pg.TextItem(anchor=(0, 0))
        self.labelRemainingDistance.setText("Remaining Distance: ")
        self.labelRemainingDistance.setPos(3500, 200)

        self.labelAngleError = pg.TextItem(anchor=(0, 0))
        self.labelAngleError.setText("Angle Error: ")
        self.labelAngleError.setPos(3500, 0)

        self.labelStatus = pg.TextItem(anchor=(0, 0))
        self.labelStatus.setText("Status: ")
        self.labelStatus.setPos(3500, -200)

        self.plot.addItem(self.labelRemainingDistance)
        self.plot.addItem(self.labelAngleError)
        self.plot.addItem(self.labelStatus)

        self.rocks = []
        self.r = 10

    def arrive(self):
        self.path.get()
        self.path.task_done()
        if self.pathLinkItems.qsize() > 0:
            item = self.pathLinkItems.get()
            self.pathLinkItems.task_done()
            self.plot.removeItem(item)
        item = self.pathPointItems.get()
        self.pathPointItems.task_done()
        self.plot.removeItem(item)

    def onClick(self, event):
        items = self.scene().items(event.scenePos())
        for item in items:
            if isinstance(item, pg.PlotItem) and item == self.plot:
                if event.modifiers() == pg.QtCore.Qt.ShiftModifier:
                    coordinate = self.plot.vb.mapSceneToView(event.scenePos())
                    self.path.put(coordinate)
                    circle = pg.QtGui.QGraphicsEllipseItem(-self.pointRadius, -self.pointRadius, self.pointRadius * 2, self.pointRadius * 2)
                    circle.setPen(pg.mkPen('y'))
                    circle.setBrush(pg.mkBrush('y'))
                    if self.pathPointItems.qsize() > 0:
                        link = QtGui.QGraphicsLineItem(QtCore.QLineF(coordinate, self.pathPointItems.queue[-1].pos()))
                        link.setPen(pg.mkPen('y'))
                        self.plot.addItem(link)
                        self.pathLinkItems.put(link)
                    self.plot.addItem(circle)
                    circle.setPos(coordinate.x(), coordinate.y())
                    self.pathPointItems.put(circle)
                    self.pathAdded.emit()
                if event.modifiers() == pg.QtCore.Qt.ControlModifier:
                    self.clearPath()

    def drawRock(self, xy):
        circle = pg.QtGui.QGraphicsEllipseItem(-self.r, -self.r, self.r * 2, self.r * 2)
        circle.setPen(pg.mkPen('y'))
        circle.setBrush(pg.mkBrush('y'))
        self.plot.addItem(circle)
        circle.setPos(xy[0], xy[1])
        self.rocks.append(circle)

    def clearRock(self):
        for item in self.rocks:
            self.plot.removeItem(item)
        self.rocks = []

    def clearPath(self):
        while not self.path.empty():
            self.arrive()
        self.pathCleared.emit()

    def keyPressEvent(self, event):
        super(ArenaWidget, self).keyPressEvent(event)
        self.keyPressed.emit(event)

    def keyReleaseEvent(self, event):
        super(ArenaWidget, self).keyReleaseEvent(event)
        self.keyReleased.emit(event)
#
# class AugerControlWidget(pg.Qt.QtWidgets.QWidget):
#     pathCleared = QtCore.pyqtSignal()
#     pathAdded = QtCore.pyqtSignal()
#     keyPressed = QtCore.pyqtSignal(QtGui.QKeyEvent)
#     keyReleased = QtCore.pyqtSignal(QtGui.QKeyEvent)
#
#     def __init__(self):
#         pg.Qt.QtWidgets.QWidget.__init__(self)
#         self.statusBar1 = QtGui.QLabel("Status "*20)
#         self.statusBar1.setStyleSheet("QLabel {color : green; }")
#         # self.splitterDrillControl.addWidget(self.statusBar1)
#         # self.add(self.statusBar1)
#         # self.path = Queue()
#         # self.pathPointItems = Queue()
#         # self.pathLinkItems = Queue()
#         # self.plot = self.addPlot()
#         # self.robot = Robot()
#         # self.arena = Arena()
#         # self.plot.addItem(self.robot)
#         # self.plot.addItem(self.arena)
#         # self.plot.setAspectLocked()
#         # self.robot.setPos(200,300)
#         # self.robot.setRotation(30)
#         # self.scene().sigMouseClicked.connect(self.onClick)
#         # self.pointRadius = 50
#         #
#         # self.labelRemainingDistance = pg.TextItem(anchor=(0, 0))
#         # self.labelRemainingDistance.setText("Remaining Distance: ")
#         # self.labelRemainingDistance.setPos(3500, 200)
#         #
#         # self.labelAngleError = pg.TextItem(anchor=(0, 0))
#         # self.labelAngleError.setText("Angle Error: ")
#         # self.labelAngleError.setPos(3500, 0)
#         #
#         # self.labelStatus = pg.TextItem(anchor=(0, 0))
#         # self.labelStatus.setText("Status: ")
#         # self.labelStatus.setPos(3500, -200)
#         #
#         # self.plot.addItem(self.labelRemainingDistance)
#         # self.plot.addItem(self.labelAngleError)
#         # self.plot.addItem(self.labelStatus)
#
#     def arrive(self):
#         self.path.get()
#         self.path.task_done()
#         if self.pathLinkItems.qsize() > 0:
#             item = self.pathLinkItems.get()
#             self.pathLinkItems.task_done()
#             self.plot.removeItem(item)
#         item = self.pathPointItems.get()
#         self.pathPointItems.task_done()
#         self.plot.removeItem(item)
#
#     def onClick(self, event):
#         items = self.scene().items(event.scenePos())
#         for item in items:
#             if isinstance(item, pg.PlotItem) and item == self.plot:
#                 if event.modifiers() == pg.QtCore.Qt.ShiftModifier:
#                     coordinate = self.plot.vb.mapSceneToView(event.scenePos())
#                     self.path.put(coordinate)
#                     circle = pg.QtGui.QGraphicsEllipseItem(-self.pointRadius, -self.pointRadius, self.pointRadius * 2, self.pointRadius * 2)
#                     circle.setPen(pg.mkPen('y'))
#                     circle.setBrush(pg.mkBrush('y'))
#                     if self.pathPointItems.qsize() > 0:
#                         link = QtGui.QGraphicsLineItem(QtCore.QLineF(coordinate, self.pathPointItems.queue[-1].pos()))
#                         link.setPen(pg.mkPen('y'))
#                         self.plot.addItem(link)
#                         self.pathLinkItems.put(link)
#                     self.plot.addItem(circle)
#                     circle.setPos(coordinate.x(), coordinate.y())
#                     self.pathPointItems.put(circle)
#                     self.pathAdded.emit()
#                 if event.modifiers() == pg.QtCore.Qt.ControlModifier:
#                     self.clearPath()
#
#     def clearPath(self):
#         while not self.path.empty():
#             self.arrive()
#         self.pathCleared.emit()
#
#     def keyPressEvent(self, event):
#         super(ArenaWidget, self).keyPressEvent(event)
#         self.keyPressed.emit(event)
#
#     def keyReleaseEvent(self, event):
#         super(ArenaWidget, self).keyReleaseEvent(event)
#         self.keyReleased.emit(event)

class LidarGUI(QtGui.QWidget):
    lidarFailed = QtCore.pyqtSignal()
    eStopPressed = QtCore.pyqtSignal()
    keyReleased = QtCore.pyqtSignal(QtGui.QKeyEvent)
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.plots = []
        self.curves = []
        self.lineEdits = [None]*9
        self.labels = [None]*9
        self.checkBoxes = [None]*5
        self.labelStatus = None
        self.labelSystemStatus = None
        self.labelRemainingDistance = None
        self.labelAngleError = None
        self.setupUI()
        self.params = Parameter.create(name='params', type='group', children=[
            dict(name ='Commands', type='group', children=[
                dict(name='Emergency Stop', type='action'),
                dict(name='XBox Controller On', type='action'),
                dict(name='XBox Controller Off', type='action'),
                dict(name='Pause', type='action'),
            ]),
            dict(name='Arduino Settings', type='group', children=[
                dict(name='Reset', type='action'),
                dict(name='Speed Limit', type='int', value=25, dec=False, step=5, limits=[5, 100]),
                dict(name='Wheel Speed', type='wheels'),
                dict(name='Tilter Position', type='tilter'),
                dict(name='Slider Position', type='slider'),
                dict(name='Auger', type='auger'),
            ]),
            dict(name='Mining Controls', type='group', children=[
                dict(name='Forward', type='action'),
                dict(name='Stop', type='action'),
                dict(name='Reverse', type='action'),
                dict(name='Slider Position', type='int', value=25, dec=False, step=5, limits=[0, 100]),
                dict(name='Slider Speed', type='int', value=25, dec=False, step=5, limits=[0, 100]),
                dict(name='Tilter Position', type='int', value=25, dec=False, step=5, limits=[0, 100]),
                dict(name='Tilter Speed', type='int', value=25, dec=False, step=5, limits=[0, 100]),
            ]),
            dict(name='LIDAR Params', type='group', children=[
                dict(name='Start', type='action'),
                dict(name='Stop', type='action'),
                dict(name='Save', type='action'),
                dict(name='Load', type='action'),
                dict(name='ANGLE_GAP', type='float', value=3.0, dec=False, step=0.5, limits=[0.0001, None]),
                dict(name='AVE_ANGLE_GAP', type='float', value=np.radians(12), dec=False, step=0.5,
                     limits=[0.0001, None]),
                dict(name='AVE_GAP_DX_DY', type='float', value=radTodydx(np.radians(12)), dec=False, step=0.5,
                     limits=[0.0001, None]),
                dict(name='AVE_DIST_GAP', type='float', value=50, dec=False, step=5, limits=[0.0001, None]),
                dict(name='MARKER_LENGTH_MIN', type='float', value=750, dec=False, step=100, limits=[0.0001, None]),
                dict(name='MARKER_LENGTH_MAX', type='float', value=920, dec=False, step=10, limits=[0.0001, None]),
                dict(name='MARKER_QUALITY_MAX', type='float', value=10, dec=False, step=5, limits=[0.0001, None]),
                dict(name='ISO_QUALITY_LENGTH', type='float', value=500, dec=False, step=100, limits=[0.0001, None]),
                dict(name='DIFF_GAP', type='float', value=0.5, dec=False, step=0.1, limits=[0.0001, None]),
            ]),
            dict(name='GUI Controls', type='group', children=[
                dict(name='PRINT_RAW_DATA', type='action'),
                dict(name='SHOW_QUALITY', type='action'),
                dict(name='HIDE_QUALITY', type='action'),
                dict(name='BRUSH', type='list', values=["brushesMarkerLengthFilter", "brushesAveFilter", "quality"]),
                dict(name='DEBUG_MODE', type='bool', value=True),
                dict(name='SHOW_RAW_DATA', type='bool', value=False),
                dict(name='SHOW_ROBOT_POS', type='bool', value=True),
                dict(name='IS_ACTIVE', type='bool', value=True),
            ]),
            dict(name='Distance PID', type='group', children=[
                dict(name='Zero Distance', type='int', value=100, dec=False, step=100, limits=[1, 5000]),
                dict(name='Max Drive', type='int', value=10, dec=False, step=5, limits=[1, 100]),
                dict(name='Max Turn', type='int', value=10, dec=False, step=5, limits=[1, 100]),
                dict(name='Stop', type='action'),
                dict(name='Kp', type='float', value=0.01, dec=False, step=0.01, limits=[0, None]),
                dict(name='Ki', type='float', value=0, dec=False, step=0.01, limits=[0, None]),
                dict(name='Kd', type='float', value=0, dec=False, step=0.01, limits=[0, None]),
                dict(name='Sample Time', type='float', value=100, dec=False, step=100, limits=[1, None]),
            ]),
            dict(name='Orientation PID', type='group', children=[
                dict(name='Zero Angle', type='int', value=2, dec=False, step=1, limits=[-180, 180]),
                dict(name='Max Angle', type='int', value=10, dec=False, step=1, limits=[-180, 180]),
                dict(name='Stop', type='action'),
                dict(name='Kp', type='float', value=0.2, dec=False, step=0.01, limits=[0, None]),
                dict(name='Ki', type='float', value=0.15, dec=False, step=0.01, limits=[0, None]),
                dict(name='Kd', type='float', value=0.03, dec=False, step=0.01, limits=[0, None]),
                dict(name='Sample Time', type='float', value=100, dec=False, step=100, limits=[1, None]),
            ]),
            dict(name='Self-Alignment PID', type='group', children=[
                dict(name='Start', type='action'),
                dict(name='Stop', type='action'),
                dict(name='Set Distance', type='int', value=300, dec=False, step=50, limits=[50, 1000]),
                dict(name='Kp', type='float', value=0.2, dec=False, step=0.01, limits=[0, None]),
                dict(name='Ki', type='float', value=0, dec=False, step=10, limits=[0, None]),
                dict(name='Kd', type='float', value=0, dec=False, step=5, limits=[0, None]),
                dict(name='Sample Time', type='float', value=200, dec=False, step=100, limits=[1, None]),
            ]),
            dict(name='Timers', type='group', children=[
                dict(name='stillAliveTimer', type='int', value=500, dec=False, step=10, limits=[1, 5000]),
                dict(name='xboxTimer', type='int', value=1, dec=False, step=10, limits=[1, 5000]),
                dict(name='distanceSensorsTimer', type='int', value=20, dec=False, step=10, limits=[1, 5000]),
                dict(name='lidarTimer', type='int', value=10, dec=False, step=10, limits=[1, 5000]),
                dict(name='goToTimer', type='int', value=50, dec=False, step=10, limits=[1, 5000]),
                dict(name='correctOrientationTimer', type='int', value=200, dec=False, step=10, limits=[1, 5000]),
        ]),
            #
            # params = [
            #     {'name': 'Basic parameter data types', 'type': 'group', 'children': [
            #         {'name': 'Integer', 'type': 'int', 'value': 10},
            #         {'name': 'Float', 'type': 'float', 'value': 10.5, 'step': 0.1},
            #         {'name': 'String', 'type': 'str', 'value': "hi"},
            #         {'name': 'List', 'type': 'list', 'values': [1, 2, 3], 'value': 2},
            #         {'name': 'Named List', 'type': 'list', 'values': {"one": 1, "two": "twosies", "three": [3, 3, 3]},
            #          'value': 2},
            #         {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
            #         {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
            #         {'name': 'Gradient', 'type': 'colormap'},
            #         {'name': 'Subgroup', 'type': 'group', 'children': [
            #             {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
            #             {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
            #         ]},
            #         {'name': 'Text Parameter', 'type': 'text', 'value': 'Some text...'},
            #         {'name': 'Action Parameter', 'type': 'action'},
            #     ]}]
            ])
        self.tree.setParameters(self.params, showTop=False)
        

    def loadLidarParams(self, fileName):
        with open("fileName", 'r') as input:
            for paramString in input.readlines():
                temp = paramString.split('=')
                print(temp)
                self.params.param("LIDAR Params", temp[0]).setValue(float(temp[1]))

    def saveLidarPamras(self, fileName):
        with open("fileName", 'w') as out:
            for child in self.params.param("LIDAR Params"):
                if child.type() != "action":
                    out.write(child.name() + "=" + str(child.value())+ '\n')

    def setupUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.layout.addWidget(self.splitter)
        self.splitterDrillControl = QtGui.QSplitter()
        self.splitterDrillControl.setOrientation(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.splitterDrillControl)

        self.tree = ParameterTree(showHeader=False)
        self.splitterDrillControl.addWidget(self.tree)

        #change here
        # self.augerControlWidget = AugerControlWidget()
        # self.splitterDrillControl.addWidget(self.augerControlWidget)


        self.splitter2 = QtGui.QSplitter()
        self.splitter2.setOrientation(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.splitter2)

        self.statusBar = QtGui.QLabel("Status "*20)
        self.statusBar.setStyleSheet("QLabel {color : green; }")
        self.splitter3 = QtGui.QSplitter()
        self.splitter3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter2.addWidget(self.statusBar)

        self.qualityPlotWidget = QualityPlotWidget()
        self.arenaWidget = ArenaWidget()
        self.splitter2.addWidget(self.arenaWidget)
        self.splitter2.addWidget(self.qualityPlotWidget)

    def setRobotPos(self, distance, angle, robotOrientation):
        robotPos = xy(distance, angle)
        self.arenaWidget.robot.blind(False)
        self.arenaWidget.robot.setPos(robotPos[0], robotPos[1])
        self.arenaWidget.robot.setRotation(robotOrientation)

        self.arenaWidget.labelRemainingDistance.setPos(robotPos[0] - 500, robotPos[1] - 400)
        self.arenaWidget.labelAngleError.setPos(robotPos[0] - 500, robotPos[1] - 600)
        self.arenaWidget.labelStatus.setPos(robotPos[0] - 500, robotPos[1] - 800)

    def keyPressEvent(self, event):
        super(LidarGUI, self).keyPressEvent(event)
        key = event.key()
        if key == pg.QtCore.Qt.Key_Escape or key == pg.QtCore.Qt.Key_Space:
            self.eStopPressed.emit()

    def lidarStartAnimation(self):
        self.statusBar.setText("LIDAR started")
        self.statusBar.setStyleSheet('color: green')

    def lidarFailAnimation(self):
        self.statusBar.setText("LIDAR failed")
        self.statusBar.setStyleSheet('color: red')

    def lidarStopAnimation(self):
        self.statusBar.setText("LIDAR stopped")
        self.statusBar.setStyleSheet('color: yellow')

class Localizer(QtCore.QObject):

    lidarFailed = QtCore.pyqtSignal()
    lidarStopped = QtCore.pyqtSignal()
    lidarStarted = QtCore.pyqtSignal()
    def __init__(self, ui = None):
        super(Localizer, self).__init__()
        self.ui = ui
        self.iterator = None
        self.scan = None

        self.robotDistance = 0
        self.robotAngle = 0
        self.robotOrientation = 0
        self.newPos = False

        self.lidarFailed.connect(self.stop)
        self.lidar = None

        if self.ui is not None:
            self.setupGUI()

        self.lastClicked = []
        self.lastText = []

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
            dq = np.diff(quality)
            dq = np.append(dq, quality[0] - quality[-1])
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
                if angle[i + 1] - angle[i] > self.ANGLE_GAP.value():
                    region += 1

            for i in range(-1, scanLength - 1, 1):  # connect 2 ends of circle
                angleFilter[i] = region
                if angle[i + 1] - angle[i] > self.ANGLE_GAP.value():
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
                        if (abs(aveDist - dd[i]) < self.AVE_DIST_GAP.value() and (abs(aveDydx - dydx[i]) < self.AVE_GAP_DX_DY.value() or abs(
                                    aveAngle - dydxAngle[i]) < self.AVE_ANGLE_GAP.value())):  # yes straight line
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
            # SumQuality = 0
            # SumDistance = 0
            count = 0
            markerLength = np.zeros(scanLength)
            markerNum = 1

            for i in range(scanLength - 1):
                if aveFilter[i] == aveFilter[i + 1]:
                    sum += dd[i]
                    # SumQuality += quality[i]
                    # SumDistance += distance[i]
                    count += 1
                    markerLength[i] = 0
                else:
                    if count < 5:
                        sum = 0
                        # SumQuality = 0
                        # SumDistance = 0
                        count = 0
                    else:
                        if sum > self.MARKER_LENGTH_MIN.value() and sum < self.MARKER_LENGTH_MAX.value():
                            # if SumQuality // count > self.MARKER_QUALITY_MAX.value() - SumDistance // count // 500:
                            for j in range(count + 1):
                                markerLength[i - j] = markerNum
                            markerNum += 1
                        sum = 0
                        count = 0
            for i in range(-1, scanLength - 1):
                if aveFilter[i] == aveFilter[i + 1]:
                    sum += dd[i]
                    # SumQuality += quality[i]
                    # SumDistance += distance[i]
                    count += 1
                    markerLength[i] = 0
                else:
                    if count < 5:

                        break
                    else:
                        if sum > self.MARKER_LENGTH_MIN.value() and sum < self.MARKER_LENGTH_MAX.value():
                            # if SumQuality // count > self.MARKER_QUALITY_MAX.value() - SumDistance // count // 500:
                            for j in range(count + 1):
                                markerLength[i - j] = markerNum
                            markerNum += 1
                        break

            # qualityFilter = np.zeros(scanLength)

            # display robot pos
            unique, indices, count = np.unique(markerLength, return_index=True, return_counts=True)
            for i in range(1, len(unique), 1):
                regions = self.qualityCheck(dq[indices[i]:indices[i]+count[i]])
                rUnique, rIndices, rCount = np.unique(regions, return_index=True, return_counts=True)
                if len(rUnique) == 2:
                    bIndex = rIndices[1]
                    p1 = (x[indices[i]], y[indices[i]])
                    p2 = (x[indices[i]+bIndex-1], y[indices[i]+bIndex-1])
                    p3 = (x[indices[i]+bIndex], y[indices[i]+bIndex])
                    p4 = (x[indices[i]+len(regions)-1], y[indices[i]+len(regions)-1])
                    if abs((distanceBetween(p1,p2) - distanceBetween(p3,p4))) < self.ISO_QUALITY_LENGTH.value():
                        firstPointIndex = indices[i]
                        lastPointIndex = indices[i]+len(regions)-1
                        self.robotDistance, self.robotAngle, self.robotOrientation = transform(
                            (x[firstPointIndex], y[firstPointIndex]),
                            (x[lastPointIndex], y[lastPointIndex]))
                        self.newPos = True
                        #UNIQUE MARKER
                        for ii in range(len(regions)):
                            markerLength[indices[i]+ii] = regions[ii]
                    else:
                        for ii in range(len(regions)):
                            markerLength[indices[i] + ii] = 0
                else:
                    for ii in range(len(regions)):
                        markerLength[indices[i]+ii] = 0

            #display data
            if self.DEBUG_MODE.value() and self.ui is not None:
                if self.SHOW_RAW_DATA.value():
                    brushType = self.BRUSH.value()
                    if brushType == "brushesMarkerLengthFilter":
                        # for i in range(len(markerLength)):
                        #     if markerLength[i] != 0:
                        #         markerLength[i] = quality[i]
                        brushes = getBrushes(markerLength, 5)
                    elif brushType == "brushesAveFilter":
                        brushes = getBrushes(aveFilter, 5)
                    elif brushType == "quality":
                        brushes = getBrushes(quality, 2000)
                    self.ui.qualityPlotWidget.polarCurve.setData(x=x, y=y, data=quality)  # polar
                    self.ui.qualityPlotWidget.qualityCurve.setData(x=angle, y=quality)
                    self.ui.qualityPlotWidget.polarCurve.setBrush(brushes)
                    self.ui.qualityPlotWidget.qualityCurve.setBrush(brushes)
                if self.PRINT_RAW_DATA.value():
                    print("ave gap: ", self.AVE_GAP_DX_DY.value())
                    print("ave aveAngleGap: ", self.AVE_ANGLE_GAP.value())
                    print("Angle", "Quality", "Distance", "Angle Filter", "dydx", "dydxAngle", "aveFilter",
                          "makerDistFilter", sep='\t\t\t\t')
                    for i in range(scanLength):
                        print(round(angle[i],2), round(quality[i],2), round(distance[i],2), round(angleFilter[i],2), round(dydx[i],2), round(dydxAngle[i],2), round(aveFilter[i],2), round(markerLength[i],2), sep='\t\t\t\t')
                    print("End")
                if self.SHOW_ROBOT_POS.value():
                    self.ui.setRobotPos(self.robotDistance, self.robotAngle, self.robotOrientation)

    def _updateHokuyo(self):
        if self.scan is not None:
            # make polar data
            scanLength = self.scan[0].size
            angle = self.scan[0] #in rad
            distance = self.scan[1]
            quality = self.scan[2]

            x = distance * np.cos(angle)
            y = distance * np.sin(angle)
            dq = np.diff(quality)
            dq = np.append(dq, quality[0] - quality[-1])
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
                if angle[i + 1] - angle[i] > self.ANGLE_GAP.value():
                    region += 1

            for i in range(-1, scanLength - 1, 1):  # connect 2 ends of circle
                angleFilter[i] = region
                if angle[i + 1] - angle[i] > self.ANGLE_GAP.value():
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
                        if (abs(aveDist - dd[i]) < self.AVE_DIST_GAP.value() and (
                                abs(aveDydx - dydx[i]) < self.AVE_GAP_DX_DY.value() or abs(
                                    aveAngle - dydxAngle[
                                    i]) < self.AVE_ANGLE_GAP.value())):  # yes straight line
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
            # SumQuality = 0
            # SumDistance = 0
            count = 0
            markerLength = np.zeros(scanLength)
            markerNum = 1

            for i in range(scanLength - 1):
                if aveFilter[i] == aveFilter[i + 1]:
                    sum += dd[i]
                    # SumQuality += quality[i]
                    # SumDistance += distance[i]
                    count += 1
                    markerLength[i] = 0
                else:
                    if count < 5:
                        sum = 0
                        # SumQuality = 0
                        # SumDistance = 0
                        count = 0
                    else:
                        if sum > self.MARKER_LENGTH_MIN.value() and sum < self.MARKER_LENGTH_MAX.value():
                            # if SumQuality // count > self.MARKER_QUALITY_MAX.value() - SumDistance // count // 500:
                            for j in range(count + 1):
                                markerLength[i - j] = markerNum
                            markerNum += 1
                        sum = 0
                        count = 0
            for i in range(-1, scanLength - 1):
                if aveFilter[i] == aveFilter[i + 1]:
                    sum += dd[i]
                    # SumQuality += quality[i]
                    # SumDistance += distance[i]
                    count += 1
                    markerLength[i] = 0
                else:
                    if count < 5:

                        break
                    else:
                        if sum > self.MARKER_LENGTH_MIN.value() and sum < self.MARKER_LENGTH_MAX.value():
                            # if SumQuality // count > self.MARKER_QUALITY_MAX.value() - SumDistance // count // 500:
                            for j in range(count + 1):
                                markerLength[i - j] = markerNum
                            markerNum += 1
                        break

            # qualityFilter = np.zeros(scanLength)

            # display robot pos
            unique, indices, count = np.unique(markerLength, return_index=True, return_counts=True)
            for i in range(1, len(unique), 1):
                regions = self.qualityCheck(dq[indices[i]:indices[i] + count[i]])
                rUnique, rIndices, rCount = np.unique(regions, return_index=True, return_counts=True)
                if len(rUnique) == 2:
                    bIndex = rIndices[1]
                    p1 = (x[indices[i]], y[indices[i]])
                    p2 = (x[indices[i] + bIndex - 1], y[indices[i] + bIndex - 1])
                    p3 = (x[indices[i] + bIndex], y[indices[i] + bIndex])
                    p4 = (x[indices[i] + len(regions) - 1], y[indices[i] + len(regions) - 1])
                    if abs((distanceBetween(p1, p2) - distanceBetween(p3,
                                                                      p4))) < self.ISO_QUALITY_LENGTH.value():
                        firstPointIndex = indices[i]
                        lastPointIndex = indices[i] + len(regions) - 1
                        self.robotDistance, self.robotAngle, self.robotOrientation = transform(
                            (x[firstPointIndex], y[firstPointIndex]),
                            (x[lastPointIndex], y[lastPointIndex]))
                        self.newPos = True
                        # UNIQUE MARKER
                        for ii in range(len(regions)):
                            markerLength[indices[i] + ii] = regions[ii]
                    else:
                        for ii in range(len(regions)):
                            markerLength[indices[i] + ii] = 0
                else:
                    for ii in range(len(regions)):
                        markerLength[indices[i] + ii] = 0

            # display data
            if self.DEBUG_MODE.value() and self.ui is not None:
                if self.SHOW_RAW_DATA.value():
                    brushType = self.BRUSH.value()
                    if brushType == "brushesMarkerLengthFilter":
                        brushes = getBrushes(markerLength, 5)
                    elif brushType == "brushesAveFilter":
                        brushes = getBrushes(aveFilter, 5)
                    elif brushType == "quality":
                        brushes = getBrushes(quality, 100)
                    self.ui.qualityPlotWidget.polarCurve.setData(x=x, y=y, data=quality)  # polar
                    self.ui.qualityPlotWidget.qualityCurve.setData(x=angle, y=quality)
                    self.ui.qualityPlotWidget.polarCurve.setBrush(brushes)
                    self.ui.qualityPlotWidget.qualityCurve.setBrush(brushes)
                if self.PRINT_RAW_DATA.value():
                    print("ave gap: ", self.AVE_GAP_DX_DY.value())
                    print("ave aveAngleGap: ", self.AVE_ANGLE_GAP.value())
                    print("Angle", "Quality", "Distance", "Angle Filter", "dydx", "dydxAngle", "aveFilter",
                          "makerDistFilter", sep='\t\t\t\t')
                    for i in range(scanLength):
                        print(round(angle[i], 2), round(quality[i], 2), round(distance[i], 2),
                              round(angleFilter[i], 2), round(dydx[i], 2), round(dydxAngle[i], 2),
                              round(aveFilter[i], 2), round(markerLength[i], 2), sep='\t\t\t\t')
                    print("End")
                if self.SHOW_ROBOT_POS.value():
                    self.ui.setRobotPos(self.robotDistance, self.robotAngle, self.robotOrientation)

    ## Make all plots clickable
    def qualityCheck(self, dq):
        regions = [1]*len(dq)
        currentRegion = 1
        for i in range(len(dq)):
            regions[i] = currentRegion
            if abs(dq[i]) > self.MARKER_QUALITY_MAX.value():
                currentRegion += 1
        # sum = 0
        # count = 0

        # for i in range(len(dq) - 1):  # could add distance between points
        #     if count == 0:
        #         count = 1
        #         sum = dq[i]
        #         regions[i] = currentRegion
        #     else:
        #         ave = sum / count
        #         if abs(ave - dq[i]) < self.MARKER_QUALITY_MAX.value():  # yes straight line
        #             sum += dq[i]
        #             count += 1
        #             regions[i] = currentRegion
        #         else:
        #             count = 0
        #             regions[i] = currentRegion
        #             currentRegion +=1
        # regions[-1] = currentRegion
        return regions

    def clicked(self, plot, points):
        for p in self.lastClicked:
            p.resetPen()
        for p in points:
            text = pg.TextItem(anchor=(0, 0))
            self.ui.plots[0].addItem(text)
            text.setText(str(p.data()))
            text.setPos(p.pos().x(), p.pos().y())
        self.lastClicked = points

    def getPos(self):
        if self.newPos:
            self.newPos = False
            return self.robotDistance, self.robotAngle, self.robotOrientation
        else:
            return None

    def angleDiffTo(self, point):
        robotToDestAngle = orientation(xy(self.robotDistance, self.robotAngle), point)
        return self.robotOrientation - robotToDestAngle

    def distanceFromRobotTo(self, point):
        robotPos = xy(self.robotDistance, self.robotAngle)
        return distanceBetween(robotPos, point)

    def getDriveParams(self, point):
        robotPos = xy(self.robotDistance, self.robotAngle)
        distance = distanceBetween(robotPos, point)
        robotToDestAngle = orientation(xy(self.robotDistance, self.robotAngle), point)
        angleDiff = self.robotOrientation - robotToDestAngle
        usingtail = robotPos[0] > point[0]
        if usingtail:
            angleDiff = standardizeAngle(angleDiff+180)
        return distance, angleDiff, usingtail

    def setShowRobotPos(self, param):
        state = param.value()
        if state == True:
            self.DEBUG_MODE.setValue(True)

    def setPrintRawData(self, param):
        state = param.value()
        if state == True:
            self.DEBUG_MODE.setValue(True)

    def setDebugMode(self, param):
        state = param.value()
        if state == False:
            self.SHOW_ROBOT_POS.setValue(False)
            self.SHOW_RAW_DATA.setValue(False)
            self.PRINT_RAW_DATA.setValue(False)

    def setShowRawData(self, param):
        state = param.value()
        if state == True:
            self.DEBUG_MODE.setValue(True)

    def showQuality(self):
        print("shaow")
        if len(self.lastText) > 0:
            self.hideQuality()
        for p in self.ui.qualityPlotWidget.polarCurve.points():
            text = pg.TextItem(anchor=(0, 0))
            self.ui.qualityPlotWidget.polarPlot.addItem(text)
            text.setText(str(p.data()))
            text.setPos(p.pos().x(), p.pos().y())
            self.lastText.append(text)

    def hideQuality(self):
        for text in self.lastText:
            self.ui.qualityPlotWidget.polarPlot.removeItem(text)

    def setupGUI(self):
        self.ANGLE_GAP = self.ui.params.param('LIDAR Params', 'ANGLE_GAP')
        self.DIFF_GAP = self.ui.params.param('LIDAR Params', 'DIFF_GAP')
        self.AVE_ANGLE_GAP = self.ui.params.param('LIDAR Params', 'AVE_ANGLE_GAP')
        self.AVE_GAP_DX_DY = self.ui.params.param('LIDAR Params', 'AVE_GAP_DX_DY')
        self.AVE_DIST_GAP = self.ui.params.param('LIDAR Params', 'AVE_DIST_GAP')
        self.MARKER_LENGTH_MIN = self.ui.params.param('LIDAR Params', 'MARKER_LENGTH_MIN')
        self.MARKER_LENGTH_MAX = self.ui.params.param('LIDAR Params', 'MARKER_LENGTH_MAX')
        self.MARKER_QUALITY_MAX = self.ui.params.param('LIDAR Params', 'MARKER_QUALITY_MAX')
        self.ISO_QUALITY_LENGTH = self.ui.params.param('LIDAR Params', 'ISO_QUALITY_LENGTH')
        self.ui.params.param('LIDAR Params', 'Start').sigActivated.connect(self.start)
        self.ui.params.param('LIDAR Params', 'Stop').sigActivated.connect(self.stop)
        self.DEBUG_MODE = self.ui.params.param('GUI Controls', 'DEBUG_MODE')
        self.SHOW_RAW_DATA = self.ui.params.param('GUI Controls', 'SHOW_RAW_DATA')
        self.SHOW_ROBOT_POS = self.ui.params.param('GUI Controls', 'SHOW_ROBOT_POS')
        self.PRINT_RAW_DATA = self.ui.params.param('GUI Controls', 'PRINT_RAW_DATA')
        self.SHOW_QUALITY = self.ui.params.param('GUI Controls', 'SHOW_QUALITY')
        self.HIDE_QUALITY = self.ui.params.param('GUI Controls', 'HIDE_QUALITY')
        self.IS_ACTIVE = self.ui.params.param('GUI Controls', 'IS_ACTIVE')
        self.BRUSH = self.ui.params.param('GUI Controls', 'BRUSH')


        self.DEBUG_MODE.sigValueChanged.connect(self.setDebugMode)
        self.SHOW_RAW_DATA.sigValueChanged.connect(self.setShowRawData)
        self.SHOW_ROBOT_POS.sigValueChanged.connect(self.setShowRobotPos)
        self.PRINT_RAW_DATA.sigValueChanged.connect(self.setPrintRawData)
        self.SHOW_QUALITY.sigActivated.connect(self.showQuality)
        self.HIDE_QUALITY.sigActivated.connect(self.hideQuality)


        self.lidarStopped.connect(self.ui.lidarStopAnimation)
        self.lidarStarted.connect(self.ui.lidarStartAnimation)
        self.lidarFailed.connect(self.ui.lidarFailAnimation)

class RMCRpLidar(Localizer):
    def __init__(self, serialPort, ui=None):
        super(RMCRpLidar, self).__init__(ui)
        self.serialPort = serialPort

    def start(self):
        try:
            self.lidar = RPLidar(self.serialPort)
            self.iterator = self.lidar.iter_scans(max_buf_meas=2000)
            for i in range(3):
                next(self.iterator)
            self.lidarStarted.emit()
            return True
        except:
            self.lidarFailed.emit()
            return False

    def stop(self):
        if self.lidar is not None:
            self.lidar.stop()
            self.lidar.stop_motor()
            self.lidar.disconnect()
            self.lidar = None
            self.lidarStopped.emit()

    def update(self):
        if self.IS_ACTIVE.value():
            self.scan = next(self.iterator)
            self._update()
        else:
            next(self.iterator)

class RMCHokuyoLidar(Localizer):
    def __init__(self, ui=None):
        super(RMCHokuyoLidar, self).__init__(ui)

    def start(self):
        if self.lidar is not None:
            self.lidar.close()
        self.lidar = HokuyoLX()
        self.lidarStarted.emit()

    def stop(self): #change
        if self.lidar is not None:
            self.lidar.close()
            self.lidarStopped.emit()

    def update(self):
        if self.IS_ACTIVE.value():
            timestamp, self.scan = self.lidar.get_filtered_intens()  # Single measurment mode
            self.scan = self.scan.transpose()
            self._updateHokuyo()