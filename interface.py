#hieu
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket, QNetworkInterface, QAbstractSocket
from PyQt5.QtCore import QByteArray, QObject, pyqtSignal, QCoreApplication, QTimer, QThread
import struct
encoder = struct.Struct("B")
MESSAGE_FORMAT = "BBBBB"
MESAGE_STRUCT = struct.Struct(MESSAGE_FORMAT)
MESSAGE_LENGTH = len(MESSAGE_FORMAT)

SYSTEM_BYTE = encoder.pack(0)
MANUAL_BYTE = encoder.pack(1)
AUTOMATIC_BYTE = encoder.pack(2)
SENSOR_BYTE = encoder.pack(3)

SYSTEM = 0
MANUAL = 1
AUTOMATIC = 2
SENSOR = 3

EMERGENCY_STOP = 0
DRIVE_AND_TURN = 10
ALIVE =        5
DISTANCE_TO_BIN = 5
def getIPAddress():
    for ipAddress in QNetworkInterface.allAddresses():
        if ipAddress != QHostAddress.LocalHost and ipAddress.toIPv4Address() != 0:
            break
    else:
        ipAddress = QHostAddress(QHostAddress.LocalHost)
    return ipAddress.toString()

class RobotServer(QObject):
    gotSystemMessage = pyqtSignal(tuple)
    gotManualMessage = pyqtSignal(QByteArray)
    gotAutomaticMessage = pyqtSignal(tuple)
    gotSensorMessage = pyqtSignal(tuple)
    controllerDisconnected = pyqtSignal()

    def __init__(self):
        super(RobotServer, self).__init__()
        self.tcpServer = QTcpServer()
        self.tcpServer.newConnection.connect(self.acceptConnection)
        self.tcpServer.acceptError.connect(self.acceptError)
        self.controller = None

        if not self.tcpServer.listen(address=QHostAddress.Any, port=1234):
            print("Unable to start the server: ", self.tcpServer.errorString())
            return
        ipAddress = getIPAddress()
        print('The server is running on', ipAddress, 'port', self.tcpServer.serverPort())

    def acceptConnection(self):
        self.controller = self.tcpServer.nextPendingConnection()
        self.controller.readyRead.connect(self.readNewMessage)
        self.controller.error.connect(self.controllerConnectionError)
        self.controller.disconnected.connect(self.controllerDisconnected)
        print("New connection from: ", self.controller.peerAddress().toString(), 'port', self.controller.peerPort())

    def acceptError(self, socketError):
        print("Server accept error", self.controller.errorString())

    def controllerConnectionError(self, socketError):
        if socketError == QTcpSocket.RemoteHostClosedError:
            print("Client connection closed: ", self.controller.errorString())
        else:
            print("TCP client error: ", self.controller.errorString())
        self.controller.close()
        self.controller = None

    def readNewMessage(self):
        messages = self.controller.readAll()
        for i in range(0, len(messages), MESSAGE_LENGTH):
            message = messages.mid(i, MESSAGE_LENGTH)
            command = message.left(1)
            if command == MANUAL_BYTE: #need to check sum in Arduino side
                self.gotManualMessage.emit(message)
            else:
                decodedMessage = MESAGE_STRUCT.unpack(message)
                if sum(decodedMessage)%256 == 0: #checksum valid
                    if command == SYSTEM_BYTE:
                        self.gotSystemMessage.emit(decodedMessage)
                    if command == AUTOMATIC_BYTE:
                        self.gotAutomaticMessage.emit(decodedMessage)
                    if command == SENSOR_BYTE:
                        self.gotSensorMessage.emit(decodedMessage)
                else:
                    print("TCP server checksum failed:", decodedMessage)

class RobotClient(QObject):
    def __init__(self):
        super(RobotClient, self).__init__()
        self.tcpSocket = QTcpSocket()
        self.tcpSocket.connected.connect(self.connected)
        self.tcpSocket.disconnected.connect(self.disconnected)
        self.tcpSocket.readyRead.connect(self.getNewMessage)
        self.tcpSocket.error.connect(self.displayError)

    def connect(self, ipAddress, port):
        self.tcpSocket.connectToHost(ipAddress, port)
        return self.tcpSocket.waitForConnected(50)

    def disconnect(self):
        self.tcpSocket.abort()
        self.tcpSocket.close()

    def getNewMessage(self):
        print("got new message")
        pass
        #socket->readAll()
        # instr = QDataStream(self.tcpSocket)
        # instr.setVersion(QDataStream.Qt_4_0)
        # if self.blockSize == 0:
        #     if self.tcpSocket.bytesAvailable() < 2:
        #         return
        #
        #     self.blockSize = instr.readUInt16()
        #
        # if self.tcpSocket.bytesAvailable() < self.blockSize:
        #     return
        #
        # nextFortune = instr.readQString()

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QAbstractSocket.HostNotFoundError:
            print("Robot Client:  The host was not found. Please check the host name and port settings.")
        elif socketError == QAbstractSocket.ConnectionRefusedError:
            print("Robot Client: The connection was refused by the peer. Make sure the fortune server is running, and check that the host name and port settings are correct.")
        else:
            print(self, "Robot Client The following error occurred: ", self.tcpSocket.errorString())

    def connected(self):
        print("robot is connected")
        pass
    def disconnected(self):
        print("robot is disconnected")
        pass

    def send(self, data):
        checksum = (256-sum(data))%256
        data.append(checksum)
        self.tcpSocket.write(MESAGE_STRUCT.pack(*data))
        # print("wrote", data)

    def motor(self, device, value1, value2):
        if value1 < 0: value1 += 256
        if value2 < 0: value2 += 256
        self.send([MANUAL, device, value1, value2])

    def drive(self, drive, turn):
        self.motor(DRIVE_AND_TURN, drive, turn)

    def forward(self, speed):
        self.drive(speed, 0)

    def backward(self, speed):
        self.drive(-speed, 0)

    def left(self, speed):
        self.drive(speed, -100)

    def right(self, speed):
        self.drive(speed, 100)

    def stop(self):
        self.drive(0, 0)

    def stopAllMotors(self):
        self.motor(EMERGENCY_STOP, 0, 0)

    def stillAlive(self):
        self.send([SYSTEM, ALIVE, 0, 0])

    def approachBin(self, on):
        if on:
            self.send([AUTOMATIC, DISTANCE_TO_BIN, 1, 0])
        else:
            self.send([AUTOMATIC, DISTANCE_TO_BIN, 0, 0])

    def increaseDistanceToBin(self):
        self.send([AUTOMATIC, DISTANCE_TO_BIN, 3, 0])

    def decreaseDistanceToBin(self):
        self.send([AUTOMATIC, DISTANCE_TO_BIN, 2, 0])
