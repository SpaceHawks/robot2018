//Arduino PID library: https://playground.arduino.cc/Code/PIDLibrary
#include <PID_v1.h>
#include <Sabertooth.h>
Sabertooth ST(128);

#define PIN_POT A0
double Setpoint, Input, Output; //Define Variables we'll be connecting to
double kp = 3, ki = 0, kd = 0; //Specify the links and initial tuning parameters
PID myPID(&Input, &Output, &Setpoint, kp, ki, kd, DIRECT);
int tolerance = 5; //threshold for change kp

void LinearActuatorSetup() {
	SabertoothTXPinSerial.begin(9600); // 9600 is the default baud rate for Sabertooth packet serial.
	ST.autobaud(); // Send the autobaud command to the Sabertooth controller(s).
	ST.motor(1, 0); //Stop motor when reset

	Input = analogRead(PIN_POT); //initialize the variables we're linked to
	Setpoint = 500; // initial set point
	myPID.SetOutputLimits(-127, 127); // power limits of sabertooth
	myPID.SetMode(AUTOMATIC); //turn the PID on
	myPID.SetSampleTime(300); // 300ms works fine for Linear Actuator
}

void LinearActuatorLoop() {
	// read the input on analog pin 0:
	Input = analogRead(PIN_POT);
	myPID.SetTunings(kp, ki, kd);
	myPID.Compute();
	int power;
	if (abs(Input - Setpoint) < tolerance) kp = 0.1;
	else kp = 3;
	power = Output;
	ST.motor(1, power);
	//delay(300);
	//{@Plot.Pos.currentPos.Green Input}, {@Plot.Pos.targetPos.Blue Setpoint}, {@Plot.Power.Power.Red Output}, {@Plot.Constant.kp.Blue kp}, {@Plot.Constant.ki.Red ki}, {@Plot.Constant.kd.Green kd},kp is {kp=?}, ki is {ki=?}, kd is {kd=?}, Output is {Output=?}, Setpoint is {Setpoint =?}
}