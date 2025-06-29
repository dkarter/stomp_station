import socket

import machine

led = machine.Pin(15, machine.Pin.OUT)
led_state = False


def load_html_template():
    try:
        with open("index.html") as f:
            return f.read()
    except OSError:
        return "<h1>Error: index.html not found</h1>"


def web_page():
    template = load_html_template()
    status = "ON" if led_state else "OFF"
    return template.replace("{status}", status)


def build_response(content, content_type="text/html", status_code=200):
    status_text = "OK" if status_code == 200 else "Error"
    return f"HTTP/1.1 {status_code} {status_text}\r\nContent-Type: {content_type}\r\n\r\n{content}"


def handle_toggle():
    global led_state
    led_state = not led_state
    if led_state:
        led.on()
    else:
        led.off()
    return '{"status": "%s"}' % ("on" if led_state else "off")


def handle_on():
    global led_state
    led_state = True
    led.on()
    return '{"status": "on"}'


def handle_off():
    global led_state
    led_state = False
    led.off()
    return '{"status": "off"}'


ROUTES = {
    "/toggle": {"handler": handle_toggle, "description": "Toggle LED state"},
    "/on": {"handler": handle_on, "description": "Turn LED on"},
    "/off": {"handler": handle_off, "description": "Turn LED off"},
}


def print_endpoints():
    print("Available endpoints:")
    print("  GET /         - Web interface")
    for path, route_info in ROUTES.items():
        print(f"  GET {path:<8} - {route_info['description']}")


def start_server(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(("", 80))
        s.listen(5)
    except OSError as e:
        print(f"Failed to start server: {e}")
        return

    print(f"HTTP server running on http://{ip}")
    print_endpoints()

    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(1024).decode()

            if request:
                request_line = request.split("\n")[0]
                print("Request:", request_line)

                path = request_line.split(" ")[1] if len(request_line.split(" ")) > 1 else "/"

                if path in ROUTES:
                    json_response = ROUTES[path]["handler"]()
                    response = build_response(json_response, "application/json")
                else:
                    response = build_response(web_page())

                conn.send(response.encode())

            conn.close()

        except Exception as e:
            print("Error:", e)
            conn.close()
