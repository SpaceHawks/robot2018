import socket
import threading
from time import sleep
from struct import Struct
from constants import *
from queue import Queue

#System commands:
#    Command = 0
#    device = 0 -> sender connected
#             1 -> sender disconnected
#             2 -> receiver connected
#             3 -> receiver disconnected
#    Value = the ip address of the target

class TCP(socket.socket, threading.Thread):
    'Communication between two devices using python'
    def __init__(self, host, port, q):
        threading.Thread.__init__(self)
        socket.socket.__init__(self)
        self.dataStruct = Struct(DATA_STRUCTURE)
        self.commandStruct = Struct(COMMAND_STRUCTURE)
        self.host = host
        self.port = port
        self.q = q
        self.running = True
        
    def doSenderTask(self):
        while self.running:
            #print("i got a sender")
            self.checkLocalQ()
            if not self.hasClient: break
            if not self.q.empty():
                data = self.q.get()
                try:
                    if self.hasClient:
                        self.client.send(data)
                    else:
                        pass #ignore and dispose the message
                    self.q.task_done()
                except:
                    self.q.task_done()
                    self.clean()
                    break
            else:
                sleep(0.0001) #to reduce processing burden

    def doReceiverTask(self):
        self.settimeout(0.1)
        while self.running:
            self.checkLocalQ()
            if not self.hasClient: break
            try:
                data = self.client.recv(1024)
                if not data: break
                self.q.put(data)
                #print("put ", data)
            except ConnectionResetError:
                print("Receiver connection reset error")
                break
            except socket.timeout:
                #print("Receiver Time out")
                continue
        self.settimeout(None)
        self.clean()

    def appendChecksum(self, data):
        data.append((256-sum(data))%256) #add all element must get 0

    def pack(self, packingStruct, data):
        lenDiff = DATA_LENGTH - (len(data) + 1)
        if lenDiff < 0:
            raise ValueError('Message is too long!')
        else:
            for i in range(lenDiff): #add addition zeros of not enough info
                data.append(0)
            self.appendChecksum(data)
            return packingStruct.pack(*data)
        
    def unpack(self, packingStruct, dataBin):
        return packingStruct.unpack(dataBin)

    def __str__(self):
        return self.host+":"+str(self.port) +" is running: "+str(self.running)

class TCPServer(TCP):
    'Communication between two devices using python'
    def __init__(self, host, port, q):
        super().__init__(host, port, q)
        self.bind()

    def bind(self):
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # add this to reuse the port
        super().bind((self.host, self.port))

    def listen(self):
        self.settimeout(0.5)
        while self.running:
            self.checkLocalQ()
            try:
                super().listen()
                self.client, self.clientAddress = self.accept()
                self.settimeout(None)
                self.connected()
                break
            except socket.timeout:
                continue

    def pack(self, data):
        return super().pack(self.dataStruct, data)
        
    def unpack(self, dataBin):
        return super().unpack(self.commandStruct, dataBin)

    def clean(self):
        if hasattr(self, 'client'):
            self.client.close()
        self.disconnected()

    def stop(self):
        if hasattr(self, 'client'):
            self.client.close()
        self.close()
        self.disconnected()
        self.running = False

class TCPServerSender(TCPServer):
    'Communication between two devices using python'
    def __init__(self, host, port, q, localInQ, localOutQ):
        super().__init__(host, port, q)
        self.localInQ = localInQ
        self.localOutQ = localOutQ
        self.hasClient = False
        self.receiverHasClient = False

    def run(self):
        while self.running:
            self.listen()
            self.doSenderTask()

    def checkLocalQ(self):
        while not self.localInQ.empty():
            signal = self.localInQ.get()
            if signal[0] == 0: #make sure its a system command
                if signal[1] == 2: #receiver got a connection
                    self.receiverHasClient = True
                elif signal[1] == 3: #receiver lost its connection
                    self.receiverHasClient = False
                    self.clean() #abort my connection


    def connected(self):
        self.hasClient = True #tell itself it has a client
        if hasattr(self, 'clientAddress'):
            self.localOutQ.put([0, 0, int(self.clientAddress[0].split('.')[3])]) #tell receiver it has a client

    def disconnected(self):
        self.hasClient = False #tell itself it has a client
        if hasattr(self, 'clientAddress'):
            self.localOutQ.put([0, 1, int(self.clientAddress[0].split('.')[3])]) #tell receiver it has a client

