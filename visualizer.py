import pygame
import config

FONT = None
MENU_HEIGHT = 30
MENU_BG = (20, 20, 20)
TEXT_COLOR = (220, 220, 220)


def init_visualizer():
    global FONT
    FONT = pygame.font.SysFont("monospace", 16)


def get_theme_colors(theme):
    t = config.THEMES[theme]
    return t["low"], t["mid"], t["high"]


def get_color(progress, colors):
    low, mid, high = colors
    if progress < config.LOW_COLOR_THRESHOLD:
        return low
    elif progress < config.MID_COLOR_THRESHOLD:
        return mid
    return high


def draw_menu(screen, active_theme):
    x = 10
    for theme in config.THEMES.keys():
        text = FONT.render(theme, True, TEXT_COLOR)
        rect = text.get_rect(topleft=(x, 5))
        screen.blit(text, rect)

        if theme == active_theme:
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        x += rect.width + 15


def handle_menu_click(pos, active_theme):
    x = 10
    for theme in config.THEMES.keys():
        text = FONT.render(theme, True, TEXT_COLOR)
        rect = text.get_rect(topleft=(x, 5))
        if rect.collidepoint(pos):
            return theme
        x += rect.width + 15
    return active_theme


def draw_bars(screen, bar_levels, active_theme):
    colors = get_theme_colors(active_theme)
    screen.fill((0, 0, 0))

    draw_menu(screen, active_theme)

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
            color = get_color(p / max(1, pixels), colors)
            pygame.draw.rect(
                screen,
                color,
                (x, y, config.PIXEL_SIZE, config.PIXEL_SIZE)
            )

    pygame.display.flip()
