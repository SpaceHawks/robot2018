// I2C.h

#ifndef _I2C_h
#define _I2C_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
	#include <Wire.h>

#else
	#include "WProgram.h"
#endif

class I2CClass
{
 protected:


 public:
	typedef void(*voidFuncPtr)(void); //needed for interuptAttach
	typedef void(*voidFuncPtrInt)(int); //needed for interuptAttach

	I2CClass(int address);
	I2CClass();
	void init();
	void attach(voidFuncPtrInt receiveDataFunction, voidFuncPtr sendData);
	void receiveData(int byteCount);
	void sendData();
	int leftTargetSpeed;
	int rightTargetSpeed;
	int _address;
};

extern I2CClass I2C;

#endif