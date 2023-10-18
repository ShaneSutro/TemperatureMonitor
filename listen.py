import os, sys, io
import M5
from M5 import *
from umqtt import *
import urequests as requests
from hardware import *
import time


mqtt_client = None
http_req = None
rgb = None


msg = None

# Describe this function...
def sendPushNotification(msg):
  global mqtt_client, http_req, rgb
  http_req = requests.post('https://api.pushover.net/1/messages.json', json={'token':'adnfdgcgtak4x3gwtcm3g8veddva9n','user':'ua8hetxm48mygrz1w96dpnxshni3n4','message':msg}, headers={'Content-Type':'application/json'})
  print(http_req.status_code)
  print(msg)
  rgb.fill_color(0xff0000)
  http_req.close()
  time.sleep(1)


def mqtt__shane_steve_weather_temp_event(data):
  global mqtt_client, http_req, rgb, msg
  sendPushNotification(data[1])


def setup():
  global mqtt_client, http_req, rgb, msg

  M5.begin()
  rgb = RGB()
  mqtt_client = MQTTClient('Temp Read', 'broker.mqtt.cool', port=1883, user='', password='', keepalive=0)
  mqtt_client.connect(clean_session=True)
  mqtt_client.subscribe('/shane/steve/weather/temp', mqtt__shane_steve_weather_temp_event, qos=0)


def loop():
  global mqtt_client, http_req, rgb, msg
  rgb.fill_color(0x6600cc)
  mqtt_client.wait_msg()


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
