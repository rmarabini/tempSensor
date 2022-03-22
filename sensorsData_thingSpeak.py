#!/usr/bin/env python3
# read temperature from sensor, store it in influx database.
# 
# https://medium.com/trabe/monitoring-humidity-and-temperature-with-grafana-influxdb-and-orange-pi-9680046c70c
# crontab */5 * * * *
# TODO back databse to disk each 24 horus
from gpiozero import CPUTemperature
import datetime
import sys
import Adafruit_DHT
from pyowm import OWM 
import requests

gpio = 4

def main():
 
    # cpu temp
    cpu = CPUTemperature()  
    
    #for DHT22
    sensor = 22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    
    # weather outside (madrid)
    key = '867e5c1fe773aacf096e4ea37e3b773d'
    owm = OWM(key)
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=40.5453765, lon=-3.69495776559637)
    one = one_call.current
    queries = {"api_key": "TF07A965JW3O7ORO",
            'field1': temperature,
            'field2': humidity,
            'field3': one.temperature('celsius')['temp'],
            'field4': one.temperature('celsius')['feels_like'],
            'field5': one.humidity,
            'field6': cpu.temperature
        }


    r = requests.get('https://api.thingspeak.com/update', params=queries)
    if r.status_code == requests.codes.ok:
        print("Data Received!")
    else:
        print("Error Code: " + str(r.status_code))

main()


