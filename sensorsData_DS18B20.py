#!/usr/bin/env python3
# read temperature from sensor, store it in influx database.
# 
# https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
# sudo pip3 install w1thermsensor
# crontab */5 * * * *
# TODO back databse to disk each 24 horus

from influxdb import client as influxdb
import datetime
# ds18b20 sensor lib
from w1thermsensor import W1ThermSensor
# madrid server
from pyowm import OWM 
from secret import key
# cpu temperature
from gpiozero import CPUTemperature


#InfluxDB Connection Details
influxHost = 'localhost'
influxPort = '8086'
influxUser = 'temp'
influxPasswd = 'celsius'
influxdbName = 'temperature'

def main():
    # cpu temp
    cpu = CPUTemperature()  
    # sensor temp
    sensor = W1ThermSensor()
    temperature = sensor.get_temperature()
    # weather outside (madrid)
    owm = OWM(key)
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=40.5453765, lon=-3.69495776559637)
    one = one_call.current

    #print("The temperature is %s celsius" % temperature)
    influx_metric = [{
        'measurement': 'TemperatureSensor',
        'time': datetime.datetime.utcnow(),
        'fields': {
            'temperature': temperature,
            'temperatureOut': one.temperature('celsius')['temp'],
            'cpu_temperature': cpu.temperature,
       }
    }]

    #Saving data to InfluxDB
    try:
        db = influxdb.InfluxDBClient(influxHost, influxPort, influxUser, influxPasswd, influxdbName)
        db.write_points(influx_metric)
    except Exception as e:
        pritnt("Error", e.msg)
    db.close()

main()


