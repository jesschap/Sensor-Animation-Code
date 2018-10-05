commands = {                                    \
            "REQUEST_READ":"10",                \
            "REQUEST_RAW_READ":"11",            \
            "REQUEST_FAULT_STATUS":"12",        \
            "GET_ADCBITS":"20",                 \
            "GET_ADCREFVOLT":"21",              \
            "GET_N_SENSORS":"22",               \
            "GET_RAW_FACTORS":"23",             \
            "GET_ZERO":"24",                    \
            "SET_FACTOR1":"30",                 \
            "SET_FACTOR2":"31",                 \
            "SET_STREAMING_INTERVAL":"32",      \
            "ZERO":"40",                        \
            "CLEAR_ERROR":"41",                 \
            "STREAMING_ON":"42",                \
            "STREAMING_OFF":"43",               \
            "PCPING":"49"                       \
            }

responses = {                                   \
            'e': "ERROR",                       \
            'r':"READ",                         \
            'R':"RAW_READ",                     \
            'f':"FAULT",                        \
            'z':"ZERO",                         \
            'a':"ADCBITS",                      \
            'v':"ADCREFVOLT",                   \
            'n':"N_SENSORS",                    \
            'p':"PONG",                         \
            'S':"STATUS",                       \
            'w':"RAW_WEIGHT_FACTORS"            \
            }

DEBUG             = False
SENSORCONNECTED   = False
MANUAL            = False

ALPHA             = 0.0221
BETA              = -6.552

RINGBUFFERSIZE    = 250
SENSORMAXLB       = 50
SENSORMAXVOLTAGE  = 5
SENSORMINVOLTAGE  = 0

TIMEKEY           = "time"
SENSORKEY         = "sensor"