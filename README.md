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
pip install git+https://github.com/NoaTheSoap/python_steelseries_sonar_api
```

## Usage

### Initialization
The library automatically looks for `coreProps.json` in the default SteelSeries path.

```python
from py_steelseries_sonar import Sonar

# Initialize Sonar connection
sonar = Sonar()

# Override corePros.json directory
sonar = Sonar("My\\Sonar\\Directory\\coreProps.json")
```

### Volume & Muting
Volume values are floats between 0.0 and 1.0.<br>
Channels: `master`, `game`, `chat`, `media`, `aux`
```python
# Set the Game channel volume to 50%
sonar.set_volume("game", 0.5)

# Mute the Media channel
sonar.mute_channel("media", True)

# Get the current volume for Chat
sonar.get_volume("chat")
```

### Managing Devices
Setting output device requires `channel` to change the output device for and `deviceID`<br>
Channels: `game`, `chat`, `media`, `aux`

```python
# List all active devices
sonar.devices.list_output_devices()
sonar.devices.list_input_devices()

# Get all active devices
devices = sonar.devices.get_output_devices()
devices = sonar.devices.get_input_devices()

# Set input device
sonar.set_input_device("{0.0.1.00000000}.{0875f144-5e02-4526-8fc2-223f9b4878ca}")

# Set output device
sonar.set_output_device("game", "{0.0.1.00000000}.{0875f144-5e02-4526-8fc2-223f9b4878ca}")

# Getting device name and ID from the first output device found
devices = sonar.devices.get_output_devices()
print(devices[0]["name"])
print(devices[0]["id"])

# Set output to first device found
sonar.set_output_device("game", devices[0]["id"])
```

