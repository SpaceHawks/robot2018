#include "Timer.h"
#include "PID.h"
int A = 6;
int B = 5;
int X = 7;
PIDClass pid = PIDClass();
int button = 12;
#include <Sabertooth.h>
Sabertooth ST(128);
int enCounter;

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
	ST.motor(1, pid.getPower(enCounter));
//	{@Plot.Power.Power.Green pid.power}, { @Plot.Speed.currentSpeed.Red pid.currentSpeed }, { @Plot.Speed.setSpeed.Green pid.setSpeed }, { @Plot.Constant.kp.Blue pid.kp }, { @Plot.Constant.ki.Red pid.ki }, { @Plot.Constant.kd.Green pid.kd }, pid.kp is{ pid.kp = ? }, pid.ki is{ pid.ki = ? }, pid.kd is{ pid.kd = ? }, pid.power is{ pid.power = ? }, pid.setSpeed is{ pid.setSpeed = ? }
}

float map1(long x, long in_min, long in_max, float out_min, float out_max){
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void speedchg() {
	if (pid.targetVal == 0)
		pid.setTargetVal(300);
	else
		pid.setTargetVal(0);
}
	
void count() {
  if (digitalRead(B) == LOW)
    enCounter++;
  else
	enCounter--;
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
