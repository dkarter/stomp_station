#!/usr/bin/env python3
import sys
import time

import serial


def restart_pico(device):
    ser = serial.Serial(device, 115200, timeout=3)
    time.sleep(1)
    ser.write(b"import machine\r\n")
    time.sleep(0.1)
    ser.write(b"machine.reset()\r\n")
    time.sleep(2)
    ser.close()
    print("Pico W restarted")


if __name__ == "__main__":
    device = sys.argv[1] if len(sys.argv) > 1 else "/dev/cu.usbmodem2101"
    restart_pico(device)
