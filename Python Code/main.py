import serial
import serial.tools.list_ports
from serial.serialutil import SerialException
import time
import datetime
import sys

from multiprocessing import Process, Queue

import matplotlib.pyplot as plt
import csv
import matplotlib.animation as animation

import numpy as np

import os
import RingBuffer as rb
import AnimatedPlot

from Definitions import *


# =============== Definitions ===============

if __name__ == '__main__':

    # create queues to hold the data points x = time, y = data, file holds strings
    # to write into csv
    timeQueue = Queue(maxsize = 500)    # queue holding the time data was taken
    dataQueue = Queue(maxsize = 500)    # queue holding data buffer representing each sensor
    fileQueue = Queue(maxsize = 500)    # queue holding strings to write to file

    # initialize our animated figure object
    liveFig = AnimatedPlot.AnimatedPlot()
    fig = liveFig.getFigure()



# =============== Functions ===============


## ======================================================================
# The function writes to the port the passed in message and reads the response
# from the port on the serial monitor.
## ======================================================================
def portWriteAndRead(message, openedPort):
    openedPort.reset_input_buffer()
    openedPort.write((message).encode())
    openedPort.flush()

    return parseResponse(openedPort.readline())


## ======================================================================
# From a given serial repsone, function returns if it is a valid command
# the response type, and the arguments for each sensor. The response type
# is given by the first letter of the serial repsonse, the arguments
# are the proceeding words after each comma.
# Returns:  isValid:    Whether the given serialResponse is a valid input
#           respType:   A single letter representing the response from the
#                       arduino to the computer
#           respData:   An array storing the response for each sensor
#                       in each entry of the array.
## ======================================================================
def parseResponse(serialResponse):
    serialResponse = serialResponse.decode()
    isValid= False
    respType = None
    respData = None

    if (serialResponse != None) and (len(serialResponse)) > 0:

        strResponse = str(serialResponse)
        if (strResponse[0] in responses) and (';' in strResponse):
            isValid = True

            # creating an array with each entry holding one sensor data value
            response = strResponse.replace(';\r\n','').split(',')
            respType = responses[response[0]]
            respData = response[1:]
            if len(respData) == 1:
                respData = respData[0]

        else:
            pass

    else:
        pass

    return isValid, respType, respData


## ======================================================================
# The function finds a list of devices with the name of the usbmodel in
# its name.
# Returns:  ports:  A list of available usbmodem ports
## ======================================================================
def findSerialDevices():

    # find COM port for arduino
    ports = list(serial.tools.list_ports.comports())

    if ((len(ports) > 0) and (ports != None)):
        print("Found the following arduinos:")

        for port in ports:
            print(port[0])

        print("Connecting...")

    else:
        print("Arduino not found")
        print("Check Arduino connection and whether drivers are installed")

    return ports


## ======================================================================
# The function checks the different serial ports to see which one is
# connected by sending in a ping command and getting a response
# Returns:  returnport: Returns the single port that is connected
## ======================================================================
def sensorHandshake(serialPorts):

    foundSuitableDevice = False
    returnPort = None

    for port in serialPorts:

        try:
            openedPort = serial.Serial(port[0], baudrate=57600, timeout = 0.1)
            if DEBUG: print("attempting to open serial port")
            time.sleep(3)
        except:
            if DEBUG: print("gone to exception")
            continue

        # writes PING to the port, looking for PONG response
        isValid, respType, respData = portWriteAndRead(commands["PCPING"]+";", openedPort)
        openedPort.close()

        if DEBUG:
            print(openedPort)
            print(isValid)
            print(respType)
            print(respData)

        if (respData == "PONG"):
            foundSuitableDevice = True
            print("Connected at: " + port[0])
            returnPort = port
            time.sleep(1)
            break

    return returnPort