class TCPServerReceiver(TCPServer):
    'Communication between two devices using python'
    def __init__(self, host, port, q, localInQ, localOutQ):
        super().__init__(host, port, q)
        self.q = q
        self.localInQ = localInQ
        self.localOutQ = localOutQ
        self.hasClient = False
        self.senderHasClient = False

    def run(self):
        while self.running:
            self.listen()
            self.doReceiverTask()

    def checkLocalQ(self):
        while not self.localInQ.empty():
            signal = self.localInQ.get()
            if signal[0] == 0: #make sure its a system command
                if signal[1] == 0: #sender got a connection
                    self.senderHasClient = True
                    if hasattr(self, 'clientAddress'):
                        self.q.put(self.pack([0, 0, int(self.clientAddress[0].split('.')[3])])) #tell the outside world sender have client
                elif signal[1] == 1: #sender lost its connection
                    self.senderHasClient = False
                    if hasattr(self, 'clientAddress'):
                        self.q.put(self.pack([0, 1, int(self.clientAddress[0].split('.')[3])])) #tell the outside world sender lost a client

    def connected(self):
        self.hasClient = True #tell itself it has a client
        if hasattr(self, 'clientAddress'):
            self.localOutQ.put([0, 2, int(self.clientAddress[0].split('.')[3])]) #tell sender it has a client
            self.q.put(self.pack([0, 2, int(self.clientAddress[0].split('.')[3])])) #tell the outside world i have client
        
    def disconnected(self):
        self.hasClient = False #tell itself it has a client
        if hasattr(self, 'clientAddress'):
            self.localOutQ.put([0, 3, int(self.clientAddress[0].split('.')[3])]) #tell sender it has a client
            self.q.put(self.pack([0, 3, int(self.clientAddress[0].split('.')[3])])) #tell the outside world i have client

class TCPClient(TCP):
    'Communication between two devices using python'
    def __init__(self, host, port, q):
        super().__init__(host, port, q)

    def connect(self):
        self.settimeout(1)
        self.checkLocalQ()
        try:
            super().connect((self.host,self.port))
            self.settimeout(None)
            self.client = self #for a clean syntax of
            self.connected()
            print("i'm Client connected")
        except ConnectionRefusedError:
            print("Connection refused error")
        except socket.timeout:
            print("Client connect timeout")

    def pack(self, data):
        return super().pack(self.commandStruct, data)
        
    def unpack(self, dataBin):
        return super().unpack(self.dataStruct, dataBin)

    def clean(self):
        pass

    def stop(self):
        self.running = False

class TCPClientSender(TCPClient):
    'Communication between two devices using python'
    def __init__(self, host, port, q, localInQ, localOutQ):
        super().__init__(host, port, q)
        self.localInQ = localInQ
        self.localOutQ = localOutQ
        self.hasClient = False
        self.receiverHasClient = False

    def run(self):
        super().connect()
        self.doSenderTask()
        self.close()
        self.disconnected()
        print("client sender exited")

    def checkLocalQ(self):
        while not self.localInQ.empty():
            signal = self.localInQ.get()
            if signal[0] == 0: #make sure its a system command
                if signal[1] == 2: #receiver got a connection
                    self.receiverHasClient = True
                elif signal[1] == 3: #receiver lost its connection
                    self.receiverHasClient = False
                    self.stop()

    def connected(self):
        self.hasClient = True #tell itself it has a client
        self.localOutQ.put([0, 0, int(self.host.split('.')[3])]) #tell receiver it has a client

    def disconnected(self):
        self.hasClient = False #tell itself it has a client
        self.localOutQ.put([0, 1, int(self.host.split('.')[3])])

