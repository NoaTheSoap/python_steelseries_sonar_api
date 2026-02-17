from src.py_steelseries_sonar import Sonar


def main():
    try:
        # Initialize Sonar
        sonar = Sonar()
        print(sonar.sonar_port)
        print("Sonar initialized successfully!")

        # List available output devices
        print("\nOutput devices:")
        for device in sonar.devices.get_output_devices():
            print(device["name"], device["id"])

        # List available input devices
        print("\nInput devices:")
        for device in sonar.devices.get_input_devices():
            print(device["name"], device["id"])

        # Test setting volume
        print("\nTesting volume set/get:")
        sonar.set_volume("master", 0.5)
        print("Master volume set to 0.5")
        vol = sonar.get_volume("chat")
        print(f"Master volume read back: {vol}")

        # Test muting a channel
        print("\nTesting mute:")
        sonar.mute_channel("game", True)
        print("Game channel muted")
        sonar.mute_channel("game", False)
        print("Game channel unmuted")

        # Test changing output device (choose first device if available)
        output_devices = sonar.devices.get_output_devices()
        if output_devices:
            device_id = output_devices[0]["id"]
            sonar.set_output_device("game", device_id)
            print(f"Game output device set to {output_devices[0]['name']}")

        # Test changing input device (choose first device if available)
        input_devices = sonar.devices.get_input_devices()
        if input_devices:
            device_id = input_devices[0]["id"]
            sonar.set_input_device(device_id)
            print(f"Microphone input device set to {input_devices[0]['name']}")

        print("\nAll tests completed successfully!")

    except Exception as e:
        print("Test failed with exception:", e)


if __name__ == "__main__":
    main()
