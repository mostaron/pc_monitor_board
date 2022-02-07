import json
from concurrent.futures import ThreadPoolExecutor

import psutil
import os
import time

from GPUtil import GPUtil
from serial import SerialException

import IntelPowerGadgetParse
import serial_communication

global frequency
global power
global temperature
global pc_info


def gpu_usage():
    gpu = GPUtil.getGPUs()[0]
    pc_info.gpu_usage = round(gpu.load * 100, 2)
    return "GPU Usage:   {}%".format(gpu.load * 100)


def cpu_name():
    p = os.popen("sysctl machdep.cpu.brand_string")
    name = p.read().replace('\n', '').replace('machdep.cpu.brand_string: ', '')
    pc_info.cpu_name = name
    return "CPU: {}".format(name)


def cpu_usage():
    pc_info.cpu_usage = round(psutil.cpu_percent(), 2)
    return "CPU Usage: \t\t{}%".format(psutil.cpu_percent())


def mem_usage():
    pc_info.mem_usage = round(psutil.virtual_memory().percent, 2)
    return "Memory Usage: \t{}%".format(psutil.virtual_memory().percent)


def mem_total():
    mem = psutil.virtual_memory().total / 1024 / 1024 / 1024
    pc_info.mem_total = round(mem, 2)
    return "Memory Total: \t{}GB".format(mem)


def disk_usage():
    pc_info.disk_usage = round(psutil.disk_usage("/").percent, 2)
    return "Disk Usage: \t{}%".format(psutil.disk_usage("/").percent)


def disk_total():
    disk = round(psutil.disk_usage("/").total / 1000 / 1000 / 1000)
    pc_info.disk_total = round(disk, 2)
    return "Disk Total: \t{}GB".format(disk)


def update_cpu_power():
    global frequency
    global power
    global temperature
    (frequency, power, temperature) = IntelPowerGadgetParse.read_info()


def cpu_frequency():
    pc_info.cpu_frequency = IntelPowerGadgetParse.frequency
    return "CPU Frequency: \t{}MHz".format(IntelPowerGadgetParse.frequency)


def cpu_power():
    pc_info.cpu_power = IntelPowerGadgetParse.power
    return "CPU Power: \t\t{}Watts".format(IntelPowerGadgetParse.power)


def cpu_temperature():
    pc_info.cpu_temperature = IntelPowerGadgetParse.temperature
    return "CPU Temperature: \t{}℃".format(IntelPowerGadgetParse.temperature)


if __name__ == '__main__':

    pool = ThreadPoolExecutor(max_workers=2)
    t = pool.submit(IntelPowerGadgetParse.start_read)
    try:
        while True:
            cpu_name()
            cpu_usage()
            cpu_frequency()
            cpu_temperature()
            cpu_power()
            mem_total()
            mem_usage()
            disk_usage()
            disk_total()
            gpu_usage()
            info = json.dumps(pc_info.__dict__)
            print(info)
            try:
                serial_communication.send(info+"___")
            except SerialException:
                serial_communication.clear()
                pass
            time.sleep(2)
    finally:
        pool.shutdown()


