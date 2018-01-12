#include "RMCKangaroo2.h"


RMCKangaroo1::RMCKangaroo1(int rxPin, int txPin, String channelList, String channelType)
{
	this->channelList = channelList;
	this->channelType = channelType;
	SerialPort = new SoftwareSerial(rxPin, txPin);
	K = new KangarooSerial(*SerialPort);
	
	for (int i = 0; i < channelList.length(); i++) {
		channel[i] = new LinearActuatorPair(*K, channelList[i]);
		channelIndex[(int)(channelList[i]-49)] = i; //if channel is 1, index is 0
	}
}

void RMCKangaroo1::loop()
{
	channel[0]->loop();
	//for (int i = 0; i < 1; i++) {
	//	int tempTargetVal = targetVal[i];
	//	int tempLASpeed = linearActuatorSpeed[i];
	//	if (channelType[i] == 'l')
	//	{
	//		
	//		//if ((tempTargetVal >= min[i] && tempTargetVal <= max[i]) && (tempTargetVal != lastVal[i] || tempLASpeed != lastSpeed[i])) {
	//		//	channel[i]->p(tempTargetVal, tempLASpeed);
	//		//	lastVal[i] = tempTargetVal;
	//		//	lastSpeed[i] = tempLASpeed;
	//		//}

	//		//status[i] = channel[i]->getP();
	//		//if (status[i].done()) {
	//		//	channel[i]->powerDown();
	//		//}
	//	}
	//	else if (channelType[i] == 'm') {

	//		//if (tempTargetVal != lastVal[i]) {
	//		//	channel[i]->s(tempTargetVal);
	//		//	delay(10);
	//		//	lastVal[i] = tempTargetVal;
	//		//}

	//		//status[i] = channel[i]->getS();
	//	}

	//}

}

void RMCKangaroo1::begin() {
	SerialPort->begin(9600);
	SerialPort->listen();
	
	for(int i=0; i< channelList.length(); i++)
		channel[i]->begin();

	for (int i = 0; i < channelList.length(); i++) {
		if (channelType[i] == 'l') {
		}
		else if (channelType[i] == 'm') {
			/*long absMin = channel[i]->getMin().value();
			long absMax = channel[i]->getMax().value();
			long safeBound = (absMax - absMin)*0.02;
			min[i] = (absMin + safeBound);
			max[i] = absMax - safeBound;
			maxSpeed[i] = 0.1 * (absMax - absMin);*/
			//setSpeed((int)(channelList[i] - 48), 50);
		}
	}
}

void RMCKangaroo1::setTargetVal(int channelName, long val) { //val = 0% to 100%
	//int index = getChannelIndex(channelName);
	
	//channel[0]->setTargetVal(val);
	//channel[1]->setTargetVal(val);
	//channel[index]->setTargetVal(val);

	//if (val >= 0 && val <= 100) {
	//	targetVal1 = map(val, 0, 100, channel[0]->min, channel[0]->max);
	//}
	channel[0]->setTargetPos(val);
}

LinearActuator::LinearActuator(KangarooSerial& K, char name):KangarooChannel(K, name)
{
}
void LinearActuator::begin() {

	start();
	getExtremes();
}
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
		//Serial.println("Clive is power down");
		powerDown();
		done = true;
	}
}
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
void LinearActuator::setTargetPosDirect(long pos)
{
	if (targetVal >= min && targetVal <= max) {
		targetVal = pos;
	}
}
void LinearActuator::setTargetVal(long pos, long newSpeed) { //val = 0% to 100%
	setTargetPos(pos);
	setSpeed(newSpeed);
}
void LinearActuator::setTargetPos(long pos) { //val = 0% to 100%
	if (pos >= 0 && pos <= 100) {
		targetVal = map(pos, 0, 100, min, max);
	}
}
void LinearActuator::setSpeed(long newSpeed) { //val = 0% to 100%
	if (newSpeed >= 0 && newSpeed <= 100) {
		speed = map(newSpeed, 0, 100, 0, maxSpeed);
	}
}
long LinearActuator::getCurrentVal()
{
	return status.value();
}


LinearActuatorPair::LinearActuatorPair(KangarooSerial & K, char name)
{
	syncPID = new PID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
	Setpoint = 0;
	syncPID->SetMode(AUTOMATIC);
	syncPID->SetOutputLimits(-5, 5);
	channel[0] = new LinearActuator(K, name);
	channel[1] = new LinearActuator(K, name+1);
}
long * LinearActuatorPair::getCurrentVal()
{
	return nullptr;
}
void LinearActuatorPair::setTargetVal(long pos, long newSpeed)
{
	Serial.println("LAPair setTargetVal is empty.");

}
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
void LinearActuatorPair::setTargetPos(long pos)
{
	targetVal = pos;
}
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
		Input = -(la1 - la2);
		long gap = Input;
		syncPID->Compute();
		Serial.println(String(gap) + "     " + String(Output));
		long scaledLa1 = map(la1, channel[0]->min, channel[0]->max, 0, 100);
		if ((tempTargetVal - scaledLa1) > 1)
		{
			channel[1]->setSpeed(speed + Output);
		}
		else if ((tempTargetVal - scaledLa1) < -1)
		{
			channel[1]->setSpeed(speed - Output);
		}

		//Serial.println(gap);
		if (abs(gap) > 40)
		{
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
	

void LinearActuatorPair::begin()
{
	
	channel[0]->begin();
	channel[1]->begin();
	setSpeed(94);
}