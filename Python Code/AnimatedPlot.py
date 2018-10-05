import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
import math
import time
import numpy as np
import RingBuffer as rb
import datetime

from Definitions import *


class AnimatedPlot:
    def __init__(self):
        self.fig = plt.figure(num = None, figsize = (18, 9), dpi = 60)
        self.gs = gridspec.GridSpec(3, 3) 
        self.ax1 = plt.subplot(self.gs[:,:])
        self.canvas1 = self.ax1.figure.canvas
        self.ax1.grid(True)

        self.ax1_title = "Plot of Syringe Force vs Time of 10mL Syringe"
        self.ax1_xlabel = "Time (s)"
        self.ax1_ylabel = "Force (Kgf)"

        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=0.35)

        # based on behaviour of graph to plot points in the middle
        self.Xlow = 5
        self.Xhigh = 40
        self.deltaTime = 0.0

        self.p1_xlim = [self.Xlow, self.Xhigh]
        self.p1_ylim = [0, 1023]

        self.plottingData = None

        self.sensors = 0
        self.colours = ['C0.', 'C1.', 'C2.', 'C3.', 'C4.', 'C5.', 'C6.', 'C7.']

        self.dataBufferList     = None
        self.plotList           = []

    def getFigure(self):
        return self.fig

    def setSensors(self, sensors):
        self.sensors = sensors

    # a map holding the keys "time", "sensordata", "calcVel", "pumpVel", "pin1", "pin2"
    def setplottingData(self, plottingData):
        self.plottingData = plottingData
        self.dataKeys = self.plottingData.keys()

    def setXLim(self):
        self.p1_xlim = [self.Xlow, self.Xhigh]

    def initPlot(self):

        # Set sensor graph
        self.ax1.set_ylim(self.p1_ylim)

        self.ax1.set_title(self.ax1_title )
        self.ax1.set_xlabel(self.ax1_xlabel)
        self.ax1.set_ylabel(self.ax1_ylabel)

        dataList = []
        timeVal = []

        for num in range(0, self.sensors):
            self.plotList.append(self.ax1.plot(timeVal, dataList, self.colours[num], markersize=14, label="Force Sensor A" + str(num))[0])

        if (self.sensors > 1):
            handles, labels = self.ax1.get_legend_handles_labels()
            self.ax1.legend(handles, labels, loc='upper right')
        # Set top title
        self.fig.suptitle('Benchtop Syringe Lifetime Test', fontsize=14, fontweight='bold')

        # Save the background
        self.background1 = self.fig.canvas.copy_from_bbox(self.ax1.bbox)

        self.ax1.set_xlim(self.p1_xlim)
        self.ax1.grid(which='major', axis='both', linestyle='-')

    def updatePlot(self, iterNum):

        self.canvas1.restore_region(self.background1)

        for key in self.dataKeys:
            if key == TIMEKEY:
                # get the time buffer and get the updated value
                timeVal = self.plottingData[key].get()
                timeRecent = self.plottingData[key]

                # shift over x-axis when points get to close to sides (ie within 1 second of the max1)
                if(timeRecent.getVal() > self.Xhigh - 1.0):
                    self.deltaTime = timeRecent.getVal() - timeRecent.getPrev()
                    self.Xlow = self.Xlow + 1.0
                    self.Xhigh = self.Xhigh + 1.0
                    self.setXLim()

                    if ( timeRecent.getLast() != 0 and ((timeRecent.getVal() > self.Xhigh) or (timeRecent.getLast() < self.Xlow)) ):
                        self.Xlow = timeRecent.getLast() - 1.0
                        self.Xhigh = timeRecent.getVal() + 1.0
                        self.setXLim()


                self.ax1.set_xlim(self.p1_xlim)

            if key == SENSORKEY:
                self.dataBufferList = self.plottingData[key]

        for num in range(0, self.sensors):
            self.plotList[num].set_ydata(self.dataBufferList[num].get())
            self.plotList[num].set_xdata(timeVal)
            self.ax1.draw_artist(self.plotList[num])

        self.ax1.set_xlim(self.p1_xlim)
        self.ax1.grid(which='major', axis='both', linestyle='-')

        self.canvas1.draw()
        self.canvas1.blit(self.ax1.bbox)


# import matplotlib
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import gridspec
# import math
# import time
# import numpy as np
# import RingBuffer as rb
# import datetime

# from Definitions import *


# class AnimatedPlot:
#     def __init__(self):
#         self.fig = plt.figure(num = None, figsize = (20, 10), dpi = 80)
#         self.gs = gridspec.GridSpec(3, 3) 
#         self.ax1 = plt.subplot(self.gs[0,0:2])
#         self.axb = plt.subplot(self.gs[0,2])
#         self.canvas1 = self.ax1.figure.canvas
#         self.canvasb = self.axb.figure.canvas
#         self.ax1.grid(True)

#         self.ax1_title = "Plot of Syringe Force vs Time of 10mL Syringe"
#         self.ax1_xlabel = "Time (s)"
#         self.ax1_ylabel = "Force (Kgf)"

#         self.axb_title = "Plot of Maximums"
#         self.axb_xlabel = "Time (min)"
#         self.axb_ylabel = "Force (Kgf)"

#         self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
#                 wspace=None, hspace=0.35)

