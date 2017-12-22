//Arduino PID library: https://playground.arduino.cc/Code/PIDLibrary
#include <PID_v1.h>
#include <Sabertooth.h>
Sabertooth ST(128);
int A = 6;
int B = 5;
int X = 7;
int power;

double Setpoint, Input, Output; //Define Variables we'll be connecting to
double kp = 0.01, ki = 0.5, kd = 0;
//0.01, 0.2, 0.009 - Optimum 12/21 3.18pm - when sample time is 100ms
//0.01, 0.5, 0.001 - Optimum 12/21 3.42pm - when sample time is 100ms
//When kd is 0 , diff by 2 value max
//Specify the links and intial tuning parameters

PID myPID(&Input, &Output, &Setpoint, kp, ki, kd, DIRECT);
int tolerance = 5; //threshold for change kp

void motorSetup() {
	pinMode(B, INPUT_PULLUP);
	pinMode(A, INPUT_PULLUP);
	attachInterrupt(digitalPinToInterrupt(A), count, RISING);
	
	SabertoothTXPinSerial.begin(9600); // 9600 is the default baud rate for Sabertooth packet serial.
	ST.autobaud(); // Send the autobaud command to the Sabertooth controller(s).
	ST.motor(1, 0); //Stop motor when reset

	//Input = analogRead(PIN_POT); //initialize the variables we're linked to
	Setpoint = 100; // initial set point
	myPID.SetOutputLimits(-127, 127); // power limits of sabertooth
	myPID.SetMode(AUTOMATIC); //turn the PID on
	myPID.SetSampleTime(100); // 10ms works fine for Motor
	ST.address();
	ST.setTimeout(0);
}

void motorLoop() {
	myPID.SetTunings(kp, ki, kd);
	if (myPID.Compute() == true) {

		if (Setpoint == 0 && Input == 0)
			 power = 0;
		else
			 power = Output;
		
		ST.motor(1, power);
		Input = 0;
	}

//	if (abs(Input - Setpoint) < tolerance) kp = 0.1;
//	else kp = 3;
	//delay(300);
	//{@Plot.Pos.currentSpeed.Green Input}, {@Plot.Pos.targetSpeed.Blue Setpoint}, {@Plot.Power.Power.Red Output}, {@Plot.Constant.kp.Blue kp}, {@Plot.Constant.ki.Red ki}, {@Plot.Constant.kd.Green kd},kp is {kp=?}, ki is {ki=?}, kd is {kd=?}, Power is {Output=?}, Setpoint is {Setpoint =?}
}

void count() {
	if (digitalRead(B) == LOW)
		Input++;
	else
		Input--;
}