## ======================================================================
# The function calibrates the sensor with two initial weights by taking the user
# input of the already known weights and determining the alpha and beta factors.
# Returns the raw zero value parsed from the arduino for the intial reading with 
# no weights on the sensor.
# Returns:  zeros: a list of floats holding the raw zero value for each sensor
#           alpha: a list of floats holding the alpha factor for each sensor
#           beta:  a list of floats holding the beta factors for each sensor
## ======================================================================
def calibrateSensors(openedSensePort, nSensors):

    if MANUAL: 
        for i in range(1,20):
            transeiveCmd(openedSensePort,"ZERO")
            time.sleep(0.1)

        print("Zeroing...")
        time.sleep(1)
        inputZero = input("Please press enter to continue: ")

    for i in range(1,20):
        transeiveCmd(openedSensePort,"ZERO")
    time.sleep(0.1)
    transeiveCmd(openedSensePort,"ZERO")

    zeroVal_raw = transeiveCmd(openedSensePort,"GET_ZERO")[2]

        # zeroVal_raw gives both the time and zero value in a list with [['time', 'zeroVal']]
        # we will take only the zero value for each sensor and not the time
    zeros = []

    for i in range(0, nSensors):
        zeros.append(zeroVal_raw[i+1])

    if MANUAL:
        # Format : outputStr = "w,factor1-1,factor2-1,factor1-2,factor2-2,...,factor1-N,factor2-N;"
        # transeiveCmd(openedSensePort,"GET_RAW_FACTORS")[2] gives [factor1-1 factor2-1... factor1-N 
        # factor2-N] so we need to split these

        rawFactor1 = []
        rawFactor2 = []

        # set up the weight calibration of the first sensor.
        print("Please place the first weight on the sensor.")
        time.sleep(1)
        kgForce1 = input("Enter the exact given weight of the first object in Kgs: ")
        transeiveCmd(openedSensePort,"SET_FACTOR1")

        # set up the weight calibration of the second sensor.
        print("Please place the second weight on the sensor.")
        time.sleep(1)
        kgForce2 = input("Enter the exact given weight of the second object in Kgs: ")
        transeiveCmd(openedSensePort, "SET_FACTOR2")

        factors = transeiveCmd(openedSensePort,"GET_RAW_FACTORS")[2]
        print("Raw Factors: ", factors)

        for i in range(0, nSensors, 2):
            rawFactor1.append(factors[i])
            rawFactor2.append(factors[i+1])

            if(rawFactor1[i] == rawFactor2[i]):
                print("ERROR: Raw Factors did not properly calibrate or same weight was used. Exiting...")
                sys.exit();

        # Calculating alpha and beta factors for the formula [kg] = (alpha)*[V_read] + (beta)
        # This will give the voltage reading in terms of kg. Note that read here is not 
        # raw read (includes zero value subtracted from it)

        alpha = []
        beta = []

        for i in range(0, nSensors):
            alpha.append(( float(kgForce1) - float(kgForce2) ) / ( float(rawFactor1[i]) - float(rawFactor2[i]) ))
            beta.append(int(kgForce1) - ( alpha[i] * int(rawFactor1[i]) ))

            # checking if the factors are constant within a 5% error range
            if ( DEBUG and SENSORCONNECTED ):
                beta2 = ( float(kgForce2) - ( alpha[i] * float(rawFactor2[i]) ) ) 

                if ( (beta[i] > beta2 + 0.05*beta2) or (beta[i] < beta2 - 0.05*beta2) ):
                    print("ERROR: beta and alpha incorrect, mismatched within 5% error. Exiting...")
                    sys.exit();

        # convert lists from list of strings to list of integers
        zeros = [float(i) for i in zeros]
        alpha = [float(i) for i in alpha]
        beta = [float(i) for i in beta]

    else:
        zero = float(zeros[0])
        alpha = []
        beta = []
        for num in range(0, nSensors):
            alpha.append(ALPHA)
            beta.append(BETA)

    return zeros, alpha, beta


## ======================================================================
# The function constructs a command string to send to the arduino from the
# args parameter. 
# Returns:  portResponse:   Returns the response given by the Arduino
## ======================================================================
def transeiveCmd(port, commandType, *args):

    cmdString = ""
    for arg in args:
        cmdString += ","
        cmdString += arg

    return portWriteAndRead(commands[commandType] + cmdString + ";", port)


## ======================================================================
# The function updates the read, data, and file values for setting up the plot
# and txt file.
## ======================================================================
def readSensor(dataQueue, timeQueue, fileQueue, closedSensePort, nSensors):

    if DEBUG:
        print("worker thread reading sensor")
        print('parent process:', os.getppid())
        print('process id:', os.getpid())

    isOpen = False
    openedSensePort = None
    dataList = []

    while True:
        if not isOpen:
            isOpen = True
            openedSensePort = serial.Serial(closedSensePort, baudrate=57600, timeout = 0.1)
            time.sleep(3)

            # Callibrate Sensors, confirm no weight is placed on them
            zeros, alpha, beta = calibrateSensors(openedSensePort, nSensors)

            headStr = "#Pump Zero Value: " + str(zeros[0]) +"\n"
            headStr += "Time(s)"

            for num in range(0, nSensors):
                headStr += " - SensorA{:d}(Kgf) - Raw Val".format(num)

            fileQueue.put(headStr + "\n")

        else:
            sensorRead = transeiveCmd(openedSensePort, "REQUEST_RAW_READ")[2]

            # converting time to seconds
            # converting the raw voltage (zeroed) to kg
            timeVal = float(sensorRead[0])*(1/1000)
            fileStr = "%0.4f, " % (timeVal)
            timeQueue.put(timeVal)

            dataList[:] = []

            for num in range(0, nSensors):
                rawVal = float(sensorRead[num+1])
                dataVal = float(sensorRead[num+1])
                # dataVal = rawVal*alpha[num]+beta[num]
                if (dataVal < 0):
                    dataVal = 0
                fileStr += "%0.4f, %0.4f, " % (dataVal, rawVal)
                dataList.append(dataVal)
                
            dataQueue.put(dataList)
            fileQueue.put(fileStr + "\n")
            time.sleep(0.09)


