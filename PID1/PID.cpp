// 
// 
// 

#include "PID.h"
/*!
Constructor. Initilizes a PID object with given constants and period.
\param Kp PID propotional constant.
\param Ki PID integral constant.
\param Kd PID derivative constant.
\param dt update period.
*/
void PIDClass::init(float kp, float ki, float kd, int dt, int targetVal)
{
	 
	 this->targetVal = targetVal;
	 accuError = 0;
	 prevError = 0;
	 power = 0;
	if (dt > 0) this->dt = dt;
	if (kp > 0) this->kp = kp;
	if (kd > 0) this->kd = kd;
	if (ki > 0) this->ki = ki;
}

/*!
Gets the Sabertooth's power needed to maintain a target speed.
\return Sabertooth's motor power 
*/
int PIDClass::getPower(int &currentVal)
{
	if (timer.getTime() > dt)
	{
		
		int tempTargetVal = (targetVal - currentVal)*.75 + currentVal; //To smoothen the curve
		int error = (tempTargetVal - currentVal);
		int chgError = error - prevError;
		prevError = error;
		accuError += error;
		if (tempTargetVal == 0 && currentVal == 0)
			power = 0;
		else
			power = kp * error + ki * accuError + kd * chgError;
		currentVal = 0;
		timer.reset();
	}

	return power;
}

int PIDClass::getPower1(int currentVal)
{
	if (timer.getTime() > dt)
	{

	
		int error = (targetVal - currentVal);
		int chgError = error - prevError;
		prevError = error;
		accuError += error;
		if (error == 0)
			power = 0;
		else
			power = kp * error + ki * accuError + kd * chgError;

		timer.reset();
	}

	return power;
}

void PIDClass::setConstant(float kp, float ki, float kd)
{
	if (kp > 0) this->kp = kp;
	if (kd > 0) this->kd = kd;
	if (ki > 0) this->ki = ki;
}

void PIDClass::setTargetVal(int targetVal)
{
	this->targetVal = targetVal;
}

/*!
Constructor. Initilizes a PID object with default constants and period.
default values for cim motor w/o load
init(kp, ki, ki, dt);
*/
PIDClass::PIDClass() {
	init(0.03, 0.1, 0.05/3, 100, 0);
}

/*!
Constructor. Initilizes a PID object with given constants and period.
\param Kp PID propotional constant.
\param Kd PID derivative constant.
\param Ki PID integral constant.
\param dt update period.
*/
PIDClass::PIDClass(float kp, float ki, float kd) {
	init(kp, ki, kd, 100, 0);
}
PIDClass::PIDClass(float kp, float ki, float kd, int dt) {
	init(kp, ki, kd, dt, 0);
}
PIDClass::PIDClass(float kp, float ki, float kd, int dt, int targetVal) {
	init(kp, ki, kd, dt, targetVal);
}
PIDClass PID;

