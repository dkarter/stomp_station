# Wireless Foot Switch

A wireless foot switch using Raspberry Pi Pico W that can control music/video playback on macOS by sending keystrokes wirelessly.

## Features

- WiFi-enabled foot switch using Pico W
- REST API for LED control
- Web interface for testing
- Secure credential management with 1Password
- Development tools and automation

## Quick Start

1. **Install dependencies:**
   ```bash
   task setup
   ```

2. **Set up WiFi credentials** (using 1Password):
   - Configure your `.envrc` file with 1Password secret references
   - Example: `export WIFI_SSID="$(op read 'op://Private/WiFi/SSID')"`

3. **Deploy to Pico W:**
   ```bash
   task fw:deploy
   ```

4. **Monitor output:**
   ```bash
   task fw:monitor
   ```

## Available Tasks

- `task setup` - Install project dependencies
- `task fw:deploy` - Deploy main script to Pico W
- `task fw:upload FILE=<file>` - Upload specific file to Pico W
- `task fw:monitor` - Monitor serial output
- `task fw:status` - Check WiFi connection status
- `task lint` - Run linting and formatting
- `task dev` - Full development workflow

## Hardware Setup

1. Connect LED to Pico W:
   - LED long leg → GP15
   - LED short leg → GND
   - (Resistor recommended but not required for testing)

2. Connect Pico W via USB

## Project Structure

```
foot_switch/
├── src/                 # Pico W source files
│   ├── wifi_led_server.py   # Main WiFi server
│   ├── blink.py            # LED blink test
│   └── main.py             # Backup main file
├── scripts/             # Development scripts
│   ├── restart_pico.py     # Restart Pico W
│   ├── monitor_serial.py   # Serial monitor
│   └── check_wifi_status.py # WiFi status check
└── Taskfile.dist.yml    # Build automation
```

## Development

The project uses modern Python tooling:
- **Black** - Code formatting
- **isort** - Import sorting  
- **Ruff** - Fast linting
- **Task** - Build automation
- **1Password** - Secure credential injection