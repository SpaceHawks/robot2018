#include "RMCKangaroo2.h"

/*!
Constructor
*/
LinearActuator::LinearActuator(KangarooSerial& K, char name):KangarooChannel(K, name)
{
}
/*!
Initiates the Kangaroo. Gets min and max positions for Linear Actuator.
*/
void LinearActuator::begin() {
	start();
	getExtremes();
}
/*!
Extends Linear Actuator to target position with set speed while in range.
Powers down when completed.
*/
void LinearActuator::loop()
{
	if (targetVal >= min && targetVal <= max && (targetVal != lastVal || speed != lastSpeed )) {
		done = false;
		p(targetVal, speed);
		lastVal = targetVal;
		lastSpeed = speed;
	}

	status = getP();
	if (status.done()) {
		powerDown();
		done = true;
	}
}
/*!
Computes min and max values for position of Linear Actuator. 
Sets default max Speed.
*/
void LinearActuator::getExtremes()
{
		long absMin = getMin().value();
		long absMax = getMax().value();
		long safeBound = (absMax - absMin)*0.02;
		min = (absMin + safeBound);
		max = absMax - safeBound;
		maxSpeed =208;
		//maxSpeed = 0.5 * (absMax - absMin);
		Serial.println("max speed is: " + String(maxSpeed));
}
/*!
Sets target position for Linear Actuator between 0 and 100.
*/
void LinearActuator::setTargetPosDirect(long pos)
{
	if (targetVal >= min && targetVal <= max) {
		targetVal = pos;
	}
}
/*!
Sets target position and speed for Linear Actuator.
*/
void LinearActuator::setTargetVal(long pos, long newSpeed) { //val = 0% to 100%
	setTargetPos(pos);
	setSpeed(newSpeed);
}
/*!
Sets target position for Linear Actuator scaled between min and max.
*/
void LinearActuator::setTargetPos(long pos) { 
	if (pos >= 0 && pos <= 100) {
		targetVal = map(pos, 0, 100, min, max);
	}
}
/*!
Sets speed for Linear Actuator scaled between 0 and max speed.
*/
void LinearActuator::setSpeed(long newSpeed) { 
	if (newSpeed >= 0 && newSpeed <= 100) {
		speed = map(newSpeed, 0, 100, 0, maxSpeed);
	}
}
/*!
Gets current position of Linear Actuator.
*/
long LinearActuator::getCurrentVal()
{
	return status.value();
}
/*!
Constructor
Instantiates PID control object. Sets default values and range.
Instaites objects to control Linear Actuators individually.
*/
LinearActuatorPair::LinearActuatorPair(KangarooSerial & K, char name)
{
	syncPID = new PID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
	Setpoint = 0;
	syncPID->SetMode(AUTOMATIC);
	syncPID->SetOutputLimits(-5, 5);
	channel[0] = new LinearActuator(K, name);
	channel[1] = new LinearActuator(K, name+1);
}
/*!
\
*/
long * LinearActuatorPair::getCurrentVal()
{
	return nullptr;
}
long LinearActuatorPair::getPos()
{
	return map(channel[0]->status.value(), channel[0]->min, channel[0]->max, 0, 100);
}
/*!
\
*/
void LinearActuatorPair::setSpeed(long newSpeed)
{// set speed in the range if 0 - 100
	if (newSpeed != lastSpeed && newSpeed >= 0 && newSpeed <= 100)
	{
		channel[0]->setSpeed(newSpeed);
		channel[1]->setSpeed(newSpeed);
		lastSpeed = newSpeed; //fix this
		speed = newSpeed;
	}
}
/*!
Sets target value for position of Linear Actuator.
*/
void LinearActuatorPair::setTargetPos(long pos)
{
	targetVal = pos;
}
/*!
Computes gap between Linear Actuators and fixes it if greater than tolerance.
Moves Linear Actuator Pair to target value controlled by PID. 
Executes loops of all channels.
*/
void LinearActuatorPair::loop()
{
	long tempTargetVal = targetVal;
	if (channel[0]->done && channel[1]->done)
	{
		channel[0]->setTargetPos(tempTargetVal);
		channel[1]->setTargetPos(tempTargetVal);
	}
	else
	{
		long la1 = channel[0]->status.value();
		long la2 = channel[1]->status.value();
		Input = la2-la1;
		long gap = Input;
		syncPID->Compute();
		//Serial.println(String(targetVal)+"     "+String(Output));
		long scaledLa1 = map(la1, channel[0]->min, channel[0]->max, 0, 100);
		long scaledLa2 = map(la2, channel[0]->min, channel[0]->max, 0, 100);
		if ((tempTargetVal - scaledLa1) > 1)
		{
			channel[1]->setSpeed(speed + Output);
		}
		else if ((tempTargetVal - scaledLa1) < -1)
		{
			channel[1]->setSpeed(speed - Output);
		}

		//Serial.println(gap);
		if (abs(gap) > 25){
			if (!isSyncing) {
				isSyncing = true;
				
				channel[0]->setTargetPosDirect(la1);
				channel[1]->setTargetPosDirect(la1);
			}
		}
		else {
			if (isSyncing && abs(gap) < 15)
			{
				isSyncing = false;
			}
			channel[0]->setTargetPos(tempTargetVal);
			channel[1]->setTargetPos(tempTargetVal);
		}
	}
	
	channel[0]->loop();
	channel[1]->loop();
}
/*!
Executes begin methods of all channels.
Sets speed of Linear Actuator.
*/
void LinearActuatorPair::begin()
{
	
	channel[0]->begin();
	channel[1]->begin();
	setSpeed(94);
}
Motor::Motor(KangarooSerial& K, char name) :KangarooChannel(K, name)
{
}
void Motor::begin()
{
	start();
}
void Motor::setTargetPos(long pos)
{
	mode = 1;
	targetPos = pos;
}
void Motor::loop()
{
	long tempSpeed = speed;
	//Serial.println("tempSpeed "+String(tempSpeed));
	//Serial.println("lastSpeed " + String(lastSpeed));
	//Serial.println("speedLimit " + String(speedLimit));
	if (tempSpeed != lastSpeed && tempSpeed >= -speedLimit && tempSpeed <= speedLimit)
	{
		s(tempSpeed);
		lastSpeed = tempSpeed;

	}
	status = getS();
}
void Motor::setTargetSpeed(long speed) {
	if (speed >= -100 && speed <= 100) {
		this->speed = map(speed, -100, 100, -speedLimit, speedLimit);
	}
}
long Motor::getCurrentSpeed()
{
	return status.value();
}
void Motor::setSpeedLimit(long speed)
{
	if (speed > 0) {
		speedLimit = speed;
	}
}
void Motor::move(long angle, long speed)
{
	long val = angle / 360 * 2040;
	pi(val, speed).wait();
	//done = true;
}

