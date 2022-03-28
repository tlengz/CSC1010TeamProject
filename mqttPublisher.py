#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#publish.single(topic="test", payload="Hello", hostname="localhost",port=1883)
publish.single(topic="test", payload="Good Night", retain=True, hostname="192.168.0.157",port=1883,keepalive=5)
