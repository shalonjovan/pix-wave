import numpy as np
import sounddevice as sd
import config

audio_buffer = np.zeros(config.FFT_SIZE)
window = np.hanning(config.FFT_SIZE)


def find_music_device():
    preferred_names = [
        "spotify",     
        "chromium",    
        "firefox",
    ]

    fallback_devices = []

    for i, dev in enumerate(sd.query_devices()):
        name = dev["name"].lower()
        if dev["max_input_channels"] > 0:
            for preferred in preferred_names:
                if preferred in name:
                    print(f"Using app stream: {dev['name']}")
                    return i
            fallback_devices.append((i, dev["name"]))

    for i, name in fallback_devices:
        if "pipewire" in name.lower() or "default" in name.lower():
            print(f"Using system audio: {name}")
            return i

    raise RuntimeError("No suitable audio input found.")


def audio_callback(indata, frames, time, status):
    global audio_buffer
    mono = np.mean(indata, axis=1)
    audio_buffer = np.roll(audio_buffer, -len(mono))
    audio_buffer[-len(mono):] = mono


def start_audio_stream():
    device_index = find_music_device()

    stream = sd.InputStream(
        device=device_index,
        channels=2,
        samplerate=config.SAMPLE_RATE,
        blocksize=512,
        callback=audio_callback
    )
    stream.start()
    return stream


def setup_frequency_bands():
    freqs = np.fft.rfftfreq(
        config.FFT_SIZE,
        1 / config.SAMPLE_RATE
    )[1:]  # drop DC

    band_edges = np.logspace(
        np.log10(config.LOW_FREQ),
        np.log10(config.HIGH_FREQ),
        config.NUM_BARS + 1
    )

    return freqs, band_edges


def compute_spectrum(freqs, band_edges):
    samples = audio_buffer * window
    fft = np.fft.rfft(samples)
    magnitudes = np.abs(fft)[1:]

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
