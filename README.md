# temperature.py

A science fair project tool (we call it a robot) for collecting temperature vs. time data from multiple DS18B20 temperature sensors and writing the output to a comma-delimited file as well as to the command line.  We bought some waterproof-probe versions (similar to these:https://www.adafruit.com/product/381) and immersed them in ice water, boiling liquids, the house hot air vents, fridges, freezers, our armpits and outside the house to watch the temperature change over time.  You set the length of the experiment, so it can run for as long as you want.  For long-running experiments, the output is written to file after every observation so you will not lose the data you have collected if you lose power during the experiment.

Hardware: Raspberry Pi 3 + waterproof DS18B20 temperature probes (https://www.adafruit.com/product/381) + 1 non-waterproof sensor (https://www.adafruit.com/product/374) for capture of the ambient temperature.  You can set up as many sensors as you want.  They all use the same single GPIO pin (Pin 4) to connect and have hard-coded unique identifiers. This robot will find any that are attached and identify them by their last 4-digits in the output file.

Software:  python, a command line script.  We used the Thonny IDE that comes installed on the Raspberry Pi operating system for editing and running this script.

We used an Adafruit tutorial to set up the hardware.  These sensors are very simple to set up, and are easy to use - On Linux, their output is written to text files.  All we need to do is parse the files when we want to take a reading.  The tutorial we used can be found here: https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf.  You will need to use it to set up your sensors and a resistor on a breadboard, connect them to GPIO pin 4 on the Raspberry Pi and do some basic configuration of the Pi to enable the one-wire protocol.

We added a twist: If you wish, the robot will email you the temperature data as a single comma-delimited (.csv) file when the experiment has ended.  We used this site as a code reference: https://realpython.com/python-send-email/.  It also includes instructions for setting up a gmail account especially for this purpose.  You will have to edit the robot_send.py script with the sending account details.

@themakerfam