## ======================================================================
# The function updates the plotting data dictionary. The function is made only
# to update a single sensor with the values stored in dataBuffer, additional
# data buffers would need to be passed to accomodate additional sensor data readings.
## ======================================================================
def fileAndUpdate(iterNum, dataBufferList, timeBuffer, liveFig, dataQueue, timeQueue, fileQueue, nSensors):

    while ( not dataQueue.empty() ):
        # remove from queue being updated by the worker threads
        data = dataQueue.get()
        time = timeQueue.get()

        timeBuffer.put(time)

        # dataQueue holds a list of the data for each sensor, so put each data point in the correct sensor buffer
        for num in range(0, nSensors):
            dataBufferList[num].put(data[num])

        # write in string created in sensorRead, holding the points in the form timeVal, dataVal, rawVal
        f.write(fileQueue.get())

    # add the updated buffer for the time values and sensor data
    for key in keys:
        # updates the times to be plotted held in time buffer
        if ( key == TIMEKEY ):
            liveFig.plottingData.update({key:timeBuffer})
        # updates the sensor data to be plotted held in databuffer
        if ( key == SENSORKEY ):
            liveFig.plottingData.update({key:dataBufferList[0:nSensors]})
             
    liveFig.updatePlot(iterNum)



# =============== Start of Code ===============


if __name__ == '__main__':

    if(DEBUG):
        print("Start")

    # find available devices, confirm that there is at least one
    availableDevices = findSerialDevices()
    if ( len(availableDevices) == 0 ):
        print("System exiting..")
        sys.exit()

    # find the sensor port is compatible, confirm that there is at least one
    sensorPort = sensorHandshake(availableDevices)
    if ( sensorPort is None ):
        print("None of the arduinos have a suitable protocol")
        print("Check firmware version")
        print("exiting...")
        sys.exit();

    # open the port for communication, wait 2 seconds for Arduino to initialize
    openedSensePort = serial.Serial(sensorPort[0], baudrate=57600, timeout = 0.1)
    time.sleep(2)

    # get hardware level information for each sensor (number of sensors, 
    # number of bits, ADC reference voltage)
    nSensors = int(transeiveCmd(openedSensePort,"GET_N_SENSORS")[2])
    nBits = int(transeiveCmd(openedSensePort,"GET_ADCBITS")[2])
    adcRef = float(transeiveCmd(openedSensePort,"GET_ADCREFVOLT")[2])

    # define our data buffer for sensor 1 and the time buffer to hold the times
    timeBuffer = rb.RingBuffer(RINGBUFFERSIZE)
    dataBufferList = []

    # ring buffers for sensor data points
    for num in range(0, nSensors):
        dataBufferList.append(rb.RingBuffer(RINGBUFFERSIZE))


    # =============== Begin Worker Thread for Sensor Data ===============


    # close the sensor port to ensure no crossover between threads
    openedSensePort.close()
    closedSensePort = sensorPort[0]

    worker = Process(target=readSensor, \
        args=(dataQueue, timeQueue, fileQueue, closedSensePort, nSensors, ))
    worker.daemon = True
    worker.start()

    # delay to allow thread to start filling up the queue and open port
    time.sleep(4)

    # Setting up the initial states for the plot figure
    # putting in the databuffer and timebuffer to initialize the plot
    plottingData = {}
    keys = []

    plottingData.update({TIMEKEY:timeBuffer})
    keys.append(TIMEKEY)
    plottingData.update({SENSORKEY:dataBufferList})
    keys.append(SENSORKEY)

    liveFig.setplottingData(plottingData)
    liveFig.setSensors(nSensors)


    # =============== Begin Inputting Data to File ===============


    # get time and date for naming file
    time_str = str(datetime.datetime.now())
    file_str = time_str.replace(":","-") + ".txt"

    # Set up the file information, writing in known constants
    with open(file_str,'w') as f:
        f.write("#File created on " + time_str +"\n")
        f.write("#File name: " + file_str +"\n")
        f.write("#Number of connected sensors: " + str(nSensors) +"\n")
        f.write("#Reported ADC Bits: " + str(nBits) +"\n")
        f.write("#Reported ADC Reference Voltage: " + str(adcRef) +"\n")
        f.write("#Inputted Sensor Max Voltage: " + str(SENSORMAXVOLTAGE) +"\n")
        f.write("#Inputted Sensor Min Voltage: " + str(SENSORMINVOLTAGE) +"\n")

        print("Collecting Data..")

        anim = animation.FuncAnimation(
            liveFig.fig, fileAndUpdate, init_func=liveFig.initPlot, frames = 500, \
            fargs = (dataBufferList, timeBuffer, liveFig, dataQueue, timeQueue, fileQueue, nSensors, ), interval=500)

        plt.show()
