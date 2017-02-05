import * from _DeviceClass

def class SensorClass(DeviceClass):
    """Class that implements any kind of sensor with a base class of Device. """

    def ValidateDevice(self):
        """method to make sure the sensor has all that is needed to operate.  Interface to hardware, logging, etc"""

    def ReadDevice(self, numberOfValues=1,Timeout=5000,bytesToRead=1):
        """method uses the configured interface to read a datapoint.  Returns a list of 1 or more values.

        Needs two parameters:  # of values to expect, timeout in milliseconds, # of bytes per read 
        """
        if not self.ValidateDevice():
            self.LogEntry({'header': 'Validation failed during '+self.__name__+'.ReadDevice'})
            return None
        else
            
        

