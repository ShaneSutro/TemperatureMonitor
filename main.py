import os, sys, io
import M5
from M5 import *
from hardware import *
import time
from unit import *
import sht30
import qmp6988
from umqtt import *


i2c0 = None
sht = None
qmp = None
mqtt_client = None


def getTempAndPressure():
  global qmp
  temperature, pressure = qmp.measure()
  pressure = pressure / 100
  converted = (temperature * 1.8) + 32
  return converted, pressure

def publishMessage(message):
  mqtt_client.publish('/shane/steve/weather/temp', message, qos=0)

def setup():
  global i2c0, sht, qmp, mqtt_client
  M5.begin()
  i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
  qmp = qmp6988.QMP6988(i2c0)
  mqtt_client = MQTTClient('Temp Send', 'broker.mqtt.cool', port=1883, user='', password='', keepalive=0)
  mqtt_client.connect(clean_session=True)


def loop():
  global i2c0, sht, qmp
  M5.update()
  converted = getTempAndPressure();
  publishMessage(str(converted))
  time.sleep(5)


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
