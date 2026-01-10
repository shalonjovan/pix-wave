# Pix-Wave 🎶🟩

Pix-Wave is a **real-time audio spectrum visualizer** that turns music into a **pixel-based frequency wave**.

It captures live audio (Spotify, browser music, or system audio on Linux), analyzes it using **FFT**, and renders a smooth, animated pixel equalizer with customizable color themes.

---

## ✨ Features

- 🎧 Live audio input (PipeWire / PulseAudio)
- 📊 FFT-based frequency analysis
- 📐 Logarithmic frequency scaling
- 🟩 Pixel-style retro visualization
- 🎨 Multiple color themes
  - Fire
  - Ice
  - Traffic Lights
- ⬇️ Smooth decay and motion
- ⚙️ Fully configurable via `config.py`
- 🧱 Clean, modular codebase

---

## 🖼️ Screenshots

### 🔥 Fire Theme
![Fire Theme](__screenshots/fire.png__)

### ❄️ Ice Theme
![Ice Theme](__screenshots/ice.png__)

### 🚦 Traffic Lights Theme
![Traffic Lights Theme](__screenshots/traffic_lights.png__)

### 🌟 Neon Theme
![Neon Theme](__screenshots/neon.png__)

---

## 🧠 How It Works (Quick Overview)

```
Audio Output
    ↓
PipeWire / PulseAudio
    ↓
PCM Samples
    ↓
FFT (frequency analysis)
    ↓
Log-scaled frequency bands
    ↓
Amplitude compression + decay
    ↓
Pixel bars on screen
```

Each frame visualizes the **energy of different frequency ranges** in real time.

---

## 📁 Project Structure

```
pix-wave/
├── main.py         # Program entry point
├── audio.py        # Audio capture & FFT logic
├── visualizer.py   # Rendering logic
├── config.py       # All configuration & themes
├── requirements.txt
├── screenshots/    # Screenshots used in README
└── experiments/    # (optional) early tests
```

---

## ⚙️ Configuration

All customization is done in **`config.py`**.

### Change color theme

```python
ACTIVE_THEME = "fire"   # fire | ice | traffic_lights
```

### Tune visuals & DSP

```python
FFT_SIZE = 4096
LOW_FREQ = 300
GAIN = 0.15
DECAY = 0.85
PIXEL_SIZE = 4
```

No other files need editing.

---

## ▶️ Running Pix-Wave

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Play some music

- Spotify (app or web)
- YouTube / browser audio
- Any system audio

### 3️⃣ Run

```bash
python main.py
```

---

## 🐧 Linux Audio Notes

- Designed for PipeWire
- Automatically detects:
  - Spotify
  - Browser audio (Chromium / Firefox)
  - Falls back to system audio if needed
- No manual audio setup required

---

## 🚀 Ideas for Future Improvements

- Stereo (L/R) split visualization
- Mirror & symmetry modes
- Glow / bloom effects
- Circular spectrum
- OpenGL / GPU renderer
- Beat detection

---

## 📜 License

MIT License — free to use, modify, and learn from.