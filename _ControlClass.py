from _Globals import *
from _DeviceClass import *


class Control(Device):
    """ Controls to be used to turn on relays """

    def __init__(self, Name):

        super(Control, self).__init(Name)
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

    def WriteDevice(self,buf):
        """Writes the buf to the device.  Normally 1 or 0"""

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

