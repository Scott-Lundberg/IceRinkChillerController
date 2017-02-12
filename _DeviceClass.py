from _DatabaseClass import *
from _LoggingClass import *
import thread
from abc import ABCMeta, abstractmethod
from Adafruit_I2C import Adafruit_I2C
from Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.PWM as PWM

class Device(object):
	'Base class that is used for all sensors, relay and the controller itself'
    __metaclass__ = ABCMeta

    def __init__(self,dbClient,Name):
	## Assume that by now we have a connection to the appropriate database
	self.dbtable = dbTable(dbClient,'Devices')
	self.loaded = False
	self.LoadDevice(Name)
        self.log = Logger(dbClient,self.Props['collection'])


    @abstractmethod
    def ValidateDevice(self):
        ' Overridden method to make sure that our device has all properties required to operate'
        pass

    def CreateDevice(self,minProps):
        ' CreateDevice:  Creates a new device in memory.  Parameter minProps is a dictionary that contains the minimum properties required to create a device, typically a Name'
	if not self.loaded:
            del minProps['_id'] if minProps.has_key('_id')
            self.Props['collection'] = 'Devicelog'
            self.Props.update(minProps)
            self.Props['Active']=True if not minProps.has_key('Active')
			self.Props['_id'] = self.dbtable.InsertOne(self.Props)
            if self.Props <> None:
                self.loaded = True
                return True
            else:
                return False
        else:
            return self.ChangeProperty(minProps)

    def RemoveDevice(self):
        ' Removes a device from the system.  Just sets active to False in the Properties '
        if self.loaded:
            self.ChangeProperty({'Active': False})
            self.SaveDevice()
            del self.Props
            return True
        else:
            return False

    def DefineInterface(self,interface):
        """Method attaches metadata necessary to start I/O. Saves it in the database for later use
        
            Currently supports I2C and GPIO.  Dictionary items must be as follows:
            I2C{'type':'I2C', 'address':'<Hex string of address of device>', 'bus':'<bus number', 'signedint':'<True/False>', 'numberofbits': '##'}
            GPIO{'type': 'GPIO', 'header':'<P9 or P8>', 'pin':'<pin number>', 'IODirection': '<OUT|IN>'}
            """
        self.Props['IOInterface'] = interface
        self.SaveDevice()

    def SetupInterface(self):
        """Method uses Adafruit library to setup connections on IO pins. """
        
        if self.Props['IOInterface']['type'] == 'I2C':
            self.interface = Adafruit_I2C(self.Props['IOInterface']['address'])

        elif self.Props['IOInterface']['type'] == 'GPIO':
            self.interface = self.Props['IOInterface']['header']+'_'+str(self.Props['IOInterface']['pin'])
            GPIO.setup(self.interface, self.Props['IOInterface']['IODirection'])

        elif self.Props['IOInterface']['type'] == '1-Wire':
            pass  ##TBD

        elif self.Props['IOInterface']['type'] == 'SPI':
            pass  ##TBD

    def ReadInterface(self,count,waittime,callback):
        """Starts a loop with count times (0 for infinity) and a waittime between reads

            Needs callback function to deliver results.  Parameters to callback are just the data
        """
        pass

    def LogEntry(self,entry):
       """Make a log entry for this Device
            entry contains {Description:specific desc, details: [{line1},{line2},{line2},...]}
            this function will add DeviceID
        """
        entry['DeviceID']=self.Props['DeviceID']
        self.log.LogEntry(entry) 
        
    def ClearInterface(self):
        """Removes references to external interface libraries and/or runs a tear-down function from the library 
        """
        if self.Props['IOInterface']['type'] == 'GPIO':
            GPIO.cleanup()
        self.interface = None
 	
    def ChangeProperty(self, changingProps):
        """Updates properties in the device"s dictionary, then saves to the database for future persistence
        """
        return False if type(changingProps) <> dict
	self.Props[property].update(changingProps)
	self.SaveDevice()
        return True

    def LoadDevice(self,name):
        """Loads device settings/Props from the database
        """

	self.Props = self.dbtable.FindByName(name)
	## In case the Find returns None, then we at least have the name to create a new device
	if self.Props == None:
            return self.CreateDevice({'Name': name})
	else:
            self.loaded = True
            return True

    def SaveDevice(self):
	result = self.dbtable.UpdateOne({'_id': self.Props['_id']},self.Props)
        return (True if result.modified_count > 0 else False)
	
