// RMCKangaroo.h

#ifndef _RMCKANGAROO_h
#define _RMCKANGAROO_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "Arduino.h"
#else
	#include "WProgram.h"
#endif

#include <SoftwareSerial.h>
#include <Kangaroo.h>

class RMCKangaroo
{
 protected:
	 KangarooChannel K1;
	 KangarooChannel K2;
	 KangarooStatus currentVal1;
	 KangarooStatus currentVal2;
	 long targetVal1;
	 long targetVal2;
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

 public:
	void init();
	RMCKangaroo(txPin, rxPin);
	void loop();
};
#endif

