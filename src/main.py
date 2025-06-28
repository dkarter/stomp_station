# Main entry point for Pico W
from wifi_manager import connect_wifi
from wifi_led_server import start_server

print("Starting WiFi LED server...")
ip = connect_wifi()

if ip:
    start_server(ip)
else:
    print("Could not connect to WiFi. Check credentials.")