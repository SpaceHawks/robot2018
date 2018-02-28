"""
commands:
1: drive motors
"""
from struct import Struct
from tcp import TCP
from queue import Queue
from time import sleep

class Robot(object):
    def __init__(self, ipAddress):
        self.sq = Queue()
        self.rq = Queue()
        self.struct = Struct('BBbB') #command, selector, value, checksum
        self.sender = TCP(isServer = False, isSender = True, host = ipAddress, port = 1234, q = self.sq)
        self.receiver = TCP(isServer = False, isSender = False, host = ipAddress, port = 5678, q = self.rq)

    def motor(self, device, value):
        self.send(1, device, value)

    def send(self, command, device, value):
        self.sq.put(self.struct.pack(command, device, value))

    def connect(self):
        self.sender.start()
        self.receiver.start()

    def listen(self):
        pass

    def disconnect(self):
        while not self.sq.empty():
            sleep(0.01)
        self.sender.running = False
        self.receiver.running = False
        self.sender.disconnect()
        self.receiver.disconnect()
        self.sender.join()
        self.receiver.join()