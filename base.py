import pygame
import numpy as np
import sounddevice as sd

# ================= AUDIO CONFIG =================
SAMPLE_RATE = 48000
FFT_SIZE = 1024
NUM_BARS = 64

# ================= FIND SPOTIFY =================
DEVICE_INDEX = None
for i, dev in enumerate(sd.query_devices()):
    if "spotify" in dev["name"].lower() and dev["max_input_channels"] > 0:
        DEVICE_INDEX = i
        print("Using Spotify stream:", dev["name"])
        break

if DEVICE_INDEX is None:
    raise RuntimeError("Spotify not found. Play a song first.")

# ================= AUDIO BUFFER =================
audio_buffer = np.zeros(FFT_SIZE)
window = np.hanning(FFT_SIZE)

def audio_callback(indata, frames, time, status):
    global audio_buffer
    mono = np.mean(indata, axis=1)

    audio_buffer = np.roll(audio_buffer, -len(mono))
    audio_buffer[-len(mono):] = mono

# ================= START AUDIO =================
stream = sd.InputStream(
    device=DEVICE_INDEX,
    channels=2,
    samplerate=SAMPLE_RATE,
    blocksize=256,
    callback=audio_callback,
)
stream.start()

# ================= PYGAME =================
pygame.init()
WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BAR_WIDTH = WIDTH // NUM_BARS

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- FFT -----
    samples = audio_buffer * window
    fft = np.fft.rfft(samples)
    magnitudes = np.abs(fft)

    # Group bins → bars
    bins = np.array_split(magnitudes, NUM_BARS)
    bar_values = np.array([np.mean(b) for b in bins])

    # Normalize
    bar_values /= np.max(bar_values) + 1e-6

    # ----- DRAW -----
    screen.fill((0, 0, 0))

    for i, value in enumerate(bar_values):
        bar_height = int(value * HEIGHT)
        x = i * BAR_WIDTH
        y = HEIGHT - bar_height

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (x, y, BAR_WIDTH - 2, bar_height),
        )

    pygame.display.flip()

# ================= CLEANUP =================
stream.stop()
pygame.quit()
