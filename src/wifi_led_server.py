import socket
import time

import machine
import network

# WiFi credentials injected from 1Password
WIFI_SSID = "op://Private/Home IoT Wifi/base station name"
WIFI_PASS = "op://Private/Home IoT Wifi/base station password"

led = machine.Pin(15, machine.Pin.OUT)
led_state = False


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".")

        if wlan.isconnected():
            print("WiFi connected!")
            print("IP address:", wlan.ifconfig()[0])
            return wlan.ifconfig()[0]
        else:
            print("WiFi connection failed")
            return None
    else:
        print("Already connected to WiFi")
        return wlan.ifconfig()[0]


def web_page():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Pico W LED Control</title>
    <style>
        body { font-family: Arial; text-align: center; margin: 50px; }
        .button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        .off { background-color: #f44336; }
        .button:disabled { opacity: 0.5; cursor: not-allowed; }
        #status { font-weight: bold; font-size: 18px; }
    </style>
</head>
<body>
    <h1>Pico W LED Control</h1>
    <p>LED Status: <span id="status">%s</span></p>
    <p>
        <button class="button" onclick="sendCommand('toggle')">Toggle LED</button>
        <button class="button" onclick="sendCommand('on')">Turn ON</button>
        <button class="button off" onclick="sendCommand('off')">Turn OFF</button>
    </p>

    <script>
        async function sendCommand(cmd) {
            const buttons = document.querySelectorAll('button');
            buttons.forEach(b => b.disabled = true);

            try {
                const response = await fetch('/' + cmd);
                const data = await response.json();
                document.getElementById('status').textContent = data.status.toUpperCase();
            } catch (error) {
                console.error('Error:', error);
                alert('Command failed');
            } finally {
                buttons.forEach(b => b.disabled = false);
            }
        }
    </script>
</body>
</html>
""" % (
        "ON" if led_state else "OFF"
    )
    return html


def start_server(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 80))
    s.listen(5)

    print(f"HTTP server running on http://{ip}")
    print("Available endpoints:")
    print("  GET /         - Web interface")
    print("  GET /toggle   - Toggle LED state")
    print("  GET /on       - Turn LED on")
    print("  GET /off      - Turn LED off")

    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(1024).decode()

            if request:
                request_line = request.split("\n")[0]
                print("Request:", request_line)

                global led_state

                if "GET /toggle" in request:
                    led_state = not led_state
                    if led_state:
                        led.on()
                    else:
                        led.off()
                    response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"status": "%s"}' % (
                        "on" if led_state else "off"
                    )

                elif "GET /on" in request:
                    led_state = True
                    led.on()
                    response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"status": "on"}'

                elif "GET /off" in request:
                    led_state = False
                    led.off()
                    response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"status": "off"}'

                else:
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page()

                conn.send(response.encode())

            conn.close()

        except Exception as e:
            print("Error:", e)
            conn.close()


# Main execution
print("Starting WiFi LED server...")
ip = connect_wifi()

if ip:
    start_server(ip)
else:
    print("Could not connect to WiFi. Check credentials.")
