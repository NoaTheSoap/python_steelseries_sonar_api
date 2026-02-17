from test import sonar

# Python Sonar Controller
A python library to control SteelSeries Sonar

## Description

This Python library allows you to control SteelSeries Sonar programmatically. With it, you can:

- Adjust volume for different channels (`master`, `game`, `chat`, `media`, `aux`)
- Mute or unmute channels
- Change input and output devices
- List active audio devices



## Installation

1. Clone the repository:

```bash
pip install git+https://github.com/your-username/python-sonar-controller.git
```

## Usage

### Initialization
The library automatically looks for `coreProps.json` in the default SteelSeries path.

```python
from py_steelseries_sonar import Sonar

# Initialize Sonar connection
sonar = Sonar()
```

### Volume & Muting
Volume values are floats between 0.0 and 1.0.

```python
# Set the Game channel volume to 50%
sonar.set_volume("game", 0.5)

# Mute the Media channel
sonar.mute_channel("media", True)

# Get the current volume for Chat
sonar.get_volume("media")
```

### Managing Devices
The library will list all active devices found by SteelSeries Sonar

```python
# List all active devices
sonar.devices.list_output_devices()
sonar.devices.list_input_devices()

# Get all active devices
devices = sonar.devices.get_output_devices()
devices = sonar.devices.get_input_devices()

# Set input device


# Getting device name and ID from first device found
devices = sonar.devices.get_output_devices()
print(devices[0]["name"])
print(devices[0]["id"])
```