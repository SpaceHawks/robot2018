from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QObject
class Voice(QObject):
    OFF = 0
    ON = 1
    CONNECTED = 2
    DISCONNECTED = 3
    XBOX_CONNECTED = 4
    XBOX_DISCONNECTED = 5
    LISTENING = 6
    APPROACH_BIN = 7
    STOP_APPROACH_BIN = 8
    ARRIVED = 9
    TOO_FAR = 10
    ARDUINO_FAILURE = 11
    DISTANCE_SENSOR_FAILURE = 12
    LOW_BATTERY = 13
    def __init__(self, audioRoot):
        super(Voice, self).__init__()
        self.muted = False
        self.audioRoot = audioRoot
        self.filenames =["0_OFF.wav"
                        ,"1_ON.wav"
                        ,"2_DISCONNECTED.wav"
                        ,"3_DISCONNECTED.wav"
                        ,"4_XBOX_CONNECTED.wav"
                        ,"5_XBOX_DISCONNECTED.wav"
                        ,"6_LISTENING.wav"
                        ,"7_APPROACH_BIN.wav"
                        ,"8_STOP_APPROACH_BIN.wav"
                        ,"9_ARRIVED.wav"
                        ,"10_TOO_FAR.wav"
                        ,"11_ARDUINO_FAILURE.wav"
                        ,"12_DISTANCE_SENSOR_FAILURE.wav"
                        ,"13_LOW_BATTERY.wav"]
        self.audios = [None]*len(self.filenames)

    def play(self, i):
        if not self.muted:
            if i < len(self.audios):
                try:
                    if self.audios[i] == None:
                        self.audios[i] = QSound(self.audioRoot + "/" + self.filenames[i])
                    self.audios[i].play()
                except:
                    print("Audio not found")

    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = True