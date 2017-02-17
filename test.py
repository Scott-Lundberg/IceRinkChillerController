#! /usr/bin/python

from _Globals import *
from _DatabaseClass import *
from _SensorClass import *
from _ControlClass import *
##from _DeviceClass import *
import time
import sys
##import pprint

def setled(client, userdata, message):
    mylight.WritePWM(50,int(message.payload),1)

Globals._dbClient = SystemDB()
Globals._dbClient.AttachDatabase()

mysensor = Sensor('TestButton')
mysensor.DefineInterface({'type': 'GPIO', 'header':'P9', 'pin':'12', 'IODirection': 'IN'})
mysensor.SetupInterface()
mysensor.ReadDevice(0,0)

mysensor2 = Sensor('AmbientLight')
mysensor2.DefineInterface({'type': 'ADC', 'header':'P9', 'pin':'39'})
mysensor2.SetupInterface()
mysensor2.ReadDevice(0)

mylight = Control('LED')
mylight.DefineInterface({'type': 'PWM', 'header':'P9', 'pin':'14'})
mylight.SetupInterface()
mylight.Subscribe(setled)

time.sleep(int(sys.argv[1]))
mysensor.StopRead()
mysensor2.StopRead()
mylight.StopWrite()

