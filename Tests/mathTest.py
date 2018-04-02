import sys
from PyQt5.QtCore import QCoreApplication, QTimer
from voice import Voice


def hieu():
    voices.play(Voice.DISTANCE_SENSOR_FAILURE)
timer = QTimer()

app = QCoreApplication(sys.argv)
voices = Voice("../audio")
timer.timeout.connect(hieu)
timer.start(3000)
app.exec_()
