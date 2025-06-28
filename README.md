<p align="center">
  <img src="./images/logo.png" width="200" alt="logo">
</p>

# StompStation

A wireless foot switch using Raspberry Pi Pico W that can control music/video playback on macOS by sending keystrokes wirelessly.

## Features

- WiFi-enabled foot switch using Pico W
- Auto-start webserver on power-up with retry logic
- REST API for LED control
- Web interface for testing
- Modular firmware architecture
- Secure credential management with 1Password
- Development tools and automation

## Quick Start

1. **Install dependencies:**

   ```bash
   task setup
   ```

1. **Deploy to Pico W:**

   ```bash
   task fw:deploy
   ```

1. **Monitor output:**
   ```bash
   task fw:monitor
   ```

## Available Tasks

- `task setup` - Install project dependencies
- `task fw:deploy` - Deploy entire src directory to Pico W (with secret injection)
- `task fw:restart` - Restart the Pico W firmware
- `task fw:monitor` - Monitor serial output
- `task fw:status` - Check WiFi connection status
- `task fw:ls` - List files on Pico W
- `task fw:shell` - Open rshell to Pico W
- `task fw:repl` - Connect to Pico W REPL
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
├── src/                     # Pico W source files
│   ├── main.py              # Main entry point (auto-runs on boot)
│   ├── boot.py              # Boot sequence with hardware initialization
│   ├── config.py            # WiFi credentials (1Password secrets injected)
│   ├── wifi_manager.py      # WiFi connection with retry logic
│   └── wifi_led_server.py   # HTTP server and LED control
├── scripts/                 # Development scripts
│   ├── restart_pico.py      # Restart Pico W
│   ├── monitor_serial.py    # Serial monitor
│   └── check_wifi_status.py # WiFi status check
├── taskfiles/               # Task automation
│   └── fw.yml               # Firmware deployment tasks
└── Taskfile.dist.yml        # Main build automation
```

## Firmware Architecture

The firmware now uses a modular architecture for better maintainability:

- **`boot.py`** - Runs first, handles hardware stabilization
- **`main.py`** - Entry point that imports and starts the server
- **`wifi_manager.py`** - Robust WiFi connection with 3 retry attempts
- **`wifi_led_server.py`** - HTTP server providing REST API and web interface
- **`config.py`** - Configuration with secure credential injection

## Development

The project uses modern Python tooling:

- **Black** - Code formatting
- **isort** - Import sorting
- **Ruff** - Fast linting
- **Task** - Build automation
- **1Password CLI** - Secure credential injection
