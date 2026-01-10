import sounddevice as sd
import numpy as np

SAMPLE_RATE = 48000
FFT_SIZE = 1024

# --- find Spotify device ---
DEVICE_INDEX = None
for i, dev in enumerate(sd.query_devices()):
    if "spotify" in dev["name"].lower() and dev["max_input_channels"] > 0:
        DEVICE_INDEX = i
        print("Using Spotify stream:", dev["name"])
        break

if DEVICE_INDEX is None:
    raise RuntimeError("Spotify stream not found. Play a song first.")

# --- FFT window ---
window = np.hanning(FFT_SIZE)

def callback(indata, frames, time, status):
    # stereo → mono
    mono = np.mean(indata, axis=1)

    if len(mono) < FFT_SIZE:
        return

    # take last FFT_SIZE samples
    samples = mono[-FFT_SIZE:] * window

    # FFT
    fft = np.fft.rfft(samples)
    magnitudes = np.abs(fft)

    # frequency bins
    freqs = np.fft.rfftfreq(FFT_SIZE, 1 / SAMPLE_RATE)

    print("\n--- Spectrum snapshot ---")
    for f, amp in zip(freqs[:20], magnitudes[:20]):  # print only first 20 bins
        print(f"{f:6.1f} Hz -> {amp:.5f}")

with sd.InputStream(
    device=DEVICE_INDEX,
    channels=2,
    samplerate=SAMPLE_RATE,
    blocksize=FFT_SIZE,
    callback=callback
):
    print("Analyzing Spotify frequencies...")
    input("Press Enter to stop\n")
