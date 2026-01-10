import numpy as np
import pygame
import sounddevice as sd

# ===================== CONFIG =====================
SAMPLE_RATE = 48000
FFT_SIZE = 4096
NUM_BARS = 128

FPS = 60

PIXEL_SIZE = 4
PIXEL_GAP = 2
DECAY = 0.85

WIDTH = NUM_BARS * (PIXEL_SIZE + PIXEL_GAP)
HEIGHT = 400

LOW_FREQ = 280
HIGH_FREQ = 20000

GAIN = 0.35   # <<< MASTER VISUAL GAIN (TUNE THIS)

# ===================== FIND SPOTIFY =====================
DEVICE_INDEX = None
for i, dev in enumerate(sd.query_devices()):
    if "spotify" in dev["name"].lower() and dev["max_input_channels"] > 0:
        DEVICE_INDEX = i
        print("Using Spotify stream:", dev["name"])
        break

if DEVICE_INDEX is None:
    raise RuntimeError("Spotify stream not found. Play a song first.")

# ===================== AUDIO BUFFER =====================
audio_buffer = np.zeros(FFT_SIZE)
window = np.hanning(FFT_SIZE)

def audio_callback(indata, frames, time, status):
    global audio_buffer
    mono = np.mean(indata, axis=1)
    audio_buffer = np.roll(audio_buffer, -len(mono))
    audio_buffer[-len(mono):] = mono

stream = sd.InputStream(
    device=DEVICE_INDEX,
    channels=2,
    samplerate=SAMPLE_RATE,
    blocksize=512,
    callback=audio_callback
)
stream.start()

# ===================== FFT SETUP =====================
freqs = np.fft.rfftfreq(FFT_SIZE, 1 / SAMPLE_RATE)[1:]

band_edges = np.logspace(
    np.log10(LOW_FREQ),
    np.log10(HIGH_FREQ),
    NUM_BARS + 1
)

bar_levels = np.zeros(NUM_BARS)

# ===================== PYGAME =====================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ===================== MAIN LOOP =====================
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---------- FFT ----------
    samples = audio_buffer * window
    fft = np.fft.rfft(samples)
    magnitudes = np.abs(fft)[1:]

    # ---------- LOG BANDS ----------
    new_levels = np.zeros(NUM_BARS)

    for i in range(NUM_BARS):
        idx = np.where(
            (freqs >= band_edges[i]) &
            (freqs < band_edges[i + 1])
        )[0]

        if len(idx) > 0:
            new_levels[i] = np.mean(magnitudes[idx])

    # ---------- STABLE COMPRESSION ----------
    new_levels = np.log10(new_levels + 1)
    new_levels *= GAIN
    new_levels = np.clip(new_levels, 0, 1)

    # decay
    bar_levels = np.maximum(new_levels, bar_levels * DECAY)

    # ---------- DRAW ----------
    screen.fill((0, 0, 0))

    for i, level in enumerate(bar_levels):
        pixels = int((level * HEIGHT) // (PIXEL_SIZE + PIXEL_GAP))
        x = i * (PIXEL_SIZE + PIXEL_GAP)

        for p in range(pixels):
            y = HEIGHT - (p + 1) * (PIXEL_SIZE + PIXEL_GAP)

            t = p / max(1, pixels)
            if t < 0.6:
                color = (0, 255, 0)
            elif t < 0.85:
                color = (255, 200, 0)
            else:
                color = (255, 0, 0)

            pygame.draw.rect(screen, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))

    pygame.display.flip()

# ===================== CLEANUP =====================
stream.stop()
pygame.quit()
