#include <Wire.h>
#define MESSAGE_LENGTH 8
#define I2CAddress 7
#define LINEAR_ACTUATOR_1 1
void i2cSetup() {
	Wire.begin(I2CAddress);
	Wire.setClock(96000L);
	Wire.onReceive(onI2CReceive);
	Wire.onRequest(onI2CRequest);
}

void onI2CReceive(int numByte) {
	int message[MESSAGE_LENGTH];
	//int i = 0;

	for (int i = 0; i < numByte; i++) {
		message[i] = Wire.read();

	}
	int command = message[0];
	switch (command)
	{
	case 1:
		Pos = map(message[2], 0, 100, 143, 4450);
		break;
	default:
		break;
	}
}

void onI2CRequest() {
	int scaledPos = map(Pos, 143, 4450, 0, 100);
	int scaledCurrentPos = map(LA_status.value(), 143, 4450, 0, 100);
	int scaledSpeed = map(Speed, 0, 500, 0, 5);
	Wire.write(LINEAR_ACTUATOR_1); // Device ID
	Wire.write(scaledPos); //Set Position
	Wire.write(scaledCurrentPos); //Current Pos
	Wire.write(scaledSpeed); // Speed

}