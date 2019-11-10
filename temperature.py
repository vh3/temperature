# temperature.py
# A script intended to read temperature information from DS18B20 temperature sensors.
#
#  8 Nov 2019, vh, starter from Adafruit lesson here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
# 10 Nov 2019, vh, added functions for multiple sensors, formatted output for graphing

import glob
import time
from datetime import datetime
import os.path
import csv

# Set the number of seconds to pause after each reading.
# Note that we don't control the total amount of time it takes
# to do an iteration of the loop - the operating system manages this. 
delay_between_readings = 1.0

# set the max length of time we will record data, in seconds
max_time = 10

# Find the filename associated with the for the first temperature sensor device
path = '/sys/bus/w1/devices/'

# get the names of all the DS18B20 devices (they start with the prefix "28")
# count the number of devices

device_counter = 1
device_paths = []
device_ids = []
for dev in glob.glob(path + '28*'):
    identifier = os.path.split(dev)[1]
    device_file = dev + '/w1_slave'
    print (f'({device_counter}) DS18B20 sensor unique ID: {dev} ({identifier})')
    device_paths.append(device_file)
    device_ids.append(identifier)
    device_counter += 1

# Settings for a single device
device_folder = glob.glob(path + '28*')[0]
device_file = device_folder + '/w1_slave'

# initialize the time
# start_time = time.time()
start_time = time.time()
start_display = time.asctime()
print (f'Experiment started at: {start_display}')

# Define the output filename
filename_prefix = "Temperature_experiment_"
# Create a unique identifier based on the start time 'YYYYMMDDHHMMSS'
now = datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
# see https://www.guru99.com/date-time-and-datetime-classes-in-python.html
output_filename = filename_prefix + timestamp + '.csv'
print (f'Output data will be sent to file:{output_filename}')

# Write a header row to this file
header_row = ['time(s)']
for id in device_ids:
    column_header = 'Temp(C)-Sensor' + id[-4:]
    header_row.append(column_header)

print (f'Header row is:{header_row}')
with open(output_filename, "a") as fp:
    wr = csv.writer(fp, dialect='excel')

    # To do: this needs to be fixed.  We are parsing out every letter
    wr.writerow(f'Temperature collection starting at {start_display}')
    wr.writerow(header_row)

# Dump the contents of a given 1-wire device
def read_temp_raw(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Extract only the temperature from the 1-wire file contents
# the info we are looking somewhere in the file has a "t=" at the beginning of the line
def read_temp():
    lines = read_temp_raw(device_file)
    
    # We only want to use data where the CRC check is "YES" - meaning valid data was returned.  Keep checking the file repeatedly until a valid data record is read.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.001)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

# read all the sensors and return their values
def read_temp2(sensor_filelist):
    
    result_list = []

    # Iterate over each of the sensor filenames provided to this function, get a reading and append to result_list
    for filename in sensor_filelist:
        # print (f'name of the current sensorfilename={filename}')

        # Read the whole file
        lines = read_temp_raw(filename)

        # We only want to use data where the CRC check is "YES" - meaning valid data was returned.  Keep checking the file repeatedly until a valid data record is read.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.001)
            lines = read_temp_raw(filename)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = round(float(temp_string) / 1000.0, 1)
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            result_list.append(temp_c)

    return result_list        

# test out put new read_temp2function
# print (f'output={read_temp2(device_paths)}')

# Loop, reading temperature and writing to file until the max time is reached
elapsed_time = 0

# initialize a list to hold our data temporarily to hold our data
reading_data = []
while (elapsed_time <= max_time):
    elapsed_time = time.time() - start_time
    data = read_temp2(device_paths)
    data.insert(0,round(elapsed_time,0))
    reading_data.append(data)
    print(data)
    time.sleep(delay_between_readings)

# Write the reading_data to comma-delimited .csv file
with open(output_filename, "a") as fp:
    wr = csv.writer(fp, dialect='excel')
    wr.writerows(reading_data)
