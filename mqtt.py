import paho.mqtt.client as mqtt
import time
import threading

client = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)

def init():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("broker.mqtt.cool", 1883, 60)

def publishMessage(message):
    client.publish('/shane/steve/weather/temp', message);

if __name__ == '__main__':
    init()