from Tests.voice import Voice
from interface import *

v = Voice("../audio")

def gotManualMessageSplot(message):
    pass

def gotAutomaticMessageSplot(decodedMessage):
    pass

def gotSystemMessageSplot(decodedMessage):
    pass

def gotSensorMessageSplot(decodedMessage):
    pass

def controllerDisconnectedSlot():
    v.play(Voice.DISCONNECTED)

def controllerConnectedSlot():
    v.play(Voice.CONNECTED)

def haveHeardFromControllerSlot():
    pass

if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)
    server = RobotServer()
    server.gotManualMessage.connect(gotManualMessageSplot)
    server.gotAutomaticMessage.connect(gotAutomaticMessageSplot)
    server.gotSystemMessage.connect(gotSystemMessageSplot)
    server.gotSensorMessage.connect(gotSensorMessageSplot)
    server.controllerDisconnected.connect(controllerDisconnectedSlot)
    server.tcpServer.newConnection.connect(controllerConnectedSlot)

    app.exec()
