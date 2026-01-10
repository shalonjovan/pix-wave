# ================= AUDIO =================
SAMPLE_RATE = 48000
FFT_SIZE = 4096
NUM_BARS = 128

LOW_FREQ = 300
HIGH_FREQ = 20000

# ================= VISUAL =================
FPS = 60
WINDOW_HEIGHT = 500

PIXEL_SIZE = 4
PIXEL_GAP = 2
DECAY = 0.85
GAIN = 0.35

# ================= COLOR THEMES =================
# Colors are ordered bottom → top

THEMES = {
    "traffic_lights": {
        "low":  (0, 255, 0),     # green
        "mid":  (255, 255, 0),   # yellow
        "high": (255, 0, 0),     # red
    },

    "ice": {
        "low":  (0, 255, 255),   # cyan
        "mid":  (0, 120, 255),   # blue
        "high": (180, 0, 255),   # purple
    },

    "fire": {
        "low":  (255, 80, 0),    # deep orange
        "mid":  (255, 160, 0),   # orange/yellow
        "high": (255, 255, 255), # white-hot
    },
    
    "neon": {
        "low":  (0, 255, 120),
        "mid":  (255, 0, 255),
        "high": (0, 200, 255),
    },
}


# ================= ACTIVE THEME =================
ACTIVE_THEME = "neon"   # "traffic_lights", "ice", "fire"

COLOR_LOW = THEMES[ACTIVE_THEME]["low"]
COLOR_MID = THEMES[ACTIVE_THEME]["mid"]
COLOR_HIGH = THEMES[ACTIVE_THEME]["high"]

LOW_COLOR_THRESHOLD = 0.6
MID_COLOR_THRESHOLD = 0.85

