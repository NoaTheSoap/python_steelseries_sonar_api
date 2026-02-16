from sonar import Sonar



sonar = Sonar()

#sonar.list_input_devices()
#sonar.set_output_device("media","{0.0.0.00000000}.{9411a678-de6a-4b28-acd4-5c7adb8c56c4}")
#sonar.set_input_device("{.0.1.00000000}.{8f3ab922-edc6-4116-8135-da12c2a89deb}")
sonar.set_volume("media", 0.5)
#sonar.mute_channel("chat", False)
print(sonar.get_volume("media"))

#sonar.devices.list_output_devices()



