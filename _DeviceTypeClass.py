from _DatabaseClass import *
from bson.objectid import ObjectId

class DeviceType:
	'Class that defines the type of device: sensor, relay, etc.  Records information about hardware also.'

	#Props = {'_id', 'Name', 'Manufacturer', 'PartNumber', 'Active'}

	def __init__(self,dbClient,Name):
		#Assume that by now we have a connection to the appropriate database
		self.dbtable = dbTable(dbClient,'DeviceTypes')
		self.loaded = False
		self.LoadRecord(Name)

	def CreateType(self,manufacturer,partnumber):
		if not self.loaded:
			self.Props['Manufacturer'] = manufacturer
			self.Props['PartNumber'] = partnumber
			self.Props['_id'] = self.dbtable.InsertOne(self.Props)
			
		
	def ChangeProperty(self, property, value):
		self.Props[property]=value
		self.SaveRecord()

	def LoadRecord(self,name):
		self.Props = self.dbtable.FindByName(name)
		## In case the Find returns None, then we at least have the name to create a new type
		if self.Props == None:
			self.Props = {'Name': name}
		else:
			self.loaded = True

	def SaveRecord(self):
		result = self.dbtable.UpdateOne({'_id': self.Props['_id']},self.Props)
		print result.matched_count
		print result.modified_count
		return result
	
