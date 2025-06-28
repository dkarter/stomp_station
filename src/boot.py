# boot.py - Runs on every boot (including hard-reset)
import gc
import time
import machine

print("=== Pico W Boot Sequence Starting ===")

# Enable garbage collection
gc.collect()

# Allow hardware to stabilize after power-on
print("Stabilizing hardware...")
time.sleep(2)

# Initialize built-in LED for status indication
led = machine.Pin("LED", machine.Pin.OUT)
led.on()  # LED on during boot
time.sleep(0.5)
led.off()

print("=== Boot Sequence Complete ===")
print("Proceeding to main.py...")