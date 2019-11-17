# temperature

A science fair project tool intended to collect temperature & time data from multiple DS18B20 sensors immersed in cooling liquids.

Hardware: Raspberry Pi 3 + waterproof DS18B20 waterproof temperature probes + 1 non-waterproof sensor for capture of the ambient temperature.

Software:  python.

We used an Adafruit tutorial to set up the hardware.  These sensors are very simple to set up, and are easy to use - On Linux, their output is written to files.  All we need to do is parse the files when we want to take a reading.

https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf
