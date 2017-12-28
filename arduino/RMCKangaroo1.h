#pragma once
#include <SoftwareSerial.h>
#include <Kangaroo.h>

class RMCKangaroo1
{
protected:
	
public:
	KangarooChannel *channel1;
	KangarooChannel *channel2;
	long targetVal1 = 500;
	long targetVal2 = 500;
	long lastVal1;
	long lastVal2;
	long max1;
	long min1;
	long max2;
	long min2;
	int speed1;
	int speed2;
	KangarooStatus *status1;
	KangarooStatus *status2;
	RMCKangaroo1(int txPin, int rxPin);
	void loop();
};

