import numpy as np
import sounddevice as sd
import config

audio_buffer = np.zeros(config.FFT_SIZE)
window = np.hanning(config.FFT_SIZE)


def find_spotify_device():
    for i, dev in enumerate(sd.query_devices()):
        if "spotify" in dev["name"].lower() and dev["max_input_channels"] > 0:
            print("Using Spotify stream:", dev["name"])
            return i
    raise RuntimeError("Spotify stream not found. Play a song first.")


def audio_callback(indata, frames, time, status):
    global audio_buffer
    mono = np.mean(indata, axis=1)
    audio_buffer = np.roll(audio_buffer, -len(mono))
    audio_buffer[-len(mono):] = mono


def start_audio_stream():
    device_index = find_spotify_device()

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

    # perceptual compression + fixed gain
    levels = np.log10(levels + 1)
    levels *= config.GAIN

    return np.clip(levels, 0, 1)
