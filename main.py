import pygame
import numpy as np
import config
import audio
import visualizer

# ================= INIT AUDIO =================
stream = audio.start_audio_stream()
freqs, band_edges = audio.setup_frequency_bands()

bar_levels = np.zeros(config.NUM_BARS)

# ================= INIT PYGAME =================
pygame.init()
visualizer.init_visualizer()

WIDTH = config.NUM_BARS * (config.PIXEL_SIZE + config.PIXEL_GAP)
screen = pygame.display.set_mode((WIDTH, config.WINDOW_HEIGHT))
clock = pygame.time.Clock()

active_theme = config.DEFAULT_THEME

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(config.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            active_theme = visualizer.handle_menu_click(
                event.pos, active_theme
            )

    new_levels = audio.compute_spectrum(freqs, band_edges)
    bar_levels = np.maximum(new_levels, bar_levels * config.DECAY)

    visualizer.draw_bars(screen, bar_levels, active_theme)

# ================= CLEANUP =================
stream.stop()
pygame.quit()
