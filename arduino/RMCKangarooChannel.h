// RMCKangarooChannel.h
#include <SoftwareSerial.h>
#include <Kangaroo.h>
#define DEFAULT_NUMBER_OF_CHANNEL 10
#ifndef _RMCKANGAROOCHANNEL_h
#define _RMCKANGAROOCHANNEL_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "Arduino.h"
#else
	#include "WProgram.h"
#endif


#endif

class LinearActuator : public KangarooChannel
{
public:
	LinearActuator(KangarooSerial& K, char channelName);
	long max;
	long min;
	KangarooStatus status;
	void setTargetVal(long val);
	long getCurrentVal();
	void begin();
	long targetPos;
	long lastTargetPos;
	long lastSpeed;
	long speed;
	long maxSpeed;
	void loop();
	void setSpeed(long newSpeed);
	void setMaxSpeed(long speed);
};
//
//class LinearActuatorPair
//{
//public:
//	LinearActuatorPair(KangarooSerial &K, char firstChannelName);
//	LinearActuator* linearActuators[2];
//	void begin();
//	long targetPos;
//	long lastTargetPos;
//	long speed;
//	void setTargetPos(long pos);
//	void loop();
//	void setMotorMaxSpeed(long speed);
//}

class Actuator {
protected:
	int channelIndex[DEFAULT_NUMBER_OF_CHANNEL];
	LinearActuator* actuators;
	SoftwareSerial* SerialPort;
	KangarooSerial* K;
	String channelList;
	String channelType;

public:
	
	Actuator(int rxPin, int txPin, String channelList, String channelType);
	void loop();
	void begin();
	long getCurrentVal(int channel);
	void setTargetVal(int channel, long val);
	int getChannelIndex(int channel);

};
