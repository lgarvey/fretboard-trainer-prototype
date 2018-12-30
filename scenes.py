import pygame
from ui import Button, Text

from config import COLOUR_BACKGROUND, FONTS
import constants as const
from games.notes import NameTheNote
from games.base import Scene


class MenuScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._active_elements = [
            Text('Fretboard Unlocker', Text.CENTRE, 50, font=FONTS['heading']),
            Button('play_namenotes', 'Play Name The Note', Button.CENTRE, 150),
            Button('play_findnotes', 'Play Find all Notes', Button.CENTRE, 220)
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
                        pass
        return None