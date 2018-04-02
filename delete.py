# import pyqtgraph.examples
# pyqtgraph.examples.run()

# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Update a simp
le plot as rapidly as possible to measure speed.
"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from lidar_tools import *
from rplidar import RPLidar

def stopLidar():
    global timer, lidar
    timer.stop()
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    lidar = None

def initLidar():
    global lidar, timer, ui
    try:
        lidar = RPLidar('/dev/tty.SLAB_USBtoUART')
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
        timer.timeout.connect(ui.update)
        timer.start(1)  # update frequency
        return True
    except:
        print("Lidar failed, Check connection!")
        stopLidar()
        return False

def connectDisconnect():
    global lidar
    if ui.buttonConnectDisconnect.text() == "Connect":
        if lidar == None and initLidar() == True:
            ui.buttonConnectDisconnect.setText("Disconnect")
    else:
        stopLidar()
        ui.buttonConnectDisconnect.setText("Connect")

timer = QtCore.QTimer()
lidar = None

app = QtGui.QApplication([""])
mw = QtGui.QMainWindow()
mw.showMaximized()
# mw.resize(1600,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
ui = LidarGUI()
ui.setupUI(view)
# ui.setRobotPos(3000,-30,-10)
mw.show()
ui.buttonConnectDisconnect.clicked.connect(connectDisconnect)
pg.QtGui.QApplication.exec_()