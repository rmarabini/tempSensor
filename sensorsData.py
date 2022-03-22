#!/usr/bin/env python3
# read temperature from sensor, store it in influx database.
# 
# https://medium.com/trabe/monitoring-humidity-and-temperature-with-grafana-influxdb-and-orange-pi-9680046c70c
# crontab */5 * * * *
# TODO back databse to disk each 24 horus
from gpiozero import CPUTemperature
from influxdb import client as influxdb
import datetime
import sys
import Adafruit_DHT
from pyowm import OWM 
from secret import key

#InfluxDB Connection Details
influxHost = 'localhost'
influxPort = '8086'
influxUser = 'temp'
influxPasswd = 'celsius'
influxdbName = 'temperature'
gpio = 4

def main():
 
    # cpu temp
    cpu = CPUTemperature()  
    
    #for DHT22
    sensor = 22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    
    # weather outside (madrid)
    owm = OWM(key)
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=40.5453765, lon=-3.69495776559637)
    one = one_call.current
       
    influx_metric = [{
        'measurement': 'TemperatureSensor',
        'time': datetime.datetime.utcnow(),
        'fields': {
            'temperature': temperature,
            'humidity': humidity,
            'temperatureOut': one.temperature('celsius')['temp'],
            'temperatureOutFeelsLike': one.temperature('celsius')['feels_like'],
            'humidityOut': one.humidity,
            'cpu_temperature': cpu.temperature
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


