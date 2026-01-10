import pygame
import config


def get_color(progress):
    if progress < config.LOW_COLOR_THRESHOLD:
        return config.COLOR_LOW
    elif progress < config.MID_COLOR_THRESHOLD:
        return config.COLOR_MID
    return config.COLOR_HIGH


def draw_bars(screen, bar_levels):
    screen.fill((0, 0, 0))

    for i, level in enumerate(bar_levels):
        pixels = int(
            (level * config.WINDOW_HEIGHT) //
            (config.PIXEL_SIZE + config.PIXEL_GAP)
        )

        x = i * (config.PIXEL_SIZE + config.PIXEL_GAP)

        for p in range(pixels):
            y = config.WINDOW_HEIGHT - (p + 1) * (
                config.PIXEL_SIZE + config.PIXEL_GAP
            )

            color = get_color(p / max(1, pixels))

            pygame.draw.rect(
                screen,
                color,
                (x, y, config.PIXEL_SIZE, config.PIXEL_SIZE)
            )

    pygame.display.flip()
