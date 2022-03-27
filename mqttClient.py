import paho.mqtt.client as mqtt
#import paho.mqtt.publish as publish

def on_connect(client, userdata, flags, rc):
    client.subscribe("test")

def on_message(client, userdata, msg):
    print(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host="192.168.0.157",port=1883, keepalive = 5)
client.loop_forever()