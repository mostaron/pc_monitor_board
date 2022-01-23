from concurrent.futures import ThreadPoolExecutor

import psutil
import os
import time

import IntelPowerGadgetParse


global frequency
global power
global temperature


def cpu_name():
    p = os.popen("sysctl machdep.cpu.brand_string")
    name = p.read().replace('\n', '').replace('machdep.cpu.brand_string: ', '')
    return "CPU: {}".format(name)


def cpu_usage():
    return "CPU Usage: \t\t{}%".format(psutil.cpu_percent())


def mem_usage():
    return "Memory Usage: \t{}%".format(psutil.virtual_memory().percent)


def mem_total():
    mem = psutil.virtual_memory().total / 1024 / 1024 / 1024
    return "Memory Total: \t{}GB".format(mem)


def disk_usage():
    return "Disk Usage: \t{}%".format(psutil.disk_usage("/").percent)


def disk_total():
    disk = round(psutil.disk_usage("/").total / 1000 / 1000 / 1000)
    return "Disk Total: \t{}GB".format(disk)


def update_cpu_power():
    global frequency
    global power
    global temperature
    (frequency, power, temperature) = IntelPowerGadgetParse.read_info()


def cpu_frequency():
    return "CPU Frequency: \t{}MHz".format(IntelPowerGadgetParse.frequency)


def cpu_power():
    return "CPU Power: \t\t{}Watts".format(IntelPowerGadgetParse.power)


def cpu_temperature():
    return "CPU Temperature: \t{}℃".format(IntelPowerGadgetParse.temperature)


if __name__ == '__main__':

    pool = ThreadPoolExecutor(max_workers=2)
    t = pool.submit(IntelPowerGadgetParse.start_read)
    try:
        while True:
            # time.sleep(1)
            print(cpu_name())
            print(cpu_usage())
            print(mem_usage())
            print(mem_total())
            print(disk_usage())
            print(disk_total())
            # update_cpu_power()
            print(cpu_frequency())
            print(cpu_power())
            print(cpu_temperature())
            time.sleep(2)
    finally:
        pool.shutdown()


