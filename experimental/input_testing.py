import sounddevice as sd

devices = sd.query_devices()
for i, dev in enumerate(devices):
    print(f"{i:2d} | {dev['name']} | inputs={dev['max_input_channels']}")
