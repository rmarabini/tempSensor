#!/bin/bash
_dow="$(date +'%A')"
_log="influx_${_dow}.log"
influxd backup -portable -database temperature -host localhost:8088 /home/pi/influxbackup/${_log}
rsync -va /home/pi/influxbackup admin@boyle:/share/ZFS18_DATA/backup/celsius/.
