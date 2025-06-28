import time
import network
from config import WIFI_SSID, WIFI_PASS


def connect_wifi():
    """Connect to WiFi with retry logic for reliable startup"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        # Try multiple times with longer timeout for better reliability
        max_attempts = 3
        for attempt in range(max_attempts):
            print(f"WiFi connection attempt {attempt + 1}/{max_attempts}...")
            wlan.connect(WIFI_SSID, WIFI_PASS)

            # Wait longer for initial connection (especially important at boot)
            timeout = 20 if attempt == 0 else 15
            while not wlan.isconnected() and timeout > 0:
                time.sleep(1)
                timeout -= 1
                print(".", end="")

            print()  # New line after dots

            if wlan.isconnected():
                print("WiFi connected!")
                print("IP address:", wlan.ifconfig()[0])
                return wlan.ifconfig()[0]
            else:
                print(f"Attempt {attempt + 1} failed")
                if attempt < max_attempts - 1:
                    print("Retrying in 3 seconds...")
                    time.sleep(3)

        print("All WiFi connection attempts failed")
        return None
    else:
        print("Already connected to WiFi")
        return wlan.ifconfig()[0]