#! /usr/bin/python

from  _DatabaseClass import *
import pprint

mclient = SystemDB()
mclient.AttachDatabase('test')

testTable = dbTable(mclient,'TT')

post = {"Type": "Sensor", "Name": "temperature", "LogDetails": ["Field1", "Field2"]}
recordID = testTable.InsertOne(post)

print recordID

pprint.pprint(testTable.FindById(recordID))

mclient.DropDatabase()

