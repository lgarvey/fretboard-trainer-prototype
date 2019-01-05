import random
import time

import pygame

import constants as const
import config
from ui import FretboardDisplay
from utils import NoteIterator

from .base import GameBase


class NameTheNote(GameBase):
    """This game puts a dot on the fretboad and asks the player to name it"""

    TITLE = 'Name the note'

    def __init__(self, game_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._fretboard = FretboardDisplay()
        self._model = NoteData(game_config)

    def draw_start_screen(self, screen):
        self._fretboard.render(screen)
        self.draw_all_notes(screen)

    def draw_game_screen(self, screen):
        self._fretboard.render(screen)
        self.draw_stats(screen)
        current = self._model.get_current_note()
        self._fretboard.render_dot(screen, current['fret'], current['string'])

    def draw_pause_screen(self, screen):
        self._fretboard.render(screen)

    def draw_stats(self, screen):
        text = config.FONTS['default'].render('Correct {correct} // Incorrect {incorrect}'.format(
            **self._model.game_stats
        ), True, config.COLOUR_DEFAULT)
        screen.blit(text, (10, 10))

    def draw_final_screen(self, screen):
        font = config.FONTS['default']

        title = font.render('~ Game over ~', True, config.COLOUR_DEFAULT)
        duration = font.render('Duration: {}'.format(str(self._timer)), True, config.COLOUR_DEFAULT)
        total = font.render('Total notes: {}'.format(self._model.game_stats['total']), True, config.COLOUR_DEFAULT)
        average = font.render('Average response time: {} seconds'.format(
            self._model.game_stats['average_response_time']), True, config.COLOUR_DEFAULT)
        accuracy = font.render('Accuracy: {}%'.format(self._model.game_stats['accuracy']), True, config.COLOUR_DEFAULT)

        stats_image = pygame.Surface((average.get_width() * 2, title.get_height() * 7))
        stats_image.fill(config.COLOUR_BACKGROUND)

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

    def draw_all_notes(self, screen):
        """Show all the notes on the fretboard"""
        for note in self._model.notes:
            self._fretboard.render_dot(screen, note['fret'], note['string'])

    def start(self):
        super().start()
        self._model.choose_next_note()

    def handle_keyboard_input(self, key_pressed):
        super().handle_keyboard_input(key_pressed)
        key = chr(key_pressed).upper()

        if self._model.valid_input(key):
            if self._model.handle_input(key):
                self.flash_background(config.COLOUR_SUCCESS, 5)
            else:
                self.flash_background(config.COLOUR_FAILURE, 5)

    def handle_mouse_input(self, x, y):
        pass


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

    TITLE = 'Find all the notes'

    def __init__(self, game_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._fretboard = FretboardDisplay()
        self._model = FindTheNoteData(game_config)
        self._restart_delay = None

    def draw_start_screen(self, screen):
        self._fretboard.render(screen)
        self.draw_all_notes(screen)

    def draw_note_text(self, screen):
        if self._model.success():
            text = config.FONTS['button'].render(
                'Success!', True, config.COLOUR_DEFAULT
            )
        else:
            text = config.FONTS['button'].render(
                'Find all the {} notes'.format(self._model.current_note), True, config.COLOUR_DEFAULT)
        rect = text.get_rect(center=(screen.get_width() / 2, 130))
        screen.blit(text, rect)

    def draw_game_screen(self, screen):
        self._fretboard.render(screen)
        self.draw_note_text(screen)
        self.draw_selected_notes(screen)

    def draw_pause_screen(self, screen):
        self._fretboard.render(screen)

    def draw_selected_notes(self, screen):
        for note in self._model.get_selected_notes():
            self._fretboard.render_dot(screen, note['fret'], note['string'], (255, 0, 0))

    def draw_all_notes(self, screen):
        """Show all the notes on the fretboard"""
        for note in self._model.notes:
            self._fretboard.render_dot(screen, note['fret'], note['string'])

    def update(self):
        if self._model.success() and not self._restart_delay:
            self._restart_delay = 120

        if self._restart_delay is not None:
            self._restart_delay -= 1

            if self._restart_delay <= 0:
                self._restart_delay = None
                self._model.choose_next_note()

    def start(self):
        super().start()
        self._model.choose_next_note()
        self._restart_delay = None

    def handle_keyboard_input(self, key_pressed):
        super().handle_keyboard_input(key_pressed)
        key = chr(key_pressed).upper()

    def handle_mouse_input(self, x, y):
        index = self._fretboard.get_index(x, y)

        if index:
            if self._model.handle_note_selection(*index):
                self.flash_background(config.COLOUR_SUCCESS, 5)
            else:
                self.flash_background(config.COLOUR_FAILURE, 5)


class FindTheNoteData:
    def __init__(self, game_config):
        self._bounds = game_config.get('bounds', (0, 5, 0, 13))
        self._tuning = game_config['tuning']

        self._config = game_config

        self.notes = self._build_note_list()

        self._available_notes = None
        self.current_note = None
        self.current_note_list = []
        self._found_note_indexes = set()
        self._wrong_notes = 0

    @staticmethod
    def _get_available_notes():
        notes = const.WHOLE_NOTES
        random.shuffle(notes)
        return notes

    def choose_next_note(self):
        if not self._available_notes:
            self._available_notes = self._get_available_notes()

        self.current_note = self._available_notes.pop()
        self.current_note_list = [note for note in self.notes if note['note'] == self.current_note]
        self._found_note_indexes = set()
        self._wrong_notes = 0

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

    def handle_note_selection(self, fret, string):
        for i, note in enumerate(self.current_note_list):
            if (fret, string) == (note['fret'], note['string']):
                self._found_note_indexes.add(i)
                return True

        self._wrong_notes += 1
        return False

    def get_selected_notes(self):
        return [self.current_note_list[index] for index in self._found_note_indexes]

    def success(self):
        return len(self.current_note_list) == len(self._found_note_indexes)
