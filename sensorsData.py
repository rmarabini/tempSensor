#!/usr/bin/env python3
# read temperature from sensor, store it in influx database.
# 
# https://medium.com/trabe/monitoring-humidity-and-temperature-with-grafana-influxdb-and-orange-pi-9680046c70c
# crontab */5 * * * *
# TODO back databse to disk each 24 horus
from gpiozero import CPUTemperature
from influxdb import client as influxdb
import datetime

#InfluxDB Connection Details
influxHost = 'localhost'
influxPort = '8086'
influxUser = 'temp'
influxPasswd = 'celsius'
influxdbName = 'temperature'

def main():

    cpu = CPUTemperature()  
    influx_metric = [{
        'measurement': 'TemperatureSensor',
        'time': datetime.datetime.utcnow(),
        'fields': {
            'temperature': cpu.temperature,
            #'humidity': humidity
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


