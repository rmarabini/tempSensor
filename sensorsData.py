#!/usr/bin/env python3
# /home/pi/Sensors_Database/sensorsData.py
# collect rapberry pi3 temperature and plot it
# crontab */5 * * * *
from gpiozero import CPUTemperature

# connect to database
import sqlite3
import sys
from time import sleep

def main():
    # get temperature
    while True:
        cpu = CPUTemperature()  
        print("Temperature", cpu.temperature)
        sleep(5)
    # call the function to insert data
    #add_data (cpu.temperature, 0)


# function to insert data on a table
def add_data (temp, hum):
    # connect database
    conn=sqlite3.connect('/home/pi/Sensors_Database/sensorsData.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
    conn.commit()
    # close the database after use
    conn.close()


main()


