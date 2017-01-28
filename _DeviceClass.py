from _DatabaseClass import *
from bson.objectid import ObjectId

class Device(object):
	'Base class that is used for all sensors, relay and the controller itself'

	#Props = {'_id', 'Name', 'Manufacturer', 'PartNumber', 'Active'}

	def __init__(self,dbClient,Name):
		## Assume that by now we have a connection to the appropriate database
		self.dbtable = dbTable(dbClient,'Devices')
		self.loaded = False
		self.LoadDevice(Name)

	def CreateDevice(self,manufacturer,partnumber):
		if not self.loaded:
			self.Props['Manufacturer'] = manufacturer
			self.Props['PartNumber'] = partnumber
			self.Props['_id'] = self.dbtable.InsertOne(self.Props)
			
		
	def ChangeProperty(self, property, value):
		self.Props[property]=value
		self.SaveDevice()

	def LoadDevice(self,name):
		self.Props = self.dbtable.FindByName(name)
		## In case the Find returns None, then we at least have the name to create a new device
		if self.Props == None:
			self.Props = {'Name': name}
		else:
			self.loaded = True

	def SaveDevice(self):
		result = self.dbtable.UpdateOne({'_id': self.Props['_id']},self.Props)
		print result.matched_count
		print result.modified_count
		return result
	
