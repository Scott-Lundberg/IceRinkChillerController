import pymongo
from pymongo import MongoClient

class SystemDB:
	'Class to implement a database for use for settings and logging'

	_dbclient = None
	_db = None

	def __init__(self,interface='localhost',port=27017):
		if SystemDB._dbclient == None:
			SystemDB._dbclient = MongoClient(interface,port)

	def AttachDatabase(self,database='RinkController'):
		if SystemDB._db == None:
			SystemDB._db = SystemDB._dbclient[database]

	def DropDatabase(self):
		if SystemDB._db <> None:
			SystemDB._dbclient.drop_database(SystemDB._db)
	
	def ConnectionValid(self):
		return (True if _dbclient <> None else False)

class dbTable:
	'Class that implements collections/tables, including inserts, updates, selects.  Requires SystemDB object exists.'

	def __init__(self,dbclient,collection):
		if dbclient.ConnectionValid <> True:
			dbclient = SystemDB()
		self.collection = dbclient._db[collection]

	def InsertOne(self,record):
		return self.collection.insert_one(record).inserted_id

	def FindById(self,recordID):
		return self.collection.find_one({"_id": recordID})	


