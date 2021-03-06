from _DatabaseClass import *
from _LoggingClass import *
from _Globals import *
from abc import ABCMeta, abstractmethod
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

class Device(object):
    """Base class that is used for all sensors, relay and the controller itself"""
    __metaclass__ = ABCMeta

    def __init__(self,Name):
	"""
            Assume that by now we have a connection to the appropriate database
        """
	self.dbtable = dbTable('Devices')
	self.loaded = False
        self.stopread = False
	self.LoadDevice(Name)
        self.log = Logger(self.Props['collection'])
        self.validinterface = False

    @abstractmethod
    def ValidateDevice(self):
        """Overridden method to make sure that our device has all properties required to operate"""
        pass

    def CreateDevice(self,minProps):
        """CreateDevice:  Creates a new device in memory.  
        
            Parameter minProps is a dictionary that contains the minimum properties required to create a device, typically a Name
        """
        if minProps.has_key('_id'): 
            del minProps['_id'] 
	if not self.loaded:
            self.Props.update(minProps)
            self.Props['collection'] = 'Devicelog'
            if not minProps.has_key('Active'):
                self.Props['Active']=True 
	    self.Props['_id'] = self.dbtable.InsertOne(self.Props)
            if self.Props['_id'] <> None:
                self.loaded = True
                return True
            else:
                return False
        else:
            return self.ChangeProperty(minProps)

    def RemoveDevice(self):
        """Removes a device from the system.  Just sets active to False in the Properties"""
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
            ADC{'type': 'ADC', 'header':'<P9 or P8>', 'pin':'<pin number>'}
            PWM{'type': 'PWM', 'header':'<P9 or P8>', 'pin':'<pin number>', 'frequency': 'hz'}
        """
        self.Props['IOInterface'] = interface
        self.SaveDevice()

    def SetupInterface(self):
        """Method uses Adafruit library to setup connections on IO pins. """
        
        if self.Props['IOInterface']['type'] == 'I2C':
            self.interface = Adafruit_I2C(self.Props['IOInterface']['address'])

        elif self.Props['IOInterface']['type'] == 'GPIO':
            self.interface = self.Props['IOInterface']['header']+'_'+str(self.Props['IOInterface']['pin'])
            GPIO.setup(self.interface, eval('GPIO.'+self.Props['IOInterface']['IODirection']))

        elif self.Props['IOInterface']['type'] == 'ADC':
            self.interface = self.Props['IOInterface']['header']+'_'+str(self.Props['IOInterface']['pin'])
            ADC.setup()

        elif self.Props['IOInterface']['type'] == 'PWM':
            self.interface = self.Props['IOInterface']['header']+'_'+str(self.Props['IOInterface']['pin'])

        elif self.Props['IOInterface']['type'] == '1-Wire':
            pass  ##TBD

        elif self.Props['IOInterface']['type'] == 'SPI':
            pass  ##TBD

    def ReadInterface(self,count,waittime,valuestoread,callback,cycletime):
        """Starts a loop with count times (0 for infinity) and a waittime between reads, up to a maximum of cycletime per second

            Needs callback function to deliver results.  Parameters to callback are just the data
        """

        ## We have a minimum sample speed to keep the processor from being overloaded by one sensor.
        if (waittime) > cycletime:
            calculatedwait = waittime
        else:
            calculatedwait = cycletime

        loopcounter = count-1
        readbyte=0
        self.stopread=False
        while loopcounter <> 0 and not self.stopread:
            if self.Props['IOInterface']['type'] == 'I2C':
                self.interface.readS8(readbyte)
                callback({'data': [readbyte]})
            elif self.Props['IOInterface']['type'] == 'GPIO':
                callback({'data': GPIO.input(self.interface)})
            elif self.Props['IOInterface']['type'] == 'ADC':
                callback({'data': str(ADC.read(self.interface))})
            loopcounter -= 1
            if waittime <> 0:
                time.sleep(calculatedwait/1000) 

    def WriteInterface(self,buf):
        """Writes data received in incoming dictionary, buf to the configured interface"""
        if self.Props['IOInterface']['type'] == 'GPIO':
            if buf['action']==1:
                GPIO.output(self.interface,GPIO.HIGH)
            else:
                GPIO.output(self.interface,GPIO.LOW)
        elif self.Props['IOInterface']['type'] == 'PWM':
            PWM.start(self.interface,buf['duty'],buf['freq'],buf['polarity'])

    def StopRead(self):
        """Sets self.stopread to True so that any sensor reading loops will stop """
        self.stopread = True
        self.ClearInterface()

    def StopWrite(self):
        """Turns interface to off"""
        if self.Props['IOInterface']['type'] == 'GPIO':
            GPIO.output(self.interface,0)
        elif self.Props['IOInterface']['type'] == 'PWM':
            PWM.stop(self.interface)
            PWM.cleanup()

    def LogEntry(self,entry):
        """Make a log entry for this Device
            entry contains {Description:specific desc, details: [{line1},{line2},{line2},...]}
            this function will add DeviceID
        """
        entry['DeviceID']=self.Props['_id']
        self.log.LogEntry(entry) 
        
    def ClearInterface(self):
        """Removes references to external interface libraries and/or runs a tear-down function from the library 
        """
        if self.Props['IOInterface']['type'] == 'GPIO':
            GPIO.cleanup()
        elif self.Props['IOInterface']['type'] == 'PWM':
            PWM.stop(self.interface)
            PWM.cleanup()

        self.interface = None
 	
    def ChangeProperty(self, changingProps):
        """Updates properties in the device"s dictionary, then saves to the database for future persistence
        """
        if type(changingProps) <> dict:
            return False
	self.Props[property].update(changingProps)
	self.SaveDevice()
        return True

    def LoadDevice(self,name):
        """Loads device settings/Props from the database
        """

	self.Props = self.dbtable.FindByName(name)
	## In case the Find returns None, then we at least have the name to create a new device
	if not isinstance(self.Props,dict):
            self.Props = {}
            return self.CreateDevice({'Name': name})
	else:
            self.loaded = True
            return True

    def SaveDevice(self):
        """Writes all configured properties to the database for future loading"""
        temp = self.Props.copy()
        if temp.has_key('_id'):
            del temp['_id']
        result = self.dbtable.UpdateOne({'_id': self.Props['_id']},temp)
        if not isinstance(result,pymongo.results.UpdateResult):
            return False
        return (True if result.modified_count > 0 else False)
	
