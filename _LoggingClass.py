import sys
import time

class Logger:
	'Class that provides logging to database structures.  Tied to each device that needs logging so default header information can be provided.'


	#Format of timestamps should be consistent, always
	_timeFormat = "%a, %d %b %Y %H:%M:%S " + str((time.timezone if time.daylight == 0 else time.altzone) * 100 / 60 )
		
	## Needs instantiated database table/collection to operate 
	def __init__(self,dbclient,device):
		self.device = device
		self.deviceID = self.device.identity
		self.dbHeaderTable = dbTable(dbclient,self.device.collection)
		self.dbDetailTable = dbTable(dbclient,self.device.collection+'Detail')

	def LogEntry(self,in_dict):
		#Input dictionary with {header:specific desc, details: [{line1},{line2},{line2},...]}
		entry = {'DeviceID':self.deviceID,'Description':in_dict['header'],'DateTimeStamp':time.strftime(Logger._timeFormat),'DetailRecordCount':in_dict['details'].count}
		headerID = self.dbHeaderTable.InsertOne(entry)
		
		#Detail entries, if they exist
		for d in enumerate(in_dict['details']):
			d['LogID'] = headerID
	
		detailIDs = self.dbDetailTable.InsertMany(in_dict['details'])
		
		
