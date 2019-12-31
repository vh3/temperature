# temperature.py

A science fair project tool for collecting temperature vs. time data from multiple DS18B20 sensors.  We immersed ours in cooling liquids, boiling liquids, the house hot air vents, fridges, freezers our armpits and outside the house and watched the temperature change over time.  You set the length of the experiment, so it can run for as long as you want.

We added a twist: the robot will email you the temperature data when the experiment is ended if you wish.  We use this site as a reference: https://realpython.com/python-send-email/.  It also includes instructions for setting up a gmail account especially for this purpose.

Hardware: Raspberry Pi 3 + waterproof DS18B20 temperature probes + 1 non-waterproof sensor for capture of the ambient temperature.  You can set up as many sensors as you want.  They all use the same single GPIO pin to connect.

Software:  python.

We used an Adafruit tutorial to set up the hardware.  These sensors are very simple to set up, and are easy to use - On Linux, their output is written to text files.  All we need to do is parse the files when we want to take a reading.  https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf
