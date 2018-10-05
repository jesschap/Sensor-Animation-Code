#include "LoadCellSensor.h"

LoadCellSensor :: LoadCellSensor(int inputPin) {
	_inputPin = inputPin;
}

// Sets the Arduino Pin to INPUT for reading
void LoadCellSensor :: begin() {
	pinMode(_inputPin, INPUT);
	_isAttached = true;
}

// Sets the reference value for reading
void LoadCellSensor :: zero(){
	_isZeroed = true;
	_zeroValue = _read();
}

void LoadCellSensor :: setSaturatedVal(int saturatedVolt) {
	_saturatedValue = saturatedVolt;
}

void LoadCellSensor :: setMinimumVal(int minimumVolt) {
	_minimumValue = minimumVolt;
}

void LoadCellSensor :: setFactors() {

	if ( _rawWeight1 != 0 ) {
		_rawWeight2 = read();
	}

	else {
		_rawWeight1 = read();
	}
}

void LoadCellSensor :: clearError() {
	_isAttached = true;
	_isSaturated = false;
	_isFaulty = false;
}

float LoadCellSensor :: read() {
	return _read() - _zeroValue;
}

int LoadCellSensor :: rawRead() {
	return _read();
}

int LoadCellSensor :: getZeroValue() {
	return _zeroValue;
}

int LoadCellSensor :: getFactor1() {
	return _rawWeight1;
}

int LoadCellSensor :: getFactor2() {
	return _rawWeight2;
}

int LoadCellSensor :: getSaturatedValue() {
	return _saturatedValue;
}

int LoadCellSensor :: getMinimumValue() {
	return _minimumValue;
}

bool LoadCellSensor :: withinSatRange() {
	if( !_isSaturated && _isAttached ) {
		_isInRange = true;
	}
	else {
		_isInRange = false;
	}
	return _isInRange;
}

bool LoadCellSensor :: isZeroed() {
	return _isZeroed;
}

bool LoadCellSensor :: isAttached() {
	return _isAttached;
}

bool LoadCellSensor :: isFaulty() {
	if ( !_isAttached || _isSaturated ) {
		_isFaulty = true;
	}
	else {
		_isFaulty = false;
	}
	return _isFaulty;
}

void LoadCellSensor :: _inputVerification() {
	if( _uncheckedRead <= _minimumValue ) {
		_isAttached = false;
	}

	if( _uncheckedRead >= _saturatedValue ) {
		_isSaturated = true;
	}
}

int LoadCellSensor :: _read() {
	_uncheckedRead = analogRead(_inputPin);
	_inputVerification();
	return _uncheckedRead;
}