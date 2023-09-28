import os, sys, io
import M5
from M5 import *
from hardware import *
import time
from unit import *
import sht30
import qmp6988


i2c0 = None
env3_0 = None
sht = None
qmp = None


rawTemp = None


def setup():
  global i2c0, env3_0, rawTemp, sht, qmp

  M5.begin()
  i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
  sht = sht30.SHT30(i2c0)
  qmp = qmp6988.QMP6988(i2c0)


def loop():
  global i2c0, env3_0, rawTemp, sht, qmp
  M5.update()
  temperature, pressure = qmp.measure()
  pressure = pressure / 100
  temperature2, humidity = sht.measure()
  converted = (temperature * 1.8) + 32
  print(converted)
  time.sleep(3)


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
