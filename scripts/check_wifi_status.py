#!/usr/bin/env python3
import sys
import time

import serial


def check_wifi_status(device):
    ser = serial.Serial(device, 115200, timeout=3)
    time.sleep(1)
    ser.write(b"\x03")  # Ctrl+C to get to prompt
    time.sleep(1)
    ser.write(b"import network\r\n")
    time.sleep(0.1)
    ser.write(b"wlan = network.WLAN(network.STA_IF)\r\n")
    time.sleep(0.1)
    ser.write(b'print("Connected:", wlan.isconnected())\r\n')
    time.sleep(0.1)
    ser.write(b'if wlan.isconnected(): print("IP:", wlan.ifconfig()[0])\r\n')
    time.sleep(2)
    response = ser.read_all()
    print(response.decode("utf-8", errors="ignore"))
    ser.close()


if __name__ == "__main__":
    device = sys.argv[1] if len(sys.argv) > 1 else "/dev/cu.usbmodem2101"
    check_wifi_status(device)