#         # based on behaviour of graph to plot points in the middle
#         self.Xlow = 5
#         self.Xhigh = 65.0
#         self.deltaTime = 0.0

#         # Plot the minutes instead of seconds
#         self.bLow = 0 / 60
#         self.bHigh = 4320 / 60

#         self.p1_xlim = [self.Xlow, self.Xhigh]
#         self.pb_xlim = [self.bLow, self.bHigh]
#         self.p1_ylim = [0, 15]
#         self.pb_ylim = [5, 20]

#         self.plottingData = None

#         self.sensors = 0
#         self.colours = ['C0.', 'C1.', 'C2.', 'C3.', 'C4.', 'C5.', 'C6.', 'C7.']

#         self.dataBufferList     = None
#         self.maxBufferList      = None
#         self.plotList           = []
#         self.peakList           = []

#     def getFigure(self):
#         return self.fig

#     def setSensors(self, sensors):
#         self.sensors = sensors

#     # a map holding the keys "time", "sensordata", "calcVel", "pumpVel", "pin1", "pin2"
#     def setplottingData(self, plottingData):
#         self.plottingData = plottingData
#         self.dataKeys = self.plottingData.keys()

#     def setXLim(self):
#         self.p1_xlim = [self.Xlow, self.Xhigh]

#     def initPlot(self):

#         # Set sensor graph
#         self.ax1.set_ylim(self.p1_ylim)

#         self.ax1.set_title(self.ax1_title )
#         self.ax1.set_xlabel(self.ax1_xlabel)
#         self.ax1.set_ylabel(self.ax1_ylabel)

#         # Set max points of sensor graph
#         self.axb.set_ylim(self.pb_ylim)

#         self.axb.set_title(self.axb_title)
#         self.axb.set_xlabel(self.axb_xlabel)
#         self.axb.set_ylabel(self.axb_ylabel)

#         dataList = []
#         timeVal = []

#         for num in range(0, self.sensor):
#             self.plotList.append(self.ax1.plot(timeVal, dataList, self.colours[0], markersize=4, label="Force Sensor"))
        
#         self.p0b, = self.peakList.append(self.axb.plot(timeVal, dataList, self.colours[5], markersize=4, label="Force Max"))

#         # Set top title
#         self.fig.suptitle('Benchtop Syringe Lifetime Test', fontsize=14, fontweight='bold')

#         # Save the background
#         self.background1 = self.fig.canvas.copy_from_bbox(self.ax1.bbox)
#         self.backgroundb = self.fig.canvas.copy_from_bbox(self.axb.bbox)

#         self.ax1.set_xlim(self.p1_xlim)
#         self.axb.set_xlim(self.pb_xlim)

#         self.ax1.grid(which='major', axis='both', linestyle='-')
#         self.axb.grid(which='major', axis='both', linestyle='-')

#     def updatePlot(self, iterNum):

#         self.canvas1.restore_region(self.background1)
#         self.canvasb.restore_region(self.backgroundb)

#         for key in self.dataKeys:
#             if key == TIMEKEY:
#                 # get the time buffer and get the updated value
#                 timeVal = self.plottingData[key].get()
#                 timeRecent = self.plottingData[key]

#                 # shift over x-axis when points get to close to sides (ie within 1 second of the max1)
#                 if(timeRecent.getVal() > self.Xhigh - 1.0):
#                     self.deltaTime = timeRecent.getVal() - timeRecent.getPrev()
#                     self.Xlow = self.Xlow + 1.0
#                     self.Xhigh = self.Xhigh + 1.0
#                     self.setXLim()

#                     if ( timeRecent.getLast() != 0 and ((timeRecent.getVal() > self.Xhigh) or (timeRecent.getLast() < self.Xlow)) ):
#                         self.Xlow = timeRecent.getLast() - 1.0
#                         self.Xhigh = timeRecent.getVal() + 1.0
#                         self.setXLim()


#                 self.ax1.set_xlim(self.p1_xlim)

#                 # check if the x-axis for homing peaks also needs to shift
#                 if ( (timeRecent.getVal() / 60) > (self.bHigh - 2) ):
#                     self.bHigh += (4320 / 60) / 2
#                     self.bLow += (4320 / 60) / 2

#                     self.pb_xlim = [self.bLow, self.bHigh]
#                     self.axb.set_xlim(self.pb_xlim)

#             if key == SENSORKEY:
#                 self.dataBufferList = self.plottingData[key]
#             if key == MAXKEY:
#                 self.maxBufferList = self.plottingData[key]

#         for num in range(0, self.sensors):
#             (self.plotList[num]).set_ydata(self.dataBufferList[0].get())
#             (self.plotList[num]).set_xdata(timeVal)

#         self.p0b.set_ydata(self.maxBufferList[0].get())
#         self.p0b.set_xdata(self.maxBufferList[1].get())

#         self.ax1.draw_artist(self.p01)
#         self.axb.draw_artist(self.p0b)

#         self.ax1.set_xlim(self.p1_xlim)
#         self.axb.set_xlim(self.pb_xlim)

#         self.ax1.grid(which='major', axis='both', linestyle='-')
#         self.axb.grid(which='major', axis='both', linestyle='-')

#         self.canvas1.draw()
#         self.canvasb.draw()
        
#         self.canvas1.blit(self.ax1.bbox)
#         self.canvasb.blit(self.axb.bbox)
