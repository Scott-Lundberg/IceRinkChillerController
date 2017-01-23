from _DatabaseClass import *

class DeviceType:
	'Class that defines the type of device: sensor, relay, etc.  Records information about hardware also.'

	#Props = {'Type_id', 'Name', 'Manufacturer', 'PartNumber', 'Active'}

	def __init__(self,dbClient,Name):
		#Assume that by now we have a connection to the appropriate database
		self.dbtable = dbTable(dbClient,'DeviceTypes')
		self.LoadRecord(Name)

	def CreateType(self,manufacturer,partnumber):
		self.Props['Manufacturer'] = manufacturer
		self.Props['PartNumber'] = partnumber
		self.Props['Type_id'] = self.dbtable.InsertOne(self.Props)
		
	def ChangeManufacturer(self, manufacturer):
		self.manufacturer=manufacturer
		self.SaveRecord()

	def ChangePartNumber(self,partnumber):
		self.partnumber=partnumber
		self.SaveRecord()

	def LoadRecord(self,name):
		self.Props = self.dbtable.FindByName(name)
		self.Props['Name':name]  #In case the Find returns None, then we at least have the name to create a new type

	def SaveRecord(self):
		return self.dbtable.UpdateOne({'Type_id': self.Props['Type_id']},self.Props)
	
