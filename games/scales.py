from .base import GameBase

from ui import FretboardDisplay, Text


class FindScaleDegrees(GameBase):
    """Find the relevant scale degrees in a caged shape region for a given scale"""

    TITLE = 'Find the scale degrees'

    def __init__(self, game_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config = game_config

        self._fretboard = FretboardDisplay()

        self._active_elements.append(
            Text('Key: C / shape: C Caged', 10, 450),
        )

    def draw_start_screen(self, screen):
        self._fretboard.render(screen)
        self._fretboard.render_scale(screen, self._config['scale_pattern'], 7)
        self._fretboard.show_root_notes(screen, self._config['tuning'], self._config['key'])
        self._fretboard.draw_bounding_box(screen, 7, 10, 0, 5)

    def draw_game_screen(self, screen):
        self._fretboard.render(screen)

    def draw_pause_screen(self, screen):
        self._fretboard.render(screen)