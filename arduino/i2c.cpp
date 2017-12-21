// 
// 
// 

#include "I2C.h"
I2CClass::I2CClass(int address)
{
	_address = address;
	init();
}
I2CClass::I2CClass()//fix this
{
}
void I2CClass::init()
{
	Wire.begin(_address);
}
void I2CClass::attach(voidFuncPtrInt receiveDataFunction, voidFuncPtr sendDataFunction)
{
	Wire.onReceive(receiveDataFunction);
	Wire.onRequest(sendDataFunction);
}
void I2CClass::receiveData(int byteCount) {
	int data[8];
	int i = 0;
	while (Wire.available()) {
		data[i] = Wire.read();
		i++;
	}
	if (data[0] == 1) //update left and right speed
	{
		leftTargetSpeed = data[1];
		rightTargetSpeed = data[2];
	}
	/*self.i2cCommands = { 'is_connected':0,
	'set_arm_address' : 1,
	'set_hand_address' : 2,
	'set_arm_height' : 3,
	'set_arm_height_offset' : 4,
	'set_arm_angle' : 5,
	'set_arm_angle_offset' : 6,
	'set_motor_speed' : 7,
	'set_motor_power' : 8,
	'set_arm_power' : 9,
	'set_hand_power' : 10,
	'set_hand_angle' : 11,
	'set_hand_angle_offset' : 12,
	'set_hand_height' : 13,
	'set_hand_height_offset' : 14,
	'set_motor_address' : 15,
	'stop_motor' : 16,
	'stop_arm' : 17,
	'stop_hand' : 18,
	}*/
}
void I2CClass::sendData() {//fix this
	Wire.write(leftTargetSpeed);
}
I2CClass I2C;