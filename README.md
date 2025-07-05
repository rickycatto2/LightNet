# LightNet
A Smart Sequential Lighting Controller

A Python-based system for Raspberry Pi that controls Tasmota-enabled bulbs via MQTT. Lights are triggered by motion (PIR sensor) or a momentary button. Lights animate on in sequence and fade out after a set time. Configuration is available through a simple web-based control panel.

## Features

* Sequential lighting with customizable animation
* MQTT control of Tasmota bulbs (no cloud dependency)
* Local Flask control panel for configuration
* PIR or button trigger support
* Auto-starts on boot
* Designed for offline use with Raspberry Pi as Wi-Fi hotspot

## Hardware

* Raspberry Pi (tested on Pi 3 B)
* Athom Tasmota bulbs (pre-flashed)
* PIR sensor or momentary button (GPIO 17)
* Optional: Zigbee dongle + Aqara motion sensor (future work)

## Setup

### 1. MQTT Broker

Use `mosquitto` as the local MQTT broker on the Pi:

```bash
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
```

### 2. File Structure

```
/home/lightmeup/
├── autostart_controller.py  # Main script
├── control_panel.py         # Flask web interface
├── config.json              # Editable config values
```

### 3. Configuration File

`config.json` example:

```json
{
  "fade_time": 6,
  "color_temp": 6500,
  "off_delay": 60
}
```

### 4. Control Panel

Available on port 5000:

```
http://<raspberry_pi_ip>:5000
```

### 5. Autostart on Boot

Edit `crontab`:

```bash
crontab -e
```

Add:

```bash
@reboot python3 /home/lightmeup/autostart_controller.py &
```

### 6. Set Tasmota Topics

Ensure your bulbs are named and accessible via topics:

* Haze01 → 192.168.4.18
* Haze02 → 192.168.4.24
* Haze03 → 192.168.4.19

Topics used:

```
cmnd/light/Haze01/Backlog
cmnd/light/Haze02/Backlog
cmnd/light/Haze03/Backlog
```

### 7. Clear Tasmota Rules

In the Tasmota console:

```bash
Rule1 ""
Rule2 ""
Rule3 ""
Rule4 ""
Rule5 ""
SaveData
```

## Future Work

* Replace GPIO-based PIR with Zigbee motion sensor (via Zigbee2MQTT)
* Add a nicer frontend UI (React/Bootstrap)
* Multi-zone lighting effects

![57c801a9-3ea9-47c6-b9f4-4ded0792a160](https://github.com/user-attachments/assets/06c4df20-4726-45d3-9d1d-09d671efdec0)
