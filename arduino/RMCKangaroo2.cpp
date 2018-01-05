#include "RMCKangaroo2.h"

long RMCKangaroo1::getMin(int channelName)
{

	return min[getChannelIndex(channelName)];
}

long RMCKangaroo1::getMax(int channelName)
{
	return max[getChannelIndex(channelName)];
}

RMCKangaroo1::RMCKangaroo1(int rxPin, int txPin, String channelList, String channelType)
{
	this->channelList = channelList;
	this->channelType = channelType;
	SerialPort = new SoftwareSerial(rxPin, txPin);
	K = new KangarooSerial(*SerialPort);
	
	for (int i = 0; i < channelList.length(); i++) {
		channel[i] = new LinearActuator(*K, channelList[i], targetVal1);
		channelIndex[(int)(channelList[i]-49)] = i; //if channel is 1, index is 0
	}
}

void RMCKangaroo1::loop()
{
	for (int i = 0; i < 1; i++) {
		int tempTargetVal = targetVal[i];
		int tempLASpeed = linearActuatorSpeed[i];
		if (channelType[i] == 'l')
		{
			long tempTargetVal = targetVal1;
			channel[0]->loop(tempTargetVal);
			channel[1]->loop(tempTargetVal);
			delay(100);
			//if ((tempTargetVal >= min[i] && tempTargetVal <= max[i]) && (tempTargetVal != lastVal[i] || tempLASpeed != lastSpeed[i])) {
			//	channel[i]->p(tempTargetVal, tempLASpeed);
			//	lastVal[i] = tempTargetVal;
			//	lastSpeed[i] = tempLASpeed;
			//}

			//status[i] = channel[i]->getP();
			//if (status[i].done()) {
			//	channel[i]->powerDown();
			//}
		}
		else if (channelType[i] == 'm') {

			if (tempTargetVal != lastVal[i]) {
				channel[i]->s(tempTargetVal);
				delay(10);
				lastVal[i] = tempTargetVal;
			}

			status[i] = channel[i]->getS();
		}

	}

}

void RMCKangaroo1::begin() {
	SerialPort->begin(9600);
	SerialPort->listen();
	
	for(int i=0; i< channelList.length(); i++)
		channel[i]->start();

	for (int i = 0; i < channelList.length(); i++) {
		if (channelType[i] == 'l') {
			channel[i]->getExtremes();
			//long absMin = channel[i]->getMin().value();
			//long absMax = channel[i]->getMax().value();
			//long safeBound = (absMax - absMin)*0.02;
			//min[i] = (absMin + safeBound);
			//max[i] = absMax - safeBound;
			//maxSpeed[i] = 0.1 * (absMax - absMin);
			//setSpeed((int)(channelList[i] -48), 50);
		}
		else if (channelType[i] == 'm') {
			long absMin = channel[i]->getMin().value();
			long absMax = channel[i]->getMax().value();
			long safeBound = (absMax - absMin)*0.02;
			min[i] = (absMin + safeBound);
			max[i] = absMax - safeBound;
			maxSpeed[i] = 0.1 * (absMax - absMin);
			setSpeed((int)(channelList[i] - 48), 50);
		}
	}
}

void RMCKangaroo1::setTargetPos(int channelName, long val) { //val = 0% to 100%
	//int index = getChannelIndex(channelName);
	
	//channel[0]->setTargetVal(val);
	//channel[1]->setTargetVal(val);
	//channel[index]->setTargetVal(val);
	if (val >= 0 && val <= 100) {
		targetVal1 = map(val, 0, 100, channel[0]->min, channel[0]->max);

	}
}

void RMCKangaroo1::setTargetSpeed(int channelName, long val) { //val = -100% to 100%
	int index = getChannelIndex(channelName);
	
	targetVal[index] = map(val, -100, 100, min[index], max[index]);

}

void RMCKangaroo1::setSpeed(int channelName, long speed) //speed:0-100%
{
	int index = getChannelIndex(channelName);
	if (speed >= 0 && speed <= maxSpeed[index]) {
		lastSpeed[index] = speed;
		linearActuatorSpeed[index] = map(speed, 0, 100, 1, maxSpeed[index]);
	}
}

void RMCKangaroo1::setMotorMaxSpeed(int channelName, long speed)
{
	int index = getChannelIndex(channelName);
	if (speed > 0)
	{
		min[index] = -speed;
		max[index] = speed;
		
	}
}

long RMCKangaroo1::getCurrentVal(int channelName)
{
	int index = getChannelIndex(channelName);
	return status[index].value();
}

int RMCKangaroo1::getChannelIndex(int channelName) {
	
	return channelIndex[channelName-1];
}

LinearActuator::LinearActuator(KangarooSerial& K, char name, long& targetVal):KangarooChannel(K, name)
{
	this->targetVal = &targetVal;
}

void LinearActuator::getExtremes()
{
		long absMin = getMin().value();
		long absMax = getMax().value();
		long safeBound = (absMax - absMin)*0.02;
		min = (absMin + safeBound);
		max = absMax - safeBound;
		maxSpeed = 0.1 * (absMax - absMin);
		setSpeed(50);
}
void LinearActuator::setSpeed(long newSpeed) //newSpeed:0-100%
{
	if (newSpeed >= 0 && speed <= maxSpeed) {
		lastSpeed = newSpeed;
		speed = map(newSpeed, 0, 100, 1, maxSpeed);
	}
}
void LinearActuator::setTargetVal(long val) { //val = 0% to 100%
	if (val >= 0 && val <= 100) {
		*targetVal = map(val, 0, 100, min, max);
	}
}
void LinearActuator::loop(long val)
{
	long tempSpeed = speed;
	if ((val >= min && val <= max) && (val != lastVal || tempSpeed != lastSpeed)) {
		p(val, tempSpeed);
		lastVal = val;
		lastSpeed = tempSpeed;
	}

	status = getP();
	if (status.done()) {
		powerDown();
	}
}
long LinearActuator::getCurrentVal()
{
	return status.value();
}