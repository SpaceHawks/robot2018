import serial

port = serial.Serial("/dev/ttyS1", baudrate=115200, timeout=3.0)
i = 1
while True:
    port.write(bytes([i%256]))
    i+=1
    #print("printed")
