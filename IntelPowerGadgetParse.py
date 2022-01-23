import os
import csv
import time

global frequency
global power
global temperature
global loop


def read_info():
    global frequency
    global power
    global temperature
    p = os.popen("/Applications/Intel\\ Power\\ Gadget/PowerLog -duration 1 -resolution 1000 -file intel.csv")
    p.close()
    f = open("intel.csv")
    with f:
        reader = csv.DictReader(f)
        reader.__next__()
        row = reader.__next__()
        frequency = int(row['CPU Frequency_0(MHz)'])
        power = float(row['Processor Power_0(Watt)'])
        temperature = float(row['Package Temperature_0(C)'])
    f.close()
    return frequency, power, temperature


def start_read():
    global loop
    loop = True
    global frequency
    global power
    global temperature
    frequency = 0
    power = 0
    temperature = 0
    while loop:
        read_info()
        time.sleep(1)