Motors::Motors(KangarooSerial & K, char name)
{
	channel[0] = new Motor(K, name);
	channel[1] = new Motor(K, name + 1);
	channel[2] = new Motor(K, name + 2);
	channel[3] = new Motor(K, name + 3);
	for (int i = 0;i < 4;i++) {
		channel[i]->setSpeedLimit(3000);
	}

}
void Motors::loop()
{
	for (int i = 0; i < 4; i++) {
		channel[i]->mode = mode;
	}
	if (mode == 1 && alreadySetTargetPos == false) {
		if (angle <= 180 && angle >= -180) {
			long leftPos;
			long rightPos;
			if (angle < 0)
			{
				leftPos = -angle;
				rightPos = angle;
			}
			else if (angle > 0)
			{
				leftPos = angle;
				rightPos = -angle;
			}
			else {
				leftPos = targetPos;
				rightPos = targetPos;
			}
			channel[FRONT_LEFT]->setTargetPos(-leftPos);
			channel[FRONT_RIGHT]->setTargetPos(-rightPos);
			channel[REAR_LEFT]->setTargetPos(leftPos);
			channel[REAR_RIGHT]->setTargetPos(rightPos);
			alreadySetTargetPos = true; //fix this
		}
	}
	long tempTurn = turn;
	long tempDrive = drive;
	if ((tempDrive <= 100 && tempDrive >= -100) && (tempTurn <= 100 && tempTurn >= -100)) {
		long leftSpeed = tempDrive;
		long rightSpeed = tempDrive;
		if (tempTurn == -100) {
			leftSpeed = -tempDrive;
		}
		else if (tempTurn < 0 && tempTurn >-100) {
			leftSpeed = tempDrive * (1 + (float)tempTurn / 100);
		}
		else if (tempTurn == 0) {
		}
		else if (tempTurn < 100 && tempTurn > 0) {
			rightSpeed = tempDrive * (1 - (float)tempTurn / 100);
		}
		else if (tempTurn == 100) {
			rightSpeed = -tempDrive;
		}
		channel[FRONT_LEFT]->setTargetSpeed(-leftSpeed);
		channel[FRONT_RIGHT]->setTargetSpeed(-rightSpeed);
		channel[REAR_LEFT]->setTargetSpeed(leftSpeed);
		channel[REAR_RIGHT]->setTargetSpeed(rightSpeed);
	}
	for (int i = 0; i < 4; i++)
	{
		if (channel[i]->done == true)
		{
			channel[i]->done == false;
			channel[i]->setTargetSpeed(0);
		}
		channel[i]->loop();
	}
}
void Motors::begin()
{
	for (int i = 0; i < 4; i++) {
		channel[i]->begin();
	}
}
long Motors::getLeftMotorS()
{
	return map(-channel[FRONT_LEFT]->status.value(), -(channel[FRONT_LEFT]->speedLimit), channel[FRONT_LEFT]->speedLimit, -100, 100);
}

