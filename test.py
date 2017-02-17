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

def setgpio(client,userdata,message):
    myled.WriteRelay(message.payload)

Globals._dbClient = SystemDB()
Globals._dbClient.AttachDatabase()

print "testbutton"
mysensor = Sensor('TestButton')
mysensor.DefineInterface({'type': 'GPIO', 'header':'P9', 'pin':'12', 'IODirection': 'IN'})
mysensor.SetupInterface()
mysensor.ReadDevice(0,0)

print "ambientlight"
mysensor2 = Sensor('AmbientLight')
mysensor2.DefineInterface({'type': 'ADC', 'header':'P9', 'pin':'39'})
mysensor2.SetupInterface()
mysensor2.ReadDevice(0,1000)

print "GPIO LED"
myled = Control('GPIOLED')
myled.DefineInterface({'type': 'GPIO', 'header':'P9', 'pin':'15','IODirection':'OUT'})
myled.SetupInterface()
myled.Subscribe(setgpio)

print "PWM LED"
mylight = Control('PWMLED')
mylight.DefineInterface({'type': 'PWM', 'header':'P9', 'pin':'14'})
mylight.SetupInterface()
mylight.Subscribe(setled)

time.sleep(int(sys.argv[1]))
mysensor.StopRead()
mysensor2.StopRead()
mylight.StopWrite()
myled.StopWrite()

