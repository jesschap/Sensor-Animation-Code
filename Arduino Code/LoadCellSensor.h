#ifndef CLREAD_H
#define CLREAD_H

#include "Arduino.h"

class LoadCellSensor {
	
public:

	LoadCellSensor(int inputPin);

	void begin();
	void zero();
	void setSaturatedVal(int saturatedVolt);
	void setMinimumVal(int minimumVolt);
	void setFactors();
	void clearError();

	float read();


	int rawRead();
	int getZeroValue();
	int getFactor1();
	int getFactor2();
	int getSaturatedValue();
	int getMinimumValue();

	bool withinSatRange();
	bool isZeroed();
	bool isAttached();
	bool isFaulty();

private:

	void _inputVerification();
	int _read();

	int _inputPin;
	int _uncheckedRead = 0;
	int _saturatedValue = 700;
	int _minimumValue = 10;
	int _rawWeight1 = 0;
	int _rawWeight2 = 0;

	float _zeroValue = 0;

	bool _isInRange = false;
	bool _isSaturated = false;
	bool _isCallibrated = false;
	bool _isAttached = false;
	bool _isZeroed = false;
	bool _isFaulty = false;

};

#endif