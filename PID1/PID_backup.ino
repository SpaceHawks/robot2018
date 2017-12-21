
int A = 6;
int B = 5;
int X = 7;
int counter = 0;
int setspeed = 0;
int button = 12;
#include <Sabertooth.h>
Sabertooth ST(128);
int power = 0;
float kp = 0.03;
float ki = 0.1;
float kd = 0.05;
int sum_error = 0;
int lastError = 0;
int goalSpeed = 0;
void setup() {
	// put your setup code here, to run once:
	SabertoothTXPinSerial.begin(9600); // 9600 is the default baud rate for Sabertooth packet serial.
	ST.autobaud(); // Send the autobaud command to the Sabertooth controller(s).
	attachInterrupt(digitalPinToInterrupt(A), count, RISING);
	pinMode(B, INPUT);
	pinMode(button, INPUT);
	attachInterrupt(digitalPinToInterrupt(button), speedchg, RISING);
	Serial.begin(9600);

}

void loop() {
	// put your main code here, to run repeatedly:

	int sensorValue3 = analogRead(A3);
	// float voltage3 = sensorValue3 * (3.3 / 1023.0);
	// power = map(sensorValue3, 0, 1023, -127, 127);
	//  Serial.print("Speed changed to " + String(power) + "  ");
	//  ST.motor(1, power);
	int currentSpeed = counter;
	setspeed = (goalSpeed - currentSpeed)*.75 + currentSpeed;
	counter = 0;
	int error = (setspeed - currentSpeed);
	int chgError = error - lastError;
	lastError = error;
	sum_error += error;
	if (setspeed == 0 && currentSpeed == 0)
		power = 0;
	else
		power = error*kp + ki*sum_error + (kd / 3)*chgError;

	ST.motor(1, power);
	delay(100);
}

float map1(long x, long in_min, long in_max, float out_min, float out_max) {
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void speedchg() {
	if (goalSpeed == 0)
		goalSpeed = 300;
	else
		goalSpeed = 0;
}

void count() {
	if (digitalRead(B) == LOW)
		counter++;
	else
		counter--;
}

void motor() {
	int power;

	// Ramp motor 1 from -127 to 127 (full reverse to full forward),
	// waiting 20 ms (1/50th of a second) per value.
	for (power = 0; power <= 127; power += 10)
	{
		SerialUSB.println("current power:" + String(power));

		ST.motor(1, power);

		delay(6000);

	}
	power = 0;
	ST.motor(1, power);
}