long Motors::getRightMotorS()
{
	return map(-channel[FRONT_RIGHT]->status.value(), -(channel[FRONT_RIGHT]->speedLimit), channel[FRONT_RIGHT]->speedLimit, -100, 100);
}

void Motors::setDrive(long drive)
{
	if (drive >= -100 && drive <= 100) {
		this->drive = drive;
	}
}
void Motors::setTurn(long turn)
{
	if (turn >= -100 && turn <= 100) {
		this->turn = turn;
	}
}
void Motors::clearAngle()
{
	angle = 0;
}
void Motors::setPos(long pos)
{
	mode = 1;
	targetPos = pos*2040;
	alreadySetTargetPos == false;
}
void Motors::setAngle(long angle)
{
	if (angle >= -180 && angle <= 180)
	{
		mode = 1;
		this->angle = angle*2040;
		alreadySetTargetPos == false;
	}
}
/*!
Constructor. Initilizes Arduino pins connected to the Kangaroo.
\param potPin the Arduino analog pin number. Default is 0.
*/
RMCKangaroo2::RMCKangaroo2(USARTClass &serial)
{
	SerialPort = &serial;
	K = new KangarooSerial(*SerialPort);
	motors = new Motors(*K, '3');
	//linearActuatorPair = new LinearActuatorPair(*K, '1');
}
/*!
Executes the loop of the right Linear Actuator
*/
void RMCKangaroo2::loop()
{
	motors->loop();
	//linearActuatorPair->loop();
}
/*!
Initiates Serial Communication.
Executes begin methods of all Linear Actuators and Motors.
*/
void RMCKangaroo2::begin() {
	//Serial.println("before");
	SerialPort->begin(9600);
	//delay(1000);
//	Serial.print("Error");
	//SerialPort->listen();
	motors->begin();
	//linearActuatorPair->begin();
}