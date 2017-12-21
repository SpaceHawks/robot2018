// PID.h
#include "Timer.h"
#ifndef _PID_h
#define _PID_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "Arduino.h"
#else
	#include "WProgram.h"
#endif

class PIDClass
{
 protected:

private:
	float kp;
	float ki;
	float kd;
	int accuError;
	int prevError;
	int dt;
	TimerClass timer;
	int power;

 public:
	PIDClass();
	PIDClass(float kp, float ki, float kd);
	PIDClass(float kp, float ki, float kd, int dt);
	PIDClass(float kp, float ki, float kd, int dt, int targetVal);
	void init();
	void init(float kp, float ki, float kd, int dt, int targetVal);
	int targetVal;
	int getPower(int &currentVal);
	int getPower1(int currentVal);
	void setConstant(float kp, float ki, float kd);
	void setTargetVal(int targetVal);

};

extern PIDClass PID;

#endif

