import sounddevice as sd
import numpy as np

DEVICE_INDEX = None

for i, dev in enumerate(sd.query_devices()):
    if "spotify" in dev["name"].lower() and dev["max_input_channels"] > 0:
        DEVICE_INDEX = i
        print("Using Spotify stream:", dev["name"])
        break

if DEVICE_INDEX is None:
    raise RuntimeError("Spotify stream not found. Make sure Spotify is playing audio.")

def callback(indata, frames, time, status):
    # Convert stereo → mono (important later)
    mono = np.mean(indata, axis=1)

    volume = np.linalg.norm(mono) / frames
    print(f"Spotify volume: {volume:.5f}")

with sd.InputStream(
    device=DEVICE_INDEX,
    channels=2,
    samplerate=48000,
    blocksize=1024,
    callback=callback,
):
    print("Listening to Spotify only...")
    input("Press Enter to stop\n")
