from src.py_steelseries_sonar.sonar import Sonar
from src.py_steelseries_sonar.sonar_devices import SonarDevices

channel = "media"

output_device = ""
input_device = "{0.0.1.00000000}.{715e2dd1-9656-4c68-8114-fff9d1d9727b}"

sonar = Sonar()
def test():
    print("List Input devices")
    sonar.devices.list_input_devices()
    print("List Output devices")
    sonar.devices.list_output_devices()

    print("Muting channels")
    sonar.mute_channel(channel, False)

    print("Set volume")
    sonar.set_volume(channel, 1)

    print("Get volume")
    sonar.get_volume(channel)

def change_devices():
    print("Set input device")
    sonar.set_input_device(input_device)

    print("Set output device")
    sonar.set_output_device(output_device)


if __name__ == '__main__':
    test()
    change_devices()
