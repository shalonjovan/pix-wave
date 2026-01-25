from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static
import numpy as np
import config
import audio
from visualizer import SpectrumWidget


class VisualizerApp(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        self.spectrum = SpectrumWidget()
        self.footer = Static(
            "1: traffic  2: ice  3: fire  4: neon   |   Q: quit"
        )
        self.footer.add_class("footer")

        yield Vertical(
            self.spectrum,
            self.footer
        )

    def on_mount(self):
        self.stream = audio.start_audio_stream()
        self.freqs, self.band_edges = audio.setup_frequency_bands()
        self.bar_levels = np.zeros(config.NUM_BARS)

        self.set_interval(1 / config.FPS, self.update_visualizer)

    def update_visualizer(self):
        new_levels = audio.compute_spectrum(self.freqs, self.band_edges)
        self.bar_levels = np.maximum(
            new_levels,
            self.bar_levels * config.DECAY
        )
        self.spectrum.set_levels(self.bar_levels)

    def on_key(self, event):
        if event.key == "q":
            self.exit()

        theme_map = {
            "1": "traffic_lights",
            "2": "ice",
            "3": "fire",
            "4": "neon",
        }

        if event.key in theme_map:
            self.spectrum.set_theme(theme_map[event.key])

    def on_shutdown(self):
        self.stream.stop()


if __name__ == "__main__":
    VisualizerApp().run()
