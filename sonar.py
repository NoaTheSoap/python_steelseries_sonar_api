import os
import requests
import json
import logging
from exceptions import *
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
        if not os.path.exists(self.core_props_path):
            raise CorePropsNotFoundError(self.core_props_path)
        with open(self.core_props_path, "r") as core_props_file:
            core_props = json.loads(core_props_file.read())
            self.base_port = core_props['ggEncryptedAddress']


    def get_sonar_port(self):
        data = requests.get("https://"+self.base_port+ "/subApps", verify=False)
        if data.status_code != 200:
            raise SonarConnectionError(self.base_port)
        data_json = json.loads(data.text)["subApps"]["sonar"]


        if not data_json["isEnabled"]:
            raise SonarNotEnabled()

        if not data_json["isReady"]:
            raise SonarNotReady()

        if not data_json["isRunning"]:
            raise SonarNotRunning()

        self.sonar_port = data_json["metadata"]["webServerAddress"]
        if not self.sonar_port:
            raise SonarConnectionError(self.sonar_port)



    # Volume: Value between 0 and 1.
    def set_volume(self, channel, volume:float):
        channel_key = self.CHANNEL_MAPPING.get(channel)
        if not channel_key:
            raise InvalidChannel(channel)
        if volume < 0 or volume > 1:
            raise InvalidVolume(volume)

        self._put(f"volumeSettings/classic/{channel_key}/Volume/{str(volume)}")

    def mute_channel(self, channel, mute:bool):
        if not channel in self.channel_names:
            raise InvalidChannel(channel)

        if channel == "chat":
            channel = "chatRender"

        self._put(f"volumeSettings/classic/{channel}/Mute/{str(mute).lower()}")


    def set_output_device(self, channel ,device_id):
        channel_key = self.CHANNEL_MAPPING.get(channel)
        if not channel_key:
            raise InvalidChannel(channel)

        if channel_key == "chatRender":
            channel_key = "chat"
        self._put(f"classicRedirections/{channel_key}/deviceId/{device_id}")


    def set_input_device(self, device_id:str):
        self._put(f"classicRedirections/mic/deviceId/{device_id}")


    def get_volume(self, channel:str):
        channel_key = self.CHANNEL_MAPPING.get(channel)
        if not channel_key:
            raise InvalidChannel(channel)

        return self._get("volumeSettings/classic")["devices"][channel_key]["classic"]["volume"]


    def _get(self, endpoint):
        try:
            response = requests.get(f"{self.sonar_port}/{endpoint}", timeout=2)
        except requests.exceptions.RequestException as e:
            raise SonarConnectionError(self.sonar_port) from e

        if not response.ok:
            raise SonarNotAccessible(response.status_code)
        return response.json()

    def _put(self, endpoint):
        try:
            response = requests.put(f"{self.sonar_port}/{endpoint}", timeout=2)
        except requests.exceptions.RequestException as e:
            raise SonarConnectionError(self.sonar_port) from e

        if not response.ok:
            raise SonarNotAccessible(response.status_code)
