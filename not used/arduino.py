
"""
#have to run 'sudo apt-get install python-smbus'
#in Terminal to install smbus
import smbus as smbus
#handle error when data slave is unavailable

commands:
1: drive motors
"""

class ArduinoSerial():
    """
    An interface with Arduino, which is attached to the RPi by the serial pins.
    """
    def __init__(self, serialPort):
        self.serialPort = serial.Serial(serialPort, baudrate=115200, timeout=3.0)
    def write(self, message):
        return self.serialPort.write(message)            
    def read(self, numBytes):
        return None
    def motor(self, device, value1, value2):
        return self.write([1, device, value1, value2])
    def drive(self, drive, turn):
        return self.motor(10, drive, turn)
    def stop(self):
        return self.motor(0, 0, 0)
    


class Arduino(smbus2.SMBus):
    import smbus2
    """
    An interface with Arduino, which is attached to the RPi by the I2C pins.
    """
    def __init__(self, i2cAddress):
        '''
        Constructor. Init i2c connection.

        Args:
            i2cAddess: i2c address of the target Arduino.
        '''

        super().__init__(1)
        self.i2cAddress=i2cAddress

    def write(self, command, data):
        '''
        Send command to the Arduino via i2c connection.

        Args:
            command: unsigned char, the command.
            data: list of insigned chars, data describing the command.
        '''
        if not isinstance(data,list):
            data=[data,]

        counter = 0
        while counter < 5:
            try:
                self.write_i2c_block_data(self.i2cAddress, command, data)               
                return True
            except:
                counter+=1
        return False
            
    def read(self, numBytes):
        '''
        Request data from the Arduino via i2c connection.
        Args:
            numBytes: integer, number of bytes requesting
        '''
        counter = 0
        while counter < 5:
            try:
                return self.read_i2c_block_data(self.i2cAddress, 0, numBytes)
            except OSError:
                print("Request failed")
                counter+=1
        return False
    def motor(self, device, value1, value2):
        '''
        Send a drive command to the arduino via i2c connection.

        Args:
            device: the motor to be driven. Values: 1, 2, 3, 4, ...
            value1: power and dirrection of the motor. Values: [-127, 127]
            value2: power and dirrection of the motor. Values: [-127, 127]
        '''
        return self.write(1, [1, device, value1, value2])
    def stop(self):
        '''
        Send a drive command to the arduino via i2c connection.

        Args:
            device: the motor to be driven. Values: 1, 2, 3, 4, ...
            value1: power and dirrection of the motor. Values: [-127, 127]
            value2: power and dirrection of the motor. Values: [-127, 127]
        '''
        return self.motor(0, 0, 0)
