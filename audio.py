import numpy as np
import sounddevice as sd
import config

# ================= AUDIO BUFFER =================
audio_buffer = np.zeros(config.FFT_SIZE)
window = np.hanning(config.FFT_SIZE)


def find_music_device():
    preferred_names = [
        "spotify",     
        "chromium",    
        "firefox",
    ]

    preferred_apps = ["spotify", "chromium", "firefox"]
    monitor_keywords = ["monitor", "pipewire"]
    fallback_keywords = ["default", "sysdefault"]

    inputs = []

    for i, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] <= 0:
            continue

        name = dev["name"]
        lname = name.lower()
        inputs.append((i, name, lname))

        # per-app streams
        for app in preferred_apps:
            if app in lname:
                print(f"Using app audio: {name}")
                return i

    # output monitor / loopback
    for i, name, lname in inputs:
        for kw in monitor_keywords:
            if kw in lname:
                print(f"Using output monitor: {name}")
                return i

    for i, name in fallback_devices:
        if "pipewire" in name.lower() or "default" in name.lower():
            print(f"Using system audio: {name}")
            return i

    raise RuntimeError("No usable audio input found.")


# ================= AUDIO CALLBACK =================
def audio_callback(indata, frames, time, status):
    global audio_buffer

    # Convert stereo → mono
    mono = np.mean(indata, axis=1)

    # Rolling buffer
    audio_buffer = np.roll(audio_buffer, -len(mono))
    audio_buffer[-len(mono):] = mono


# ================= STREAM CONTROL =================
def start_audio_stream():
    device_index = find_audio_device()

    stream = sd.InputStream(
        device=device_index,
        channels=2,
        samplerate=config.SAMPLE_RATE,
        blocksize=512,
        callback=audio_callback,
    )

    stream.start()
    return stream


# ================= FFT SETUP =================
def setup_frequency_bands():
    freqs = np.fft.rfftfreq(
        config.FFT_SIZE,
        1 / config.SAMPLE_RATE
    )[1:]  # drop DC bin

    band_edges = np.logspace(
        np.log10(config.LOW_FREQ),
        np.log10(config.HIGH_FREQ),
        config.NUM_BARS + 1
    )

    return freqs, band_edges


# ================= SPECTRUM =================
def compute_spectrum(freqs, band_edges):
    samples = audio_buffer * window
    fft = np.fft.rfft(samples)
    magnitudes = np.abs(fft)[1:]  # drop DC

    levels = np.zeros(config.NUM_BARS)

    for i in range(config.NUM_BARS):
        idx = np.where(
            (freqs >= band_edges[i]) &
            (freqs < band_edges[i + 1])
        )[0]

        if len(idx) > 0:
            levels[i] = np.mean(magnitudes[idx])

    levels = np.log10(levels + 1)
    levels *= config.GAIN

    return np.clip(levels, 0, 1)
