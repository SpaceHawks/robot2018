from tcp import Controller
from time import sleep
import socket
ipAddress = socket.gethostbyname(socket.getfqdn())
print("server: ", ipAddress)
pc = Controller(ipAddress)
pc.start()

while 1:
    messages = pc.getNewMessages()
    if messages is not None:
        for message in messages:
            s = ""
            if message[0] == 0:
                s+="System: "
                if message[1] == 0:
                    s+=" TCP Status "
                    if message[2] == 0:
                        s+=" Sender "+ str(message[3]) +" connected "
                    elif message[2] == 1:
                        s+=" Sender "+ str(message[3]) +" disconnected "
                    elif message[2] == 2:
                        s+=" Receiver "+ str(message[3]) +" connected "
                    elif message[2] == 3:
                        s+=" Receiver "+ str(message[3]) +" disconnected "
            elif message[0] == 1:
                s+="Manual control: "
                if message[1] == 0:
                    s+=" EMERGENCY STOP!"
                elif message[1] == 10:
                    s+="Drive at " + str(message[2]) + " Turn at " + str(message[3])
            print(s)



