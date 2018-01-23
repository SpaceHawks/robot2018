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

//
//void LinearActuatorPair::setTargetVal(long pos, long newSpeed)
//{
//	Serial.println("LAPair setTargetVal is empty.");
//
//}

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


	//long tempTargetVal = targetVal;
	//long la1 = channel[0]->status.value();
	//long la2 = channel[1]->status.value();
	//Input = -(la1 - la2);
	//long gap = Input;
	//syncPID->Compute();
	//Serial.println(String(gap) + "     " + String(Output));
	//long scaledLa1 = map(la1, channel[0]->min, channel[0]->max, 0, 100);
	//if ((tempTargetVal - scaledLa1) > 5)
	//{
	//	channel[1]->setSpeed(speed + Output);
	//}
	//else if ((tempTargetVal - scaledLa1) < -5)
	//{
	//	channel[1]->setSpeed(speed - Output);
	//}

	////Serial.println(gap);
	//if (abs(gap) > 20)
	//{
	//	if (!isSyncing) {
	//		isSyncing = true;
	//		channel[0]->setTargetPosDirect(la1);
	//		channel[1]->setTargetPosDirect(la1);
	//	}
	//}
	//else {
	//	if (isSyncing && abs(gap) < 15)
	//	{
	//		isSyncing = false;
	//	}
	//	channel[0]->setTargetPos(tempTargetVal);
	//	channel[1]->setTargetPos(tempTargetVal);
	//}

	//channel[0]->loop();
	//channel[1]->loop();





}
	//	if (!syncHaveBeenDetected) //have not detected unsynced
	//	{
	//		syncHaveBeenDetected = true;
	//		if (la1 > la2)
	//		{

	//			channel[1]->forceStop = true;
	//		}
	//		if (la1 < la2)
	//		{
	//			channel[0]->forceStop = true;
	//		}
	//		Serial.println("is not Sync");
	//	}
	//}
	//else {
	//	if (syncHaveBeenDetected) {
	//		syncHaveBeenDetected = false;
	//		channel[0]->forceStart = true;
	//		channel[1]->forceStart = true;
	//		Serial.println("is Sync");
	//	}
	//}
	
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
		Serial.println("motor loop sent");
	}
}

//
void Motor::setTargetSpeed(long speed) {
	if (speed >= -100 && speed <= 100) {
		this->speed = map(speed, -100, 100, -speedLimit, speedLimit);
	}
}

//void Motor::setTargetVal(long val, long distance)
//{
//	setTargetSpeed(val);
//	//setTargetDistance(distance);
//}

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
//void Motor::moveAtSpeed(long val, long newSpeed)
//{
//
//}

//void motor::move(long val)
//{
//	long speedlimit = maxspeed;
//	pi(val, speedlimit);
//	//done = true;
//
//}
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
long Motors::setTargetVal(long drive, long turn)
{
	setDrive(drive);
	setTurn(turn);
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

void Motors::loop()
{
	long tempTurn = turn;

	long tempDrive = drive;
	if ((tempDrive <= 100 && tempDrive >= -100) && (tempTurn <= 100 && tempTurn >= -100)) {
		long leftSpeed = tempDrive;
		long rightSpeed = tempDrive;
		if (tempTurn == -100) {
			leftSpeed = -tempDrive;
			Serial.print(String(0) + " ");
		}
		else if (tempTurn < 0 && tempTurn >-100) {
			leftSpeed = tempDrive * (1 + (float)tempTurn / 100);
			Serial.print(String(1) + " ");
		}
		else if (tempTurn == 0) {
			Serial.print(String(2) + " ");
		}
		else if (tempTurn < 100 && tempTurn > 0) {
			rightSpeed = tempDrive * (1 - (float)tempTurn / 100);
			Serial.print(String(3) + " ");
		}
		else if (tempTurn == 100) {
			rightSpeed = -tempDrive;
			Serial.print(String(4) + " ");
		}
		Serial.println(String(leftSpeed) + " " + String(rightSpeed));
		channel[FRONT_LEFT]->setTargetSpeed(-leftSpeed);
		channel[FRONT_RIGHT]->setTargetSpeed(-rightSpeed);
		channel[REAR_LEFT]->setTargetSpeed(leftSpeed);
		channel[REAR_RIGHT]->setTargetSpeed(rightSpeed);
	}

	for (int i = 0;i < 4;i++) {
		channel[i]->loop();
	}
}

void Motors::begin()
{
	for (int i = 0;i < 4;i++) {
		channel[i]->begin();
	}
}

/*!
Constructor. Initilizes Arduino pins connected to the Kangaroo.
\param potPin the Arduino analog pin number. Default is 0.
*/
RMCKangaroo1::RMCKangaroo1(int rxPin, int txPin, String channelList, String channelType)
{
	this->channelList = channelList;
	this->channelType = channelType;
	SerialPort = new SoftwareSerial(rxPin, txPin);
	K = new KangarooSerial(*SerialPort);

	for (int i = 0; i < channelList.length(); i++) {
		channel[i] = new Motors(*K, channelList[i]);
		channelIndex[(int)(channelList[i] - 49)] = i; //if channel is 1, index is 0
	}
}
/*!
Executes the loop of the right Linear Actuator
*/
void RMCKangaroo1::loop()
{
	channel[0]->loop();

}

/*!
Initiates Serial Communication.
Executes begin methods of all Linear Actuators and Motors.
*/
void RMCKangaroo1::begin() {
	SerialPort->begin(9600);
	SerialPort->listen();

	for (int i = 0; i< channelList.length(); i++)
		channel[i]->begin();

	for (int i = 0; i < channelList.length(); i++) {
		if (channelType[i] == 'l') {
		}
		else if (channelType[i] == 'm') {
		}
	}
}
/*!
Sets target value to selected channel.
\param channel number, value.
*/
void RMCKangaroo1::setTargetVal(int channelName, long val) { //val = 0% to 100%
															 //int index = getChannelIndex(channelName);

															 //channel[0]->setTargetVal(val);
															 //channel[1]->setTargetVal(val);
															 //channel[index]->setTargetVal(val);

															 //if (val >= 0 && val <= 100) {
															 //	targetVal1 = map(val, 0, 100, channel[0]->min, channel[0]->max);
															 //}
	channel[0]->setDrive(val);
}
/*!
Sets target value to selected channel.
\param channel number, value.
*/
void RMCKangaroo1::setTargetVal1(int channelName, long val) { //val = 0% to 100%
															 //int index = getChannelIndex(channelName);

															 //channel[0]->setTargetVal(val);
															 //channel[1]->setTargetVal(val);
															 //channel[index]->setTargetVal(val);

															 //if (val >= 0 && val <= 100) {
															 //	targetVal1 = map(val, 0, 100, channel[0]->min, channel[0]->max);
															 //}
	channel[0]->setTurn(val);
}