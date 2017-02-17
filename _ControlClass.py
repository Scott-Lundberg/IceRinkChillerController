from _Globals import *
from _DeviceClass import *
from _MessageClass import *


class Control(Device):
    """ Controls to be used to turn on relays """

    def __init__(self, Name):

        super(Control, self).__init__(Name)
        self.mqttc = MClient('/' + Globals._PlantName + '/Controls/' + Name, Globals._MQTTLogLevel)
        self.mqttc.Connect()


    def ValidateDevice(self):
        """method to make sure the Control has all that is needed to operate.  Interface to hardware, logging, etc"""
        isvalid=True
        if not self.Props.has_key('_id'):
            isvalid=False
        if self.interface == None:
            isvalid=False

        return isvalid

    def Subscribe(self,callback):
        """Setup subscription to MQTT channel with callback when message received"""
        self.mqttc.Receive(callback)


    def WriteRelay(self,onoff='off'):
        """sets relay to on or off. String verison"""
        if onoff == 'on' or onoff=='1' or onoff=='yes' or onoff=='Yes':
            self.WriteInterface({'type':'GPIO','action':1})
        else:
            self.WriteInterface({'type':'GPIO','action':0})

    def WriteRelay(self,onoff=False):
        """sets relay to on or off. boolean verison"""
        if onoff == True:
            self.WriteInterface({'action':1})
        else:
            self.WriteInterface({'action':0})

    def WriteRelay(self,onoff=0):
        """sets relay to on or off. int verison"""
        if onoff == 1:
            self.WriteInterface({'action':1})
        else:
            self.WriteInterface({'action':0})

    def WritePWM(self,duty=50,freq=1000,polarity=1):
        """Starts the output with duty, freq and polarity"""
        self.WriteInterface({'duty':duty,'freq':freq,'polarity':polarity})


    def LogEntry(self,entry):
        """
            Incoming data can be either Errors or data.  
            Typically takes raw data from a ReadInterface callback and puts it into a Loggable/MQTT format
        """
        if entry.has_key('Error'):
            logentry = {'Description': 'Error:'+entry['Error']}
            mqtt = 'Error:'+str(entry['Error'])
        else:
            logentry = {'Description': 'Data Written','details':[{'data':entry['data']}]}
            mqtt = str(entry['data'])

        super(Control, self).LogEntry(logentry)
        self.mqttc.Send(mqtt)

