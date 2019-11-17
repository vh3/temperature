# temperature.py
# A script intended to read temperature information from a set of DS18B20 temperature sensors
# and send to a comma-delimited file

# 08 Nov 2019, vh3, starter from Adafruit lesson here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
# 10 Nov 2019, vh3, added functions for multiple sensors, formatted output for graphing
# 14 Nov 2019, vh3, added email support after: https://realpython.com/python-send-email/
# 17 Nov 2019, vh3, moved email function to a seperate file

# setup - this script was developed on a Raspberry PI 3+ running Raspian Linux.
# setup - sensor connection for the digital DS18B20 temperature sensors is super easy.
# setup - sensors were connected according to adafruit instructions: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

import glob
import time
from datetime import datetime
import os.path
import csv

# Optional: Do we want to email the output file somewhere?
# If you want to use the email functionality, you will need to set up and email account for your robot.
# Instructions for this are available here: https://realpython.com/python-send-email/
email_result = 0
email_destination = "adestination@adomain.com"

# Set the number of seconds to pause after each reading.
# Note that we don't control the total amount of time it takes
# to do an iteration of the loop - the operating system manages this. 
delay_between_readings = 1.0

# set the max length of time we will record data, in seconds
max_time = 5.0

# For certain long-running data collection activities, we may want to write the data
# one reading at a time in case there is some power failure or other stoppage in data collection before it is complete.
write_immediate = 0
if delay_between_readings >= 30.0 and max_time >= 600.0:
    write_immediate = 1

# Find the output filenames associated with the temperature sensor devices.
# The temperature sensors are "Dallas 1-wire protocol" devices, whose outputs are found here:
path = '/sys/bus/w1/devices/'

# get the names of all the DS18B20 devices (they start with the prefix "28")
# count the number of devices

device_counter = 0
# Initialize empty list to hold the path names for each device
device_paths = []
# Initialize an empty list to hold the unique identifier for each device
device_ids = []

# Create a list of paths we can iterate over when we want to read all the individual sensors later 
for dev in glob.glob(path + '28*'):

    identifier = os.path.split(dev)[1]
    device_counter += 1
    device_file = dev + '/w1_slave'
    print (f'({device_counter}) DS18B20 sensor unique ID: {dev} ({identifier})')
    device_paths.append(device_file)
    device_ids.append(identifier)

# Settings for the first device
# device_folder = glob.glob(path + '28*')[0]
# device_file = device_folder + '/w1_slave'

# initialize the time.  ToDo: figure out the types and use only a single reference variable to format the display
start_time = time.time()
start_display = time.asctime()
print (f'Experiment started at: {start_display}')
now = datetime.now()
# Create a unique identifier based on the start time 'YYYYMMDDHHMMSS'
# For formatting key, see https://www.guru99.com/date-time-and-datetime-classes-in-python.html
timestamp = now.strftime("%Y%m%d%H%M%S")

# Define the output filename
filename_prefix = "Temperature_experiment_"
output_filename = filename_prefix + timestamp + '.csv'
print (f'Output data will be sent to file:{output_filename}')

# Assemble and write a header row to this file
header_row = ['time(s)']
for id in device_ids:

    # Abbreviate the sensor unique identifiers to their last 4 digits for display in the output file.
    column_header = 'Temp(C)-Sensor' + id[-4:]
    header_row.append(column_header)

print (f'Header row is:{header_row}')
# Write title row and header row to the output data file in 'append' mode.
with open(output_filename, "a") as fp:
    wr = csv.writer(fp, dialect='excel')
    # Make the row a list with a single element - the .writerow() function demands an iterable object and will treat every letter as a seperate data item if we don't. 
    title = [f'Temperature collection experiment starting at {start_display}']
    websource= ['Code available at:','https://github.com/vh3/temperature']
    wr.writerow(title)
    wr.writerow(websource)
    wr.writerow(header_row)

# Read the entire contents of a given 1-wire device data file
def read_temp_raw(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Read all the sensors and return their values
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

# Start a timer
elapsed_time = 0

# initialize a list to hold our data temporarily.  Each element of reading_data will become a row in our output data file
reading_data = []

# Loop, reading temperature and writing to file until the max time is reached
while (elapsed_time <= max_time):
    elapsed_time = time.time() - start_time
    data = read_temp2(device_paths)
    data.insert(0,round(elapsed_time,0))
    print(data)
    reading_data.append(data)

    # If we are going to write results to file immediately
    if write_immediate == 1:
        # Write the reading_data to comma-delimited .csv file and clear the reading_data variable
        with open(output_filename, "a") as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerows(reading_data)
            reading_data = []

    time.sleep(delay_between_readings)

# Write the reading_data to comma-delimited .csv file
# This will only be meaningful where write_immediate = 0 (otherwise, we have been writing every record as it was read)
with open(output_filename, "a") as fp:
    wr = csv.writer(fp, dialect='excel')
    wr.writerows(reading_data)

# If we asked to send an email with the results, do it now.
if email_result == 1:
    from robot_send import send_email
    print (f'Attempting to email the output file ({output_filename}) to {email_destination}.')
    send_email(email_destination, output_filename, timestamp)
    print ('Done.')
