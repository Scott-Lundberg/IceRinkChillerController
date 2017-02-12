import time
from _DatabaseClass import *

class Logger:
	'Class that provides logging to database structures.  '


	#Format of timestamps should be consistent, always
	_timeFormat = "%a, %d %b %Y %H:%M:%S " + str((time.timezone if time.daylight == 0 else time.altzone) * 100 / 60 )
		
	def __init__(self,dbclient,collection):
            """
            Creates a Logging object to be used for database recording of data
                
            dbclient is a reference to an instantiated database object 
            """
            self.dbHeaderTable = dbTable(dbclient,collection)
            self.dbDetailTable = dbTable(dbclient,collection+'Detail')

	def LogEntry(self,entry):
            """
            entry contains {'DeviceID': deviceid, 'Description':specific desc, details: [{line1},{line2},{line2},...]}
            """
            entry['DateTimeStamp'] = time.strftime(Logger._timeFormat)
            entry['DetailRecordCount'] = len(entry.get('details',[]))
            temp = entry.copy()
            if temp.has_key('details'):
                del temp['details']
            headerID = self.dbHeaderTable.InsertOne(temp)

            #Detail entries, if they exist
            for i,j in enumerate(entry['details']):
                entry['details'][i]['LogID'] = headerID
            
            detailIDs = self.dbDetailTable.InsertMany(entry['details'])
		
		
		
