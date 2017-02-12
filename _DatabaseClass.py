import pymongo
import sys
from _Globals import *
from pymongo import MongoClient
from bson.objectid import ObjectId

class SystemDB(object):
	'Class to implement a database for use for settings and logging'

	_dbclient = None
	_db = None
        gb = Globals()

	def __init__(self,interface=gb._DBInterface,port=gb._DBPort):
		if SystemDB._dbclient == None:	
			SystemDB._dbclient = MongoClient(interface,port)

	def AttachDatabase(self,database=gb._Database):
		if SystemDB._db == None:
			SystemDB._db = SystemDB._dbclient[database]

	def DropDatabase(self):
		if SystemDB._db <> None:
			SystemDB._dbclient.drop_database(SystemDB._db)
	
	def ConnectionValid(self):
		return (True if _dbclient <> None else False)

class dbTable:
	"""Class that implements collections/tables, including inserts, updates, selects.  Requires SystemDB object exists."""

	def __new__(dbclient,collection):
		if not dbclient.ConnectionValid():
			sys.exit("dbTable Class: Can't connection to Collection.  Database connection not valid.\n")
			return None
		else:
			return super(dbTable, dbclient, collection).__new__(dbclient, collection)			
		
	def __init__(self,dbclient,collection):
		self.dbclient = dbclient
		self.collection = self.dbclient._db[collection]

	def InsertOne(self,record):
		return self.collection.insert_one(record).inserted_id

	def InsertMany(self,listofrecords):
		#takes in a list of dictionaries.  returns a list of IDs
		return self.collection.insert_many(listofrecords).inserted_ids

	def FindById(self,recordID):
		oid = ObjectId(recordID)
		return self.collection.find_one({'_id': oid})

	def FindByName(self,name):
		return self.collection.find_one({'Name': name})

	def UpdateOne(self,filter,record):
		#filter out _id if it's in the record
		if '_id' in record:
			del(record['_id'])
		if not isinstance(filter['_id'], ObjectId):
			filter['_id']=ObjectId(filter['_id'])
		result = self.collection.update_one(filter,{'$set':record}).modified_count
		return (noRecord if result == None else result)
			

class noRecord:
	modified_count = 0
	matched_count = 0
	
