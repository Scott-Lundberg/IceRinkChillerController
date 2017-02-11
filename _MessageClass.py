import paho.mqtt.client as paho

class MClient():
    """Used to setup and send MQTT messages to a broker"""

    def __init__(self):
        self.mqttc = paho.Client()
        self.options = {}

    def SetOptions(self,options):
        """Sets options to be used later in MQTT client.  

        options is a dictionary with options as keys
        """
        self.options = options

    def GetOption(self,option,default):
        """Returns option if set, default if not set or key doesn't exist"""
        return default if not self.options.has_key(option) else self.options[option]

    def Connect(self,broker="localhost",port=1883,heartbeat=60):
        """function to connect the client to a broker. 

            Takes in a broker host/ip, port number and maximum heartbeat period
        """
        self.mqttc.connect(broker,port,heartbeat)
        self.mqttc.loop_start()

    def Send(self,message,channel):
        """publishes a message to a channel
            Takes in a message and channel string
        """
        self.mqttc.publish(channel,message,self.GetOption("qos",0))

    def Receive(self,channel,callback):
        """subscribes to a channel/topic.  sets up call back function from calling object
        
            callback requires 3 parameters: client,userdata, message (object) """
        self.mqttc.subscribe(channel,self.GetOption("qos",0))
        self.mqttc.message_callback_add(channel,callback)

    def Disconnect(self):
        self.mqttc.loop_stop()
        self.mqttc.disconnect()




class MBroker():
    """Used to startup a broker for use by publishers and subscribers"""



