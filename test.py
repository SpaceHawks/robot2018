from lidar_tools import RMCLidar
import pyqtgraph as pg
import lidar_tools, platform

print("Running lidarTest.py")
app = pg.QtGui.QApplication([""])
ui = lidar_tools.LidarGUI()
mw = pg.QtGui.QMainWindow()
mw.showMaximized()
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
ui = lidar_tools.LidarGUI()
ui.setupUI(view)
# ui.buttonConnectDisconnect.clicked.connect(connectDisconnect)
mw.show()
if platform.system() == "Darwin":
    port = '/dev/tty.SLAB_USBtoUART'
else:
    port = '/dev/ttyUSB0'
lidar = RMCLidar(port, ui)
timer = pg.QtCore.QTimer()
timer.timeout.connect(lidar.update)
lidar.lidarStarted.connect(lambda : timer.start(10))
lidar.lidarStopped.connect(timer.stop)
pg.QtGui.QApplication.exec_()

# self.lidar = RPLidar()
# self.lidar = RPLidar('/dev/ttyUSB0')
# if lidar.init():
#     lidar.update()
