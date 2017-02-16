import pymongo
import sys
from _Globals import *
from pymongo import MongoClient
from bson.objectid import ObjectId

class SystemDB(object):
	'Class to implement a database for use for settings and logging'

	def __init__(self,interface=Globals._DBInterface,port=Globals._DBPort):
            self.dbClient = MongoClient(interface,port)

	def AttachDatabase(self,database=Globals._Database):
            self.db = self.dbClient[database]

	def DropDatabase(self):
            if isinstance(SystemDB,self.db):
                self.dbClient.drop_database(self.db)
	
	def ConnectionValid(self):
            return isinstance(SystemDB,self.dbClient)

class dbTable:
	"""Class that implements collections/tables, including inserts, updates, selects.  Requires SystemDB object exists."""

	def __init__(self,collection):
            if not isinstance(Globals._dbClient,SystemDB):
                Globals._dbClient = SystemDB()
            self.collection = Globals._dbClient.db[collection]

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
	
