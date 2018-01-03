"""
#have to run 'sudo apt-get install python-smbus'
#in Terminal to install smbus
import smbus as smbus
#handle error when data slave is unavailable

commands:
1: drive motors
"""



import smbus2
class Arduino(smbus2.SMBus):
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
                #print(command, "failed")
                counter+=1
        return False
            
        #time.sleep(0.01)#must delay 0.01 second

    def read(self, numBytes):
        '''
        Request data from the Arduino via i2c connection.

        Args:
            numBytes: integer, number of bytes requesting
        '''
        return self.read_i2c_block_data(self.i2cAddress, 0, numBytes)

    def motor(self, device, value):
        '''
        Send a drive command to the arduino via i2c connection.

        Args:
            motorID: the motor to be driven. Values: 1, 2, 3, 4, ...
            power: power and dirrection of the motor. Values: [-127, 127]
        '''
        
        return self.write(1, [1, device, value])
