import pygame
from ui import Button, Text

from config import COLOUR_BACKGROUND, FONTS
import constants as const
from games.notes import NameTheNote, FindAllNotes
from games.scales import FindScaleDegrees
from games.base import Scene


class MenuScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._active_elements = [
            Text('Fretboard Unlocker', Text.CENTRE, 20, font=FONTS['heading']),
            Button('play_namenotes', 'Play Name The Note', Button.CENTRE, 150, width=300),
            Button('play_findnotes', 'Play Find all Notes', Button.CENTRE, 220, width=300),
            Button('play_scaledegrees', 'Play name the scale degrees', Button.CENTRE, 290, width=300)
        ]

    def draw(self, screen):
        screen.fill(COLOUR_BACKGROUND)
        for elem in self._active_elements:
            elem.render(screen)

    def update(self):
        pass

    def cleanup(self):
        pass

    def handle_event(self, event):

        if event.type == pygame.QUIT:
            return 'quit'

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            for elem in self._active_elements:
                if elem.is_clicked(x, y):
                    if elem.value == 'play_namenotes':
                        game_config = {
                             'tuning': const.GUITAR_STANDARD_TUNING
                        }

                        return NameTheNote(game_config)
                    elif elem.value == 'play_findnotes':
                        game_config = {
                             'tuning': const.GUITAR_STANDARD_TUNING
                        }

                        return FindAllNotes(game_config)
                    elif elem.value == 'play_scaledegrees':
                        game_config = {
                            'tuning': const.GUITAR_STANDARD_TUNING,
                            'scale_pattern': const.C_SHAPE_MAJOR,
                            'key': 'C',
                        }

                        return FindScaleDegrees(game_config)
        return None