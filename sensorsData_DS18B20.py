#!/usr/bin/env python3
# read temperature from sensor, store it in influx database.
# 
# https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
# sudo pip3 install w1thermsensor
# crontab */5 * * * *
# TODO back databse to disk each 24 horus

from influxdb import client as influxdb
import datetime
from w1thermsensor import W1ThermSensor

#InfluxDB Connection Details
influxHost = 'localhost'
influxPort = '8086'
influxUser = 'temp'
influxPasswd = 'celsius'
influxdbName = 'temperature'

def main():
    sensor = W1ThermSensor()
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    influx_metric = [{
        'measurement': 'TemperatureSensor',
        'time': datetime.datetime.utcnow(),
        'fields': {
            'temperature': temperature,
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


