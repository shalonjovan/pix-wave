from textual.widget import Widget
from rich.style import Style
from rich.text import Text
import config
import math

DOT = "."


class SpectrumWidget(Widget):
    def __init__(self):
        super().__init__()
        self.levels = None
        self.active_theme = config.DEFAULT_THEME

        self.vertical_density = 1.8  
        self.headroom = 0.65        
        self.gamma = 0.65             

    def set_levels(self, levels):
        self.levels = levels
        self.refresh()

    def set_theme(self, theme):
        self.active_theme = theme
        self.refresh()

    def get_color(self, progress, colors):
        low, mid, high = colors
        if progress < config.LOW_COLOR_THRESHOLD:
            return low
        elif progress < config.MID_COLOR_THRESHOLD:
            return mid
        return high

    def render(self):
        if self.levels is None or len(self.levels) == 0:
            return ""

        width = self.size.width
        height = self.size.height

        theme = config.THEMES[self.active_theme]
        low, mid, high = theme["low"], theme["mid"], theme["high"]

        fft_len = len(self.levels)

        max_height = int(height * self.headroom)

        text = Text()

        for row in range(height):
            y = height - 1 - row

            for col in range(width):
                fft_index = int(col * fft_len / width)
                level = float(self.levels[fft_index])

                level = math.pow(level, self.gamma)

                bar_height = int(
                    level * max_height * self.vertical_density
                )

                if y < bar_height:
                    progress = y / max(1, bar_height)
                    color = self.get_color(progress, (low, mid, high))

                    style = Style(
                        color=f"rgb({color[0]},{color[1]},{color[2]})",
                        bold=True  
                    )

                    text.append(DOT, style=style)
                else:
                    text.append(" ")

            text.append("\n")

        return text
