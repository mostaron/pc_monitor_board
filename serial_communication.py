import time

import serial

global ser

ser: serial.Serial = None


def clear():
    global ser
    if ser is not None:
        ser.close()
    ser = None


def send(message):
    global ser
    if ser is None:
        ser = serial.Serial('COM4', 9600, timeout=5)
    ser.write(message.encode('utf-8'))
    time.sleep(2)


if __name__ == '__main__':
    while True:
        send('aaa,bbb,ccc,ddd,eee,fff,ggg,hhh,iii___')
