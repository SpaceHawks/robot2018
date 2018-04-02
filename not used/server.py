from tcp import Controller
from time import sleep, time

import socket
from arduino import Arduino

t1 = time()
positioning = False
setDist = 0

def getLocalIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP = '127.0.0.1'
    while IP is '127.0.0.1':
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            time.sleep(1)
    s.close()
    return IP

arduino = Arduino("/dev/ttyS1")
ipAddress = getLocalIP()
print("server: ", ipAddress)
pc = Controller(ipAddress)
pc.start()

def positionRobot():
    global positioning
    if positioning and setDist > 0 and setDist < 1000:
        pass
        #get sensor data
        #send motor command
    else:
        print("Distance out of range or positioning is False")

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
                        t1 = time()
                        s+=" Sender "+ str(message[3]) +" connected "
                    elif message[2] == 1:
                        s+=" Sender "+ str(message[3]) +" disconnected "
                        arduino.stop()
                    elif message[2] == 2:
                        s+=" Receiver "+ str(message[3]) +" connected "
                    elif message[2] == 3:
                        s+=" Receiver "+ str(message[3]) +" disconnected "
                        arduino.stop()
            elif message[0] == 1:
                s+="Manual control: "
                if message[1] == 0:
                    s+=" EMERGENCY STOP!"
                    positioning = False
                elif message[1] == 10:
                    s+="Drive at " + str(message[2]) + " Turn at " + str(message[3])
                if arduino.writeDirectly(list(message)) is False:
                    print("Failed at",message)
            elif message[0] == 2:
                s+="Partial autonomy: "
                if message[1] == 5:
                    s+=" Positioning for dumping: "
                    if message[2] == 0:
                        positioning = False
                        s+="OFF."
                    else:
                        setDist = message[2]*4
                        positioning = True
                        s+= str(setDist)+" mm."
            #print(s)
    #positionRobot()
            
    if time() - t1 > 1:
        arduino.stop()
        t1 = time()
        #print("E-stop")
        


