#pragma once
#include <SoftwareSerial.h>
#include <Kangaroo.h>

#include <PID_v1.h>
#define DEFAULT_NUMBER_OF_CHANNEL 10
class Actuator
{
public:
	void begin();
	void loop();
	void setTargetVal(long val);
	void setTargetVal(long val1, long val2); // only for motor
	long *getCurrentVal();
private:

};

class LinearActuator : public KangarooChannel, public Actuator {
public:
	LinearActuator(KangarooSerial& K, char name);
	long min;
	long max;
	long maxSpeed;
	long speed;
	long lastSpeed;
	long targetVal;
	long lastVal;
	long getCurrentVal();
	bool done = false;
//	void setSpeed(long speed);
	void getExtremes();
	void setTargetPosDirect(long pos);
	void setTargetVal(long pos, long newSpeed);
	void setSpeed(long newSpeed);
	void setTargetPos(long pos );
	void loop();
	KangarooStatus status;
	void begin();
};

class LinearActuatorPair{
public:
	LinearActuatorPair(KangarooSerial& K, char name);
	LinearActuator* channel[2];
	long targetVal;
	long lastVal;
	long lastSpeed;
	bool isSyncing;
	long *getCurrentVal();
	void setTargetVal(long pos, long newSpeed);
	void setSpeed(long newSpeed);
	void setTargetPos(long pos);
	void loop();
	void begin();
	long speed;
	//Define Variables we'll be connecting to
	double Setpoint, Input, Output;

	//Specify the links and initial tuning parameters
	double Kp = 0.4, Ki = 0, Kd = 0;
	PID* syncPID;

};

class RMCKangaroo1
{
protected:
	int channelIndex[DEFAULT_NUMBER_OF_CHANNEL];
	LinearActuatorPair* channel[DEFAULT_NUMBER_OF_CHANNEL];
	SoftwareSerial* SerialPort;
	KangarooSerial* K;
	String channelList;
	String channelType;

public:

	RMCKangaroo1(int rxPin, int txPin, String channelList, String channelType);
	void loop();
	void begin();
	void setTargetVal(int channelName, long val);
	KangarooStatus status[DEFAULT_NUMBER_OF_CHANNEL];
	
};
