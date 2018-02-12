import smbus
import time
bus = smbus.SMBus(1)
address = 0x04


#Send one byte
def writeOneByte(value):
    global bus
    global address
    bus.write_byte(address, value)
    return -1

def readOneByte():
    global bus
    global address
    number = bus.read_byte(address)
    return number

def sendSingleBytes():
    for i in range(127):
        writeOneByte(i)
        print ('RPI: Hi Arduino, I sent you ', i)
        time.sleep(1)
        number = readOneByte()
        print ('Arduino: Hey RPI, I received ', number)

#Send multiple bytes
def writeMulBytes():
    global bus
    global address
    bus.write_block_data(address, 0, [2,3,6,8,9])
    return -1

def sendMulBytes():
    writeMulBytes()
    print("Sent 2,3,6,8,9")


def main():
    sendSingleByte()

if __name__ == '__main__':
    main()
        
