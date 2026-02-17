from sonar import Sonar



sonar = Sonar()


#sonar.set_output_device("media","{0.0.0.00000000}.{9411a678-de6a-4b28-acd4-5c7adb8c56c4}")
sonar.set_input_device("{0.0.1.00000000}.{214e4883-a908-4190-9d1a-48be0f059d33}")
#sonar.set_volume("media", 0.5)
sonar.mute_channel("chat", True)
print(sonar.get_volume("media"))

sonar.devices.list_input_devices()



