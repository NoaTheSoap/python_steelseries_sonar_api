import requests
import json


class SonarDevices:
    def __init__(self, sonar_port):
        self.sonar_port = sonar_port

    # ----- Output ----- #

    # Returns list[dict[str, str]] of all active output devices available in Sonar
    def get_output_devices(self):
        filtered= [{"name": d["friendlyName"], "id": d["id"]}
                   for d in self.get_devices()
                   if d["dataFlow"] == "render"
                   and not d["isVad"]
                   and d["state"] == "active"]
        return filtered

    def list_output_devices(self):
        for device in self.get_output_devices():
            print(device["name"], device["id"])

    # ----- Input ----- #

    # Returns list[dict[str, str]] of all active input devices available in Sonar
    def get_input_devices(self):
        filtered= [{"name": d["friendlyName"], "id": d["id"]}
                   for d in self.get_devices()
                   if d["dataFlow"] == "capture"
                   and not d["isVad"]
                   and d["state"] == "active"]
        return filtered

    def list_input_devices(self):
        for device in self.get_input_devices():
            print(device["name"], device["id"])


    def get_devices(self):
        return requests.get(f"{self.sonar_port}/audioDevices").json()