#! /usr/bin/python

from _DatabaseClass import *
from _SensorClass import *
##from _DeviceClass import *
import time
import sys
##import pprint


mclient = SystemDB()
mclient.AttachDatabase()

mysensor = Sensor(mclient,'TestButton',1)
mysensor.DefineInterface({'type': 'GPIO', 'header':'P9', 'pin':'12', 'IODirection': 'IN'})
mysensor.SetupInterface()
mysensor.ReadDevice(0,0)

mysensor2 = Sensor(mclient,'Light',1)
mysensor2.DefineInterface({'type': 'ADC', 'header':'P9', 'pin':'39'})
mysensor2.SetupInterface()
mysensor2.ReadDevice(0,0)

time.sleep(int(sys.argv[1]))
mysensor.StopRead()

