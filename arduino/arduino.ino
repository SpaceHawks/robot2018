//#include "Sabertooth.ino"
//#include "RMCKangarooChannel.h"
//#include "RMCKangaroo1.h"
#include <Wire.h>

//#include "Sabertooth.ino"
#include "RMCKangaroo2.h"


#define MESSAGE_LENGTH 8
#define I2CAddress 7
/*Not all pins on the Mega and Mega 2560 support change interrupts, so only the following can be used for RX: 10, 11, 12, 13, 14, 15, 50, 51, 52, 53, A8 (62), A9 (63), A10 (64), A11 (65), A12 (66), A13 (67), A14 (68), A15 (69).
*/
RMCKangaroo1 motorK(51, 50, "1", "p");
//At a higher resoultion, speed limit is lower

void setup() {
	Serial.begin(9600);
	
	
	//motorK.setTargetSpeed(3, 50);
	//motorK.setMotorMaxSpeed(3, 20000);
	i2cSetup();
	Serial.println("start begin setup");
	motorK.begin();
	Serial.println("end setup");
}
void loop() {
	
	motorK.loop();
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
	int systemCommand = message[0];
	// 1 - from a controller
	// 2 - from the pi directly
	// 3 - x
	int command = message[1];
	int device = message[2];
	int value = message[3];
	switch (systemCommand)
	{
	case 0:
		break;
	case 1: //pass through
		switch (command)
		{
		case 1:
			switch (device)
			{
			case 1:
				motorK.setTargetVal(device, value);
				break;
			case 2:
				motorK.setTargetVal(device, value);
				break;
			
			case 3:
				motorK.setTargetVal(device, (signed char)value);
				break;
			case 4:
				motorK.setTargetVal(device, (signed char)value);
				break;
			case 5:
				break;
			case 6: //channel 1 and 2 together
				motorK.setTargetVal(1, value);
				motorK.setTargetVal(2, value);
				break;
			default:
				break;
			}
			Serial.println(value);
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

