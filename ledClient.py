from gpiozero import LED
from time import sleep
import threading 
import paho.mqtt.client as mqtt


red = LED(17)
yellow = LED(23)
green = LED(26)


def on_connect(client, userdata, flags, rc):
    client.subscribe("Doorbell")

def on_message(client, userdata, msg):
    global red
    global green
    global yellow
    
    
    
    print(str(msg.payload))
    if "No one is at the door" in str(msg.payload):
            yellow.on()
            green.off()
            red.off()
    if "Teo Leng is at the door" in str(msg.payload):
            green.on()
            red.off()
            yellow.off()
    if "Kee Boon Hwee is at the door" in str(msg.payload):
            green.on()
            red.off()
            yellow.off()
    if "Unknown person(s) is at the door" in str(msg.payload):
            print("asdasdas")
            red.on()
            yellow.off()
            green.off()
            
    
    
def main():
 

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host="192.168.156.141",port=1883, keepalive = 5)
    client.loop_start()



    
    



if __name__ == "__main__":
    main()



