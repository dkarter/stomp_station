#!/usr/bin/env python3
import signal
import sys
import time

import serial


def signal_handler(sig, frame):
    print("\nStopping monitor...")
    sys.exit(0)


def monitor_serial(device):
    signal.signal(signal.SIGINT, signal_handler)

    ser = serial.Serial(device, 115200, timeout=1)
    time.sleep(1)

    print(f"Monitoring serial output from {device} (Ctrl+C to stop)...")

    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            output = data.decode("utf-8", errors="ignore")
            if output.strip():
                print(output, end="")
        time.sleep(0.1)


if __name__ == "__main__":
    device = sys.argv[1] if len(sys.argv) > 1 else "/dev/cu.usbmodem2101"
    monitor_serial(device)
