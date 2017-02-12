from _DeviceClass import *
from _Globals import *
import time

def class Sensor(Device):
    """Class that implements any kind of sensor with a base class of Device. """

    def __init__(self,dbClient,Name,cycletime, mode='event'):
        """mode can be either polling or event driven.  If event driven, will only send data
            when the data being measured changes, up to the cycletime or to processor limits
            If using polling method, the cycletime will be used to take a sample cycletime/second
        """
        super(Sensor, self).__init__(dbClient,Name)
        self.cycletime = cycletime
        self.mode = mode
        self.mqtt = MClient('/' + Globals._PlantName + '/Sensors/' + Name, self.LogEntry)


    def ValidateDevice(self):
        """method to make sure the sensor has all that is needed to operate.  Interface to hardware, logging, etc"""
        return self.Props.has_key('DeviceID')

    def ReadDevice(self, numberOfValues=1,Timeout=5000,bytesToRead=1):
        """method uses the configured interface to read a datapoint.  Returns a list of 1 or more values.

        Needs two parameters:  # of values to expect, timeout in milliseconds, # of bytes per read 
        """
        if not self.ValidateDevice():
            self.LogEntry({'Description': 'Validation failed during '+self.__name__+'.ReadDevice'})
            return None
        else
            self.ReadInterface(1,0,self.LogEntry)

    def LogEntry(self,data):
        """Takes raw data from a ReadInterface callback and puts it into a Loggable/MQTT format
        """

        

