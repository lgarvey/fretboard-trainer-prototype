import random
import time

import pygame

import constants as const

from ui import FretboardDisplay
from utils import NoteIterator

from .base import GameBase


class NameTheNote(GameBase):
    """This game puts a dot on the fretboad and asks the player to name it"""

    TITLE = 'Name the note'

    def __init__(self, global_config, game_config, *args, **kwargs):
        super().__init__(global_config, *args, **kwargs)

        self._fretboard = FretboardDisplay()
        self._model = NoteData(game_config)

    def render_start_screen(self, screen):
        self._fretboard.render(screen)
        self.render_all_notes(screen)

    def render_game_screen(self, screen):
        self._fretboard.render(screen)
        self.render_stats(screen)
        current = self._model.get_current_note()
        self._fretboard.render_dot(screen, current['fret'], current['string'])

    def render_stats(self, screen):
        text = self._config['fonts']['default'].render('Correct {correct} // Incorrect {incorrect}'.format(
            **self._model.game_stats
        ), True, (0, 0, 0))
        screen.blit(text, (10, 10))

    def render_final_screen(self, screen):
        font = self._config['fonts']['default']

        title = font.render('~ Game over ~', True, (0, 0, 0))
        duration = font.render('Duration: {}'.format(self.formatted_time()), True, (0, 0, 0))
        total = font.render('Total notes: {}'.format(self._model.game_stats['total']), True, (0, 0, 0))
        average = font.render('Average response time: {} seconds'.format(
            self._model.game_stats['average_response_time']), True, (0, 0, 0))
        accuracy = font.render('Accuracy: {}'.format(self._model.game_stats['accuracy']), True, (0, 0, 0))

        stats_image = pygame.Surface((average.get_width() * 2, title.get_height() * 7))
        stats_image.fill((255, 255, 255))

        for i, image in enumerate([title, duration, total, average, accuracy]):
            y = (i + 1) * (title.get_height() + 3)
            rect = image.get_rect(center=(stats_image.get_width()/2, y))
            stats_image.blit(image, rect)

        pygame.draw.rect(
            stats_image,
            (0, 0, 0),
            pygame.Rect(0, 0, stats_image.get_width()-1, stats_image.get_height()-1),
            1
        )

        rect = stats_image.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
        screen.blit(stats_image, rect)

    def render_all_notes(self, screen):
        """Show all the notes on the fretboard"""
        for note in self._model.notes:
            self._fretboard.render_dot(screen, note['fret'], note['string'])

    def start(self):
        self._model.choose_next_note()
        super().start()

    def handle_mouse_input(self, mouse_x, mouse_y):
        super().handle_mouse_input(mouse_x, mouse_y)

    def handle_keyboard_input(self, key_pressed):
        super().handle_keyboard_input(key_pressed)
        key = chr(key_pressed).upper()

        if self._model.valid_input(key):
            if self._model.handle_input(key):
                self.flash_background(const.COLOUR_SUCCESS, 5)
            else:
                self.flash_background(const.COLOUR_FAILURE, 5)


class NoteData:
    def __init__(self, game_config):
        self._bounds = game_config.get('bounds', (0, 5, 0, 13))
        self._tuning = game_config['tuning']

        self._current_note = None
        self._note_start_time = None
        self._failed_attempt = False

        self.notes = self._build_note_list()

        self.game_stats = {
            'correct': 0,
            'incorrect': 0,
            'total': 0,
            'accuracy': 0,
            'total_response_time': 0,
            'average_response_time': 0,
        }

        self._reset_active_notes()

    def _build_note_list(self):
        """Generate a 1d list of notes that maps to string/fret"""

        notes = []

        fret_count = self._bounds[3] - self._bounds[2]

        for string_index in range(self._bounds[1] - self._bounds[0] + 1):
            for fret_index, note in enumerate(NoteIterator(self._tuning[string_index], fret_count)):
                if len(note) == 1:  # whole note
                    notes.append({
                        'fret': fret_index + self._bounds[2],
                        'string': string_index,
                        'note': note,
                        'selected': 0,
                        'incorrect': 0,
                        'latency': None,
                    })

        return notes

    def _reset_active_notes(self):
        self._active_notes = list(range(len(self.notes)))

    def _calculate_stats(self, response_time):
        """
        Increments total notes and calculates the accuracy and average response time stats
        :param response_time: current note's response time
        """
        self.game_stats['total'] += 1
        self.game_stats['total_response_time'] += response_time
        self.game_stats['average_response_time'] = \
            round(self.game_stats['total_response_time'] / self.game_stats['total'], 2)

        self.game_stats['accuracy'] = round(
            100 * ((self.game_stats['total'] - self.game_stats['incorrect']) / self.game_stats['total']), 2)

    def choose_next_note(self):
        if self._current_note is not None:
            note_time = int(time.time() - self._note_start_time)
            self._calculate_stats(note_time)
            if note_time <= 2:
                # remove all notes that the user selects withint 2 seconds
                print('removing {} {}'.format(
                    self._current_note,
                    self.notes[self._current_note]['note']
                ))
                self._active_notes.pop(self._active_notes.index(self._current_note))

                if len(self._active_notes) <= 2:
                    print('resetting notes')
                    self._reset_active_notes()

        prev_note = self._current_note
        while True:
            self._current_note = random.choice(self._active_notes)
            if self._current_note != prev_note:
                break

        self._note_start_time = time.time()
        self.notes[self._current_note]['selected'] += 1
        self._failed_attempt = False

    def get_current_note(self):
        return self.notes[self._current_note]

    def valid_input(self, note):
        return note in const.NOTES

    def handle_input(self, note):
        if note == self.notes[self._current_note]['note']:
            if not self._failed_attempt:
                self.game_stats['correct'] += 1
            self.choose_next_note()
            return True
        else:
            if not self._failed_attempt:
                self.game_stats['incorrect'] += 1
                self._failed_attempt = True
            return False


class FindAllNotes(GameBase):
    """Find all notes on fretboard"""