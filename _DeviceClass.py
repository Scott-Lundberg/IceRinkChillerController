from _DatabaseClass import *
from abc import ABCMeta, abstractmethod
from Adafruit_I2C import Adafruit_I2C

class Device(object):
	'Base class that is used for all sensors, relay and the controller itself'
    __metaclass__ = ABCMeta

    def __init__(self,dbClient,Name):
	## Assume that by now we have a connection to the appropriate database
	self.dbtable = dbTable(dbClient,'Devices')
	self.loaded = False
	self.LoadDevice(Name)

    @abstractmethod
    def ValidateDevice(self):
        ' Overridden method to make sure that our device has all properties required to operate'
        pass

    def CreateDevice(self,minProps):
        ' CreateDevice:  Creates a new device in memory.  Parameter minProps is a dictionary that contains the minimum properties required to create a device, typically a Name'
	if not self.loaded:
            del minProps['_id'] if minProps.has_key('_id')
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
        self.Props['IOInterface'] = interface
        self.SaveDevice()

    def SetupInterface(self):
        ' Setup GPIO or I2C i/o. self.props[IOInterface] contains a dictionary with appropriate values '
        if self.Props['IOInterface']['type'] == 'I2C':
            ## Need bus number and address to setup I2C interface
            ## Also need to know whether we are reading 8 or 16 bits signed/unsigned
            self.interface = Adafruit_I2C(self.Props['IOInterface']['address'])

        elif self.Props['IOInterface']['type'] == 'GPIO':

        elif self.Props['IOInterface']['type'] == '1-Wire':
            pass  ##TBD

        elif self.Props['IOInterface']['type'] == 'SPI':
            pass  ##TBD
		
    def ChangeProperty(self, changingProps):
        ' Updates properties in the device"s dictionary, then saves to the database for future persistence '
        return False if type(changingProps) <> dict
	self.Props[property].update(changingProps)
	self.SaveDevice()
        return True

    def LoadDevice(self,name):
        ' Loads device settings/Props from the database '
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
	
