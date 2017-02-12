from _DeviceClass import *
from _Globals import *
from _MessageClass import *
import time
import thread

class Sensor(Device):
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
        return self.Props.has_key('_id')

    def ReadDevice(self, numberOfValues=1,Timeout=1000,bytesToRead=1):
        """method uses the configured interface to read a datapoint.  Returns a list of 1 or more values.

        Needs two parameters:  # of values to expect, timeout in milliseconds, # of bytes per read 
        """
        if not self.ValidateDevice():
            self.LogEntry({'Error': 'Validation failed during Sensor.ReadDevice'})
            return None
        else:
            self.lastread = None
            thread.start_new_thread(self.ReadInterface,(numberOfValues,Timeout,bytesToRead,self.LogEntry))

    def LogEntry(self,entry):
        """
            Incoming data can be either Errors or data.  
            Typically takes raw data from a ReadInterface callback and puts it into a Loggable/MQTT format
        """
        if self.mode == 'event' and entry['data'] == self.lastread:
            pass
        else:
            if entry.has_key('Error'):
                logentry = {'Description': 'Error:'+entry['Error']}
                mqtt = {'Description': 'Error:'+entry['Error']}
            else:
                self.lastread = entry['data']
                logentry = {'Description': 'Data Read','details':[{'data':entry['data']}]}
                mqtt = {'Description': 'Data Read','details':[{'data':entry['data']}], 'DeviceID': self.Props['_id']}

            super(Sensor, self).LogEntry(logentry)
            print logentry
        
