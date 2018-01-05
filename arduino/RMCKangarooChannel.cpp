
#include <Kangaroo.h>
#include "RMCKangarooChannel.h"

//
//LinearActuatorPair::LinearActuatorPair(KangarooSerial &K, char firstChannelName)
//{
//	linearActuators[0] = new LinearActuator(K, firstChannelName);
//	linearActuators[1] = new LinearActuator(K, firstChannelName + 1);
//}
//
//void LinearActuatorPair::begin()
//{
//	linearActuators[0]->begin();
//	linearActuators[1]->begin();
//}
//
//void LinearActuatorPair::setTargetPos(long pos)
//{
//	targetPos = pos;
//}
//
//void LinearActuatorPair::loop()
//{
//	long tempTargetPos = targetPos;
//	long tempSpeed = speed;
//	if (tempTargetPos != lastTargetPos)
//	{
//		linearActuators[0]->p(tempTargetPos, tempSpeed);
//		linearActuators[1]->p(tempTargetPos, tempSpeed);
//	}
//	
//	lastTargetPos = tempTargetPos
//}

LinearActuator::LinearActuator(KangarooSerial& K, char channelName): KangarooChannel(K, channelName)
{

}

void LinearActuator::setTargetVal(long val)
{
	if (val >= 0 && val <= 100) {
		targetPos = map(val, 0, 100, min, max);
	}
}

long LinearActuator::getCurrentVal()
{
	return status.value();
}

void LinearActuator::begin()
{
	start();
	Serial.println("after start");
//	min = getMin().value();
//	max = getMax().value();
}

void LinearActuator::loop()
{
	if (lastTargetPos != targetPos || lastSpeed != speed)
	{
		p(targetPos, speed);
		lastTargetPos = targetPos;
	}
	status = getP();
	if (status.done()) 
	{
		powerDown();
	}
}

void LinearActuator::setSpeed(long newSpeed)
{
	
		if (newSpeed >= 0) {
			lastSpeed = speed;
			speed = newSpeed;
			if (newSpeed > maxSpeed)
				speed = maxSpeed;
		}
}

void LinearActuator::setMaxSpeed(long speed)
{
	if (speed > 0)
		maxSpeed = speed;
}

Actuator::Actuator(int rxPin, int txPin, String channelList, String channelType)
{
	this->channelList = channelList;
	this->channelType = channelType;
	SerialPort = new SoftwareSerial(rxPin, txPin);
	K = new KangarooSerial(*SerialPort);

	//for (int i = 0; i < channelList.length(); i++) {
		//if (channelType[i] == 'l')
		//{
			actuators =  new LinearActuator(*K, channelList[]);
			//channelIndex[(int)(channelList[i] - 49)] = i; //if channel is 1, index is 0
		//}
	//}
}

int Actuator::getChannelIndex(int channel)
{
	return channelIndex[channel - 1];
}

void Actuator::loop()
{
	for (int i = 0; i < channelList.length(); i++) {

		actuators->loop();
	}
}

	void Actuator::begin()
	{
		//for (int i = 0; i < channelList.length(); i++) {
			actuators->begin();
		//}
	}

	long Actuator::getCurrentVal(int channel)
	{
		int i = getChannelIndex(channel);
		return actuators->getCurrentVal();
	}

	void Actuator::setTargetVal(int channel, long val)
	{

		int i = getChannelIndex(channel);
		actuators->setTargetVal(val);
	}

