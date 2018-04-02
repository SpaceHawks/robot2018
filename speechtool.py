from gtts import gTTS
import os
from pydub import AudioSegment

def text2Speech(text, filename, preview = False, lang = "en"):
    tts = gTTS(text=text, lang=lang)
    path = "audio/"+filename+".mp3"
    tts.save(path)
    mp3towav(path)
    if preview:
        os.system("afplay "+ path)

def mp3towav(path):
    sound = AudioSegment.from_mp3(path)
    sound.export(path[:-3]+"wav", format="wav")

text2Speech("Goodbye!", "0_OFF", preview=True, lang="en")
text2Speech("Hey, I'm on.", "1_ON", preview=True, lang="en")
text2Speech("Beep Beep Beep, connected to a Mac", "2_DISCONNECTED", preview=True, lang="en")
text2Speech("Beep beep beep, disconnected to the Mac", "3_DISCONNECTED", preview=True, lang="en")
text2Speech("Beep Beep Beep, connected to the Xbox controller.", "4_XBOX_CONNECTED", preview=True, lang="en")
text2Speech("Beep Beep Beep, disconnected to an Xbox controller.", "5_XBOX_DISCONNECTED", preview=True, lang="en")
text2Speech("Waiting for controller, beep, beep, beep, come on hurry up hurry up, beep beep beep, beep beep beep.", "6_LISTENING", preview=True, lang="en")
text2Speech("Approaching bin!", "7_APPROACH_BIN", preview=True, lang="en")
text2Speech("Stopped approaching bin", "8_STOP_APPROACH_BIN", preview=True, lang="en")
text2Speech("Arrived!", "9_ARRIVED", preview=True, lang="en")
text2Speech("Too far! get closer!", "10_TOO_FAR", preview=True, lang="en")
text2Speech("My Due crashed, resetting it.", "11_ARDUINO_FAILURE", preview=True, lang="en")
text2Speech("Oops, Distance sensor failed.", "12_DISTANCE_SENSOR_FAILURE", preview=True, lang="en")
text2Speech("Hey, my battery is almost empty, charge me up.", "13_LOW_BATTERY", preview=True, lang="en")
