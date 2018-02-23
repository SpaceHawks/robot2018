//#include "Sabertooth.ino"
//#include "RMCKangarooChannel.h"
//#include "RMCKangaroo1.h"
//#include "SimpleTimer.h"
#include <Wire.h>
#include <Kangaroo.h>
// <PID_v1.h>
//#include "Sabertooth.ino"
#include "RMCKangaroo2.h"
#define MESSAGE_LENGTH 8
#define I2CAddress 7
/*Not all pins on the Mega and Mega 2560 support change interrupts, so only the following can be used for RX: 10, 11, 12, 13, 14, 15, 50, 51, 52, 53, A8 (62), A9 (63), A10 (64), A11 (65), A12 (66), A13 (67), A14 (68), A15 (69).
*/
int X_PIN = A0;
int Y_PIN = A1;
int Z_PIN = A2;
double aX = 0;
double aY = 0;
double aZ = 0;
double uX = 0;
double vX = 0;
float v[3];
int zeros[3];
long lastTime = 0;
//KangarooSerial  motorK(Serial3);
RMCKangaroo2  motorK(Serial3);
//SimpleTimer timer;
//RMCKangaroo2 motorK(10, 11);
//At a higher resoultion, speed limit is lower

void setup() {
	/*for (int i = 0; i < 3; i++)
	{
		zeros[i] = 0;
		v[i] = 0.0;
		for (int j = 0; j < 5; j++)
		{
			zeros[i] += analogRead(i);
			delay(1);
		}
		zeros[i] = zeros[i] / 5;
	}
	
	pinMode(X_PIN, INPUT);
	pinMode(Y_PIN, INPUT);
	pinMode(Z_PIN, INPUT);*/
	
	//motorK.setTargetSpeed(3, 50);
	
	
	motorK.begin();
	i2cSetup();
	Serial.println("start begin setup");
	Serial.println("end setup");
	//motorK.setMotorMaxSpeed(3, 20000);
		
	//motorK.setTargetVal(3,90);
//	timer.setInterval(1, acce);
}
void loop() {
	//timer.run();
	motorK.loop();
	//Serial.println(String(motorK.motors->getLeftMotorS())+ "speed"+String(motorK.motors->getLeftMotorS()));
	//{@Plot.Velocity.Velo.Red aX}, {@Plot.Position.Min.Green linearK.min1}, setValue is {setValue =?},  {@Plot.Speed.SetSpeed.Red setMotorSpeed}, {@Plot.Speed.CurrentSpeed.Green motorK.status1->value()}, setMotorSpeed is {setMotorSpeed =?}
	delay(1);
}

void acce() {
		for (int i = 0; i < 3; i++)
		{
			int diff = analogRead(i) - zeros[i];
			if (abs(diff) < 2) {
				diff = 0;
			}
			float a = 9.81*((((float)5 * (float)diff / 1023)) / 0.333);
			v[i] += a* ((float)1/ 1000);
		}
		//Serial.println(String(v[0])+" "+ String(v[1])+" "+ String(v[2]));
}

void i2cSetup() {
	Wire1.begin(I2CAddress);
	Wire1.setClock(96000L);
	Wire1.onReceive(onI2CReceive);
	Wire1.onRequest(onI2CRequest);
	
}

void onI2CReceive(int numByte) {
	int message[MESSAGE_LENGTH];
	int i = 0;
	for (int i = 0; i < numByte; i++) {
		message[i] = Wire1.read();
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
				motorK.motors->setDrive((signed char)value);
				motorK.motors->mode = 0;
				break;
			case 2:
				motorK.motors->setTurn((signed char)value);
				break;
			case 3:
				break;
			case 4:
				break;
			case 5:
				break;
			case 6: //channel 1 and 2 together
				break;
			case 8:
				motorK.motors->setPos(2);
				break;
			default:
				break;
			}
			//Serial.println(value);
		}
	default:
		break;
	}
}

void onI2CRequest() {
	int linearActPos = motorK.linearActuatorPair->getPos();
	int leftMotorSpeed = (motorK.motors->getLeftMotorS());
	int rightMotorSpeed =(motorK.motors->getRightMotorS());

	//Wire.write(LINEAR_ACTUATOR_1); // Device ID
	//Wire.write(linearActPos); //Linear actuator current position
	Wire1.write(leftMotorSpeed); //Speed for left motor speed
	Wire1.write(rightMotorSpeed); // Speed for right motor speed
}

