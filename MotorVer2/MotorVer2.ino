#include "RMCKangaroo.h"
RMCKangaroo motorK(Serial3);
void setup() {
	Serial1.begin(115200);
	Serial.begin(115200);
	motorK.begin();
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
		bool valid = verifyCheckSum(message, 5);
		while (!valid && Serial1.available())
		{
			for (int i = 4; i > 0; i--)
			{
				message[i] = message[i - 1];
			}
			message[0] = Serial1.read();
			valid = verifyCheckSum(message, 5);
			Serial.println("hieu");
		}
		if (valid)
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
				case 1:
					char *kangarooName = motorK.motors->currentSpeeds;
					char *errorStatus = motorK.motors->currentSpeeds;
					sendData(1, 10, kangarooName, errorStatus);
					sendData(1, 10, kangarooName, errorStatus);
					break;
				case 10:
					motorK.motors->setSpeedLimit(value1);
					motorK.getStatus();
					break;
				default:
					break;
				}
				break;
			case 1:
				switch (device)
				{
				case 0:
					//Emergency Stop. Should stop all motors
					motorK.motors->drive(0, 0);
					break;
				case 1:
					break;
				case 2:
					break;
				case 3:
					break;
				case 4:
					break;
				case 5://linear actuator pair
					motorK.linearActuatorPair->setTargetPosAndSpeed(value1, value2);
					break;
				case 6://linear actuator pair
					motorK.linearActuatorPair->setTargetPosAndSpeed(value1, value2);
					break;
				case 7:// auger on/off reverse/forward
					motorK.slider->setTargetPosAndSpeed(value1, value2);
					break;
				case 8:// auger on/off reverse/forward
					motorK.auger->setDirection(value1, value2);
					break;
				case 10:
					motorK.motors->drive((signed char)value1, (signed char)value2);
					break;
				case 11:
					motorK.motors->tankDrive((signed char)value1, (signed char)value2);
					break;
				case 12:
					motorK.motors->shutDown();
					break;
				default:
					Serial.println("unhanddle command: " + String(command) + " " + String(device) + " " + String(value1) + " " + String(value2));
					break;
				}
				break;
			case 3:
				switch (device)
				{
				case 0:

					break;
				case 1:
					//Serial1.write(motorK.motors->getFrRightMotorS());
					break;
				case 2:
					//Serial1.write(motorK.motors->getFrLeftMotorS());
					break;
				case 3:
					//Serial1.write(motorK.motors->getReLeftMotorS());
					break;
				case 4:
					//Serial1.write(motorK.motors->getReRightMotorS());
					break;
				case 5:
					//sendData(5, speeds[FRONT_LEFT], speeds[FRONT_RIGHT]);
					//Serial1.write(motorK.linearActuatorPair->getCurrentVal, 3);
					break;
				case 6:
				{
					//long *speedArr = motorK.linearActuatorPair -> getCurrentVal();
					//Serial.println(*speedArr);
					//Serial1.write(*speedArr, 3);
					break;
				}
				case 10:
				{
					//motorK.motors->getMotorSpeedS();
					//char spd[] = {speedArr[0], speedArr[1], speedArr[2], speedArr[3]};
					//char spd[] = { 20,20,20,20,-79 };

					//speeds[4] = getChecksum(speeds, 4);
					//Serial1.write(speeds, 5);

					char *speeds = motorK.motors->currentSpeeds;
					speeds[FRONT_LEFT] = -speeds[FRONT_LEFT];
					speeds[FRONT_RIGHT] = -speeds[FRONT_RIGHT];
					sendData(3, 10, speeds[FRONT_LEFT], speeds[FRONT_RIGHT]);
					sendData(3, 20, speeds[REAR_LEFT], speeds[REAR_RIGHT]);
					break;
				}
				default:
					break;
				}
				break;
			}
		}
		else {// com failed, stop all actuators
			motorK.motors->drive(0, 0); //should be all motors
		}
	}
}

void sendData(char  command, char device, char value1, char value2) {
	char data[] = { command, device, value1, value2, 0 };
	write(data, 4);
}

char getChecksum(char *data, int size) {
	char checksum = 256;
	for (int i = 0; i < size; i++)
	{
		checksum -= data[i];
	}
	return checksum;
}

void write(char *data, int size) {
	data[size] = getChecksum(data, size);
	Serial1.write(data, size + 1);
}

bool verifyCheckSum(char arrayNum[], int len) {
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
			Serial.print("Test" + arrayNum[i]);
			Serial.print("Test"+arrayNum[i]);
			Serial.print(" ");
		}
		Serial.println();
		return false;
	}
}