class TCPClientReceiver(TCPClient):
    'Communication between two devices using python'
    def __init__(self, host, port, q, localInQ, localOutQ):
        super().__init__(host, port, q)
        self.q = q
        self.localInQ = localInQ
        self.localOutQ = localOutQ
        self.hasClient = False
        self.senderHasClient = False

    def run(self):
        super().connect()
        self.doReceiverTask()
        self.close()
        self.disconnected()
        while self.senderHasClient and self.running: #help sender to communicate with the outside until it dies
            print("client receiver still runing")
            self.checkLocalQ()
        print("client receiver exited")

    def checkLocalQ(self):
        while not self.localInQ.empty():
            signal = self.localInQ.get()
            if signal[0] == 0: #make sure its a system command
                if signal[1] == 0: #sender got a connection
                    self.senderHasClient = True
                    print("serder has client to true")
                    self.q.put(self.pack([0, 0, int(self.host.split('.')[3])])) #tell the outside world sender have client
                elif signal[1] == 1: #sender lost its connection
                    self.senderHasClient = False
                    self.q.put(self.pack([0, 1, int(self.host.split('.')[3])])) #tell the outside world sender lost a client
                    self.disconnected()


    def connected(self):
        self.hasClient = True #tell itself it has a client
        self.localOutQ.put([0, 2, int(self.host.split('.')[3])]) #tell sender it has a client
        self.q.put(self.pack([0, 2, int(self.host.split('.')[3])])) #tell the outside world i have client
        
    def disconnected(self):
        self.hasClient = False #tell itself it has a client
        self.localOutQ.put([0, 3, int(self.host.split('.')[3])]) #tell sender it has a client
        self.q.put(self.pack([0, 3, int(self.host.split('.')[3])])) #tell the outside world i have client

class BiDirectionalTCP(object):
    """Multithreading implimentation of bi diractional TCP: sender and receiver."""
    def __init__(self, ipAddress, isServer):
        self.ipAddress = ipAddress
        self.isServer = isServer
        self.outQ = None
        self.inQ = None
        self.sender = None
        self.receiver = None
    
    def stop(self):
        if self.outQ == None or self.inQ == None or self.sender == None and self.receiver == None:
            pass #nothing to stop
        else:
            if self.sender.isAlive():
                while not self.outQ.empty(): #wait for the stop command to send
                    sleep(0.01)
                self.sender.stop()
                self.sender.join()
            if self.receiver.isAlive():
                self.receiver.stop()
                self.receiver.join()

    def start(self, ipAddress = None):
        self.stop()
        self.outQ = Queue()
        self.inQ = Queue()
        localSenderOutQ = Queue() #talk to sender via this queue
        localSenderInQ = Queue() #talk to receiver via this queue

        if ipAddress == None: ipAddress = self.ipAddress
        if self.isServer:
            self.sender = TCPServerSender(host = ipAddress, port = DATA_PORT, q = self.outQ, localInQ = localSenderInQ, localOutQ = localSenderOutQ)
            self.receiver = TCPServerReceiver(host = ipAddress, port = COMMAND_PORT, q = self.inQ, localInQ = localSenderOutQ, localOutQ = localSenderInQ)
        else:
            self.sender = TCPClientSender(host = ipAddress, port = COMMAND_PORT, q = self.outQ, localInQ = localSenderInQ, localOutQ = localSenderOutQ)
            self.receiver = TCPClientReceiver(host = ipAddress, port = DATA_PORT, q = self.inQ, localInQ = localSenderOutQ, localOutQ = localSenderInQ)
        self.sender.start()
        self.receiver.start()

    def send(self, data):
        if type(data) == list:
            data = self.pack(data)
        self.outQ.put(data)

    def pack(self, data):
        return self.sender.pack(data)

    def unpack(self, data):
        return self.sender.unpack(data)


    def newPackage(self, messageLength): # only return valid data
        if not self.inQ.empty():
            data = self.inQ.get() #get binary data from receiver queue
            def iter():
                for i in range(0, len(data), messageLength):
                    dataList = self.unpack(data[i: i + messageLength])
                    if sum(dataList)%256 == 0: #check sum
                        if dataList[0] == 0:
                            #system commands
                            pass
                    yield dataList
            return iter()
        else:
            return None


class Robot(BiDirectionalTCP):
    def __init__(self, ipAddress):
        super().__init__(ipAddress = ipAddress, isServer = False)

    def motor(self, device, value):
        self.send([1, device, value])

    def getNewData(self): # only return valid data
        return self.newPackage(DATA_LENGTH)

class Controller(BiDirectionalTCP):
    def __init__(self, ipAddress):
        super().__init__(ipAddress = ipAddress, isServer = True)

    def getNewCommands(self): # only return valid data
        return self.newPackage(COMMAND_LENGTH)