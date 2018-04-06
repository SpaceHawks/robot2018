#include "RMCKangaroo.h"
#include <Kangaroo.h>
RMCKangaroo motorK(Serial3);
void setup() {
	motorK.begin();
	Serial1.begin(115200);
	Serial.begin(115200);
	Serial.println("Motor control started!");
}

void loop() {
	motorK.loop();
	serialEvent();
}

void serialEvent() {
	while (Serial1.available() > 4) {
		char message[5];
		Serial1.readBytes(message, 5);
		bool valid = checkSum(message, 5);
		while (!valid && Serial1.available())
		{
			for (int i = 4; i > 0; i--)
			{
				message[i] = message[i - 1];
			}
			message[0] = Serial1.read();
			valid = checkSum(message, 5);
			Serial.println("hieu");
		}
		if(valid)
		{
			char command = message[0];
			char device = message[1];
			char value1 = message[2];
			char value2 = message[3];
			//Serial.println("Passed checksum: " + String(command) + " " + String(device) + " " + String(value1) + " " + String(value2));
			switch (command)
			{
			case 0:
				switch (device)
				{
				case 11:
					motorK.motors->setSpeedLimit(value1);
					break;
				default:
					break;
				}
			case 1:
				switch (device)
				{
				case 0:
					//Emergency Stop. Should stop all motors
					motorK.motors->drive(0,0);
					break;
				case 1:
					break;
				case 2:
					break;
				case 3:
					break;
				case 4:
					break;
				case 5:
					break;
				case 6: //channel 1 and 2 together
					break;
				case 7: // Send speed data once
					break;
				case 8: // Send continuous data
					break;
				case 10:
					motorK.motors->drive((signed char)value1, (signed char)value2);
					break;
				case 11:
					motorK.motors->tankDrive((signed char)value1, (signed char)value2);
					break;
				default:
					Serial.println("unhanddle command: " + String(command) + " " + String(device) + " " + String(value1) + " " + String(value2));
					break;
				}
			}
		}
		else {// com failed, stop all actuators
			motorK.motors->drive(0, 0); //should be all motors
		}
	}
}
bool checkSum(char arrayNum[], int len) {
	char sum = 0;
	for (int i = 0; i < len; i++)
	{
		sum += arrayNum[i];
	}
	if (sum == 0)
	{
		return true;
	}
	else
	{
		Serial.print("Checksum fails.");
		for (int i = 0; i < len; i++)
		{
			Serial.print(arrayNum[i]);
			Serial.print(" ");
		}
		Serial.println();
		return false;
	}
}