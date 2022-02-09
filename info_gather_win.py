import json

import psutil
import wmi
import os
import time
import GPUtil
import datetime

from serial import SerialException

import IntelPowerGadgetParse
import serial_communication
from model import PCInfo

global frequency
global power
global temperature
global pc_info


def gpu_usage():
    gpu = GPUtil.getGPUs()[0]
    pc_info.gpu_usage = round(gpu.load * 100, 2)
    return "GPU Usage:   {}%".format(gpu.load * 100)


def cpu_name():
    cpu = wmi.WMI().Win32_Processor()[0]
    pc_info.cpu_name = cpu.Name
    return "{}".format(cpu.Name)


def cpu_usage():
    pc_info.cpu_usage = round(psutil.cpu_percent(), 2)
    return "CPU Usage:   {}%".format(psutil.cpu_percent())


def mem_usage():
    pc_info.mem_usage = round(psutil.virtual_memory().percent, 2)
    return "Memory Usage:  {}%".format(psutil.virtual_memory().percent)


def mem_total():
    mem = psutil.virtual_memory().total / 1024 / 1024 / 1024
    pc_info.mem_total = round(mem, 2)
    return "Memory Total:  {:2f}GB".format(mem)


def disk_usage():
    pc_info.disk_usage = round(psutil.disk_usage("/").percent, 2)
    return "Disk Usage:  {}%".format(psutil.disk_usage("/").percent)


def disk_total():
    disk = round(psutil.disk_usage("/").total / 1000 / 1000 / 1000)
    pc_info.disk_total = round(disk, 2)
    return "Disk Total:  {}GB".format(disk)


def cpu_frequency():
    cpu = wmi.WMI().Win32_Processor()[0]
    pc_info.cpu_frequency = round(cpu.CurrentClockSpeed, 2)
    return "CPU Frequency:  {}MHz".format(cpu.CurrentClockSpeed)


def cpu_power():
    pc_info.cpu_power = round(0, 2)
    return "CPU Power:   {}Watts".format("0")


def cpu_temperature():
    pc_info.cpu_temperature = round(0, 2)
    return "CPU Temperature:  {}".format("0")


if __name__ == '__main__':
    pc_info = PCInfo()
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
        # gpu_usage()gpu_usage
        pc_info.date = datetime.datetime.now().strftime('%Y-%m-%d')
        pc_info.time = datetime.datetime.now().strftime('%H:%M')
        info = json.dumps(pc_info.__dict__)
        print(info)
        try:
            serial_communication.send(info+"___")
        except SerialException:
            serial_communication.clear()
            pass


