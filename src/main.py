import time

import machine

# Try pin 25 (onboard LED on Pico W)
led = machine.Pin(25, machine.Pin.OUT)

print("Starting LED blink...")
for i in range(10):
    print(f"Blink {i+1}")
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
print("Done blinking")
