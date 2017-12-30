//#include "Sabertooth.ino"
#include <Kangaroo.h>
#include "RMCKangaroo1.h"
#include <Wire.h>

#define MESSAGE_LENGTH 8
#define I2CAddress 7
#define LINEAR_ACTUATOR_1 1
/*Not all pins on the Mega and Mega 2560 support change interrupts, so only the following can be used for RX: 10, 11, 12, 13, 14, 15, 50, 51, 52, 53, A8 (62), A9 (63), A10 (64), A11 (65), A12 (66), A13 (67), A14 (68), A15 (69).
*/

RMCKangaroo1 motorK(10, 11, "13", "lm");
long setValue = 1000;
long setSpeed=50;
long setMotorSpeed = 15000;
//At a higher resoultion, speed limit is lower

void setup() {
	pinMode(4, OUTPUT);
	digitalWrite(4, HIGH);
	Serial.begin(9600);
	motorK.begin();
	motorK.setTargetPos(1, setValue);
	motorK.setTargetSpeed(3, 50);
	motorK.setMotorMaxSpeed(3, 20000);
	i2cSetup();
}
void loop() {
	digitalWrite(4, LOW);
	motorK.loop();
	digitalWrite(4, HIGH);
	delay(100);
	//{@Plot.Position.Max.Red motorK.max1}, {@Plot.Position.Min.Green linearK.min1}, setValue is {setValue =?},  {@Plot.Speed.SetSpeed.Red setMotorSpeed}, {@Plot.Speed.CurrentSpeed.Green motorK.status1->value()}, setMotorSpeed is {setMotorSpeed =?}

}


void i2cSetup() {
	Wire.begin(I2CAddress);
	Wire.setClock(96000L);
	Wire.onReceive(onI2CReceive);
	Wire.onRequest(onI2CRequest);
}

void onI2CReceive(int numByte) {
	int message[MESSAGE_LENGTH];
	int i = 0;

	for (int i = 0; i < numByte; i++) {
		message[i] = Wire.read();

	}
	int command = message[0];
	int deviceID = message[1];
	int val = message[2];
	
	switch (command)
	{
	case 1:
		switch (deviceID)
		{
		case 1:
			motorK.setTargetPos(deviceID, val);
			Serial.println(val);
			break;
		case 3:
			motorK.setTargetSpeed(deviceID, (signed char)val);
			break;
		default:
			break;
		}
	default:
		break;
	}
	
}

void onI2CRequest() {
	//int scaledTargerVal = map(linearK.targetVal1, 143, 4450, 0, 100);
	//int scaledCurrentVal = map(linearK.status1.value(), 143, 4450, 0, 100);
	//int scaledSpeed = map(linearK.speed1, 0, 500, 0, 5);
	//Wire.write(LINEAR_ACTUATOR_1); // Device ID
	//Wire.write(scaledTargerVal); //Set Value
	//Wire.write(scaledCurrentVal); //Current Value
	//Wire.write(scaledSpeed); // Speed for L.Actuator, motor will ignore
}

