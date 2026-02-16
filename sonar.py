import os
import requests
import json
import logging
from sonar_devices import SonarDevices

class Sonar:
    channel_names = ["Master", "game", "chat", "media", "aux"]

    CHANNEL_MAPPING = {
        "master": "Master",
        "game": "game",
        "chat": "chatRender",
        "media": "media",
        "aux": "aux"
    }

    def __init__(self, core_props_path = None):
        requests.packages.urllib3.disable_warnings()

        # If coreProps.json is not overridden use standard path
        if core_props_path is None:
            core_props_path = os.path.join(os.environ['ProgramData'], 'SteelSeries', 'SteelSeries Engine 3','coreProps.json')

        self.core_props_path = core_props_path

        self.base_port = None
        self.sonar_port = None

        self.get_base_port()
        self.get_sonar_port()

        if self.sonar_port:
            self.devices = SonarDevices(self.sonar_port)

    def get_base_port(self):
        # Use ggEncryptedAddress: C:\ProgramData\SteelSeries\SteelSeries Engine 3\coreProps.json
        try:
            with open(self.core_props_path, "r") as core_props_file:
                core_props = json.loads(core_props_file.read())
                self.base_port = core_props['ggEncryptedAddress']
        except FileNotFoundError:
            logging.error("coreProps.json not found at: %s", self.core_props_path)

    def get_sonar_port(self):
        data = requests.get("https://"+self.base_port+ "/subApps", verify=False)
        data_json = json.loads(data.text)["subApps"]["sonar"]

        if not data_json["isEnabled"]:
            logging.warning("Sonar not enabled")
            return False

        if not data_json["isReady"]:
            logging.warning("Sonar not ready")
            return False

        if not data_json["isRunning"]:
            logging.warning("Sonar not running")
            return False

        self.sonar_port = data_json["metadata"]["webServerAddress"]
        if not self.sonar_port:
            logging.error("WebServer not found")
            return False

        return True


    # Volume: Value between 0 and 1.
    def set_volume(self, channel, volume:float):
        channel_key = self.CHANNEL_MAPPING.get(channel)
        if not channel_key:
            logging.warning("Invalid channel: %s", channel)
            return False

        if volume < 0 or volume > 1:
            logging.warning("Volume must be between 0 and 1 %s", volume)
            return False

        url = f"{self.sonar_port}/volumeSettings/classic/{channel_key}/Volume/{str(volume)}"
        requests.put(url)
        return True

    def mute_channel(self, channel, mute:bool):
        if not channel in self.channel_names:
            logging.warning("Invalid channel: %s", channel)

        if channel == "chat":
            channel = "chatRender"

        url = f"{self.sonar_port}/volumeSettings/classic/{channel}/Mute/{str(mute).lower()}"
        requests.put(url)

    def set_output_device(self, channel ,device_id):
        channel_key = self.CHANNEL_MAPPING.get(channel)
        if not channel_key:
            logging.warning("Invalid channel: %s", channel)
            return False

        if channel_key == "chatRender":
            channel_key = "chat"
        url = f"{self.sonar_port}/classicRedirections/{channel_key}/deviceId/{device_id}"
        response = requests.put(url)

        if response.status_code != 200:
            logging.error("Could not set output device %s", device_id)
            return False
        return True

    def set_input_device(self, device_id:str):
        url = f"{self.sonar_port}/classicRedirections/mic/deviceId/{device_id}"
        response = requests.put(url)

        if response.status_code != 200:
            logging.error("Could not set input device %s", device_id)
            return False
        return True


    def post_changes(self, setting, old_value, new_value):
        payload = {
            "event": "Setting Changed",
            "properties":{
                "source": "slider",
                "setting": setting,
                "value_old": old_value,
                "value_new": new_value
            }
        }

        post = requests.post(f"{self.sonar_port}/analytics/track", json=payload)

    def get_volume(self, channel:str):
        channel_key = self.CHANNEL_MAPPING.get(channel)
        if not channel_key:
            logging.warning("Invalid channel: %s", channel)
            return None

        url = f"{self.sonar_port}/volumeSettings/classic"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()["devices"][channel_key]["classic"]["volume"]

