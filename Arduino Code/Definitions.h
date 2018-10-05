#define SENSOR1PIN A0
#define SENSOR2PIN A1
#define SENSOR3PIN A2
#define SENSOR4PIN A3
#define SENSOR5PIN A4
#define SENSOR6PIN A5

#define MANUALCONFIGURE = true

enum : uint8_t
{
    // 1-9 reserved for variables
    ack = 1,
    err = 2,
    // 10-19 reserved for requesting values/proccesses
    REQUEST_READ = 10,
    REQUEST_RAW_READ = 11,
    REQUEST_FAULT_STATUS = 12,
    // 20-29 reserved for getting values
    GET_ADCBITS = 20,
    GET_ADCREFVOLT = 21,
    GET_N_SENSORS = 22,
    GET_RAW_FACTORS = 23,
    GET_ZERO = 24,
    // 30-39 reserved for setting values
    SET_FACTOR1 = 30,
    SET_FACTOR2 = 31,
    SET_STREAMING_INTERVAL = 32,
    // 40-49 is reserved for additional commands
    ZERO = 40,
    CLEAR_ERROR = 41,
    STREAMING_ON = 42,
    STREAMING_OFF = 43,
    PCPING = 49,
};
