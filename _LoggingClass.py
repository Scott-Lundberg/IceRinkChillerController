import sys
import time
from _DatabaseClass import *

class Logger:
	'Class that provides logging to database structures.  Tied to each device that needs logging so default header information can be provided.'


	#Format of timestamps should be consistent, always
	_timeFormat = "%a, %d %b %Y %H:%M:%S " + str((time.timezone if time.daylight == 0 else time.altzone) * 100 / 60 )
		
	## Needs instantiated database table/collection to operate 
	def __init__(self,dbclient,device):
            """Creates a Logging object to be used for database recording of data
                
                dbclient is a reference to an instantiated database object
                device is a dict from the _DeviceClass Props must contain an _id and collection item
            """
		self.device = device
		self.deviceID = device['_id']
		self.dbHeaderTable = dbTable(dbclient,device['collection'])
		self.dbDetailTable = dbTable(dbclient,device['collection']+'Detail')

	def LogEntry(self,in_dict):
		"""in_dict contains {header:specific desc, details: [{line1},{line2},{line2},...]}"""
		entry = {'DeviceID':self.deviceID,'Description':in_dict['header'],'DateTimeStamp':time.strftime(Logger._timeFormat),'DetailRecordCount': len(in_dict['details'])}
		headerID = self.dbHeaderTable.InsertOne(entry)
		
		#Detail entries, if they exist
		for i,j in enumerate(in_dict['details']):
			in_dict['details'][i]['LogID'] = headerID
	
		detailIDs = self.dbDetailTable.InsertMany(in_dict['details'])
		
		
