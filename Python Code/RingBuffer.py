import numpy as np


class RingBuffer():
    # "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.zeros(length, dtype='f')
        self.index = 0

    def extend(self, x):
        # "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self):
        # "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) % self.data.size
        return self.data[idx]

    # gives the most recent value in the buffer
    def getVal(self):
        orderedBuffer = self.get()
        return orderedBuffer[len(orderedBuffer)-1]

    # gives the second most recent value in the buffer
    def getPrev(self):
        orderedBuffer = self.get()
        return orderedBuffer[len(orderedBuffer)-2]

    def getLast(self):
        orderedBuffer = self.get()
        return orderedBuffer[0]

    def put(self,x):
        #add a single number to ring buffer
        x_index = (self.index) % self.data.size
        self.data[x_index] = x
        self.index = x_index + 1



if __name__ == '__main__':
    
    ringlen = 10
    ringbuff = RingBuffer(ringlen)
    print("Extend:")
    for i in range(10):
        ringbuff.extend(np.arange(i+1, dtype='f')) # write
        print(ringbuff.get()) #read

    print("PUT:")
    ringbuff = RingBuffer(ringlen)
    for i in range(40):
        ringbuff.put(i)
        print(ringbuff.get())