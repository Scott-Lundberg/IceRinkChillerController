import paho.mqtt.client as paho
from _LoggingClass import *
from _Globals import *

class MClient():
    """Used to setup and send MQTT messages to a broker
        
       the channel is specific to each instance, so you can't publish to one channel and subscribe to another with the
       same instance
    """
    _Loglevel = {'1':('MQTT_LOG_INFO',6), '2': ('MQTT_LOG_NOTICE',5), '4':('MQTT_LOG_WARNING',4),'8':('MQTT_LOG_ERR',3),'16':('MQTT_LOG_DEBUG',7)}

    def __init__(self,channel,loglevel=4):
        self.mqttc = paho.Client()
        self.options = {}
        self.channel = channel
        self.loglevel = loglevel
        self.mqttc.on_log = self.WriteLog
        self.log = Logger(Globals._MessageLog)

    def SetOptions(self,options):
        """Sets options to be used later in MQTT client.  

        options is a dictionary with options as keys
        """
        if len(options) > 0:
            self.options = options 

    def GetOption(self,option,default):
        """Returns option if set, default if not set or key doesn't exist"""
        if not self.options.has_key(option):
            return default
        else:
            self.options[option]

    def Connect(self,broker=Globals._MQTTBroker,port=Globals._MQTTPort,heartbeat=60):
        """function to connect the client to a broker. 

            Takes in a broker host/ip, port number and maximum heartbeat period
        """
        self.mqttc.connect(broker,port,heartbeat)
        self.mqttc.loop_start()

    def Send(self,message):
        """publishes a message to a channel
            Takes in a message and channel string
        """
        self.mqttc.publish(self.channel,message,self.GetOption("qos",0))

    def Receive(self,callback):
        """subscribes to a channel/topic.  sets up call back function from calling object
        
            callback requires 3 parameters: client,userdata, message (object) """
        self.mqttc.subscribe(self.channel,self.GetOption("qos",0))
        self.mqttc.on_message=callback
        self.mqttc.message_callback_add(self.channel,callback)

    def Disconnect(self):
        """close our message loop and disconnect from the broker"""
        self.mqttc.loop_stop()
        self.mqttc.disconnect()
    
    def WriteLog(self, client, userdata, level, buf):
        """Write a log entry to the Device's database collection

            During init of MClient, the logging level can be set, otherwise, it's MQTT_LOG_WARNING by default
            MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, and MQTT_LOG_DEBUG are the levels of logging
        """
        if MClient._Loglevel[str(level)][1] <= self.loglevel:
            self.log.LogEntry({'Description': MClient._Loglevel[str(level)][0] + ' message on channel ' + self.channel, 'details':[{'detail':buf}]})

