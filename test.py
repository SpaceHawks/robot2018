from arduino import Task
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
i = 0
def setFunction(value1, value2):
    print("setFunction", value1, value2)

def getFunction():
    global i
    print(i)
    i +=1
    return i
def stopFunction():
    print("stop function called")


app = QtGui.QApplication([""])
timer = QtCore.QTimer()
t = Task(setFunction, (30,3), getFunction, stopFunction, 3000)
t1 = Task(setFunction, (20,3), getFunction, stopFunction, 3000)
t.abandoned.connect(lambda: print("t abandoned"))
t.completed.connect(lambda: print("t compleed"))
t.timeout.connect(lambda: print("t timeout"))
t.notMoving.connect(lambda: print("t not moving"))

t1.abandoned.connect(lambda: print("t1 abandoned"))
t1.completed.connect(lambda: print("t1 compleed"))
t1.timeout.connect(lambda: print("t1 timeout"))
t1.notMoving.connect(lambda: print("t1 not moving"))

timer.singleShot(1000, t.execute)
timer.singleShot(1000, t1.execute)
pg.QtGui.QApplication.exec_()


