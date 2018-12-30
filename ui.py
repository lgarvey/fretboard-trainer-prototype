from collections import namedtuple

import pygame

import constants as const
import config


class Element:
    value = None

    def is_clicked(self, x, y):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError


class FretboardDisplay(Element):
    """The fretboard display component"""

    Fret = namedtuple('Fret', ['x', 'mid_x', 'region_x', 'region_width'])
    String = namedtuple('String', ['y', 'mid_y', 'region_y', 'region_height'])

    def __init__(self, frets=13, strings=6):
        self._frets = []
        self._strings = []
        self._start_x = config.FRETBOARD_X_MARGIN
        self._end_x = config.SCREEN_WIDTH - config.FRETBOARD_X_MARGIN
        self._start_y = config.SCREEN_HEIGHT / 2 - ((strings / 2) * config.STRING_SPACING)
        self._end_y = self._start_y + (strings - 1) * config.STRING_SPACING

        self.generate_board(frets, strings)

    def show_root_notes(self, screen, tuning, key):
        for string_index, string_tuning in enumerate(tuning):
            index = const.NOTES.index(key) - const.NOTES.index(string_tuning) - 1
            self.render_dot(screen, index, string_index, colour=(255, 0, 0), shape=3)

    def generate_board(self, frets, strings):
        for i in range(frets):
            fret_x = self._start_x + i * config.FRET_SPACING
            self._frets.append(
                self.Fret(
                    fret_x,
                    fret_x - config.FRET_SPACING / 2 if i != 0 else fret_x,
                    fret_x - config.FRET_SPACING if i != 0 else fret_x - 10,
                    config.FRET_SPACING if i != 0 else 10,
                )
            )
        for i in range(strings):
            string_y = self._start_y + i * config.STRING_SPACING
            self._strings.append(
                self.String(
                    string_y,
                    string_y,
                    string_y - config.STRING_SPACING / 2,
                    config.STRING_SPACING
                )
            )

    def get_index(self, mouse_x, mouse_y):
        """Take mouse coords and determine the fret and string that has been clicked"""

        string_index = None
        fret_index = None

        # if self._frets[0].region_x <= mouse_x <= self._frets[-1].region_x + self._frets[-1].region_width and \
        #     self._strings[0].region_y <= mouse_y <= self._strings[-1].region_y + self._strings[-1].region_height:

        for i, fret in enumerate(self._frets):
            if fret.region_x <= mouse_x <= fret.region_x + fret.region_width:
                fret_index = i
                break

        for i, string in enumerate(self._strings):
            if string.region_y <= mouse_y <= string.region_y + string.region_height:
                string_index = i
                break

        if fret_index is not None and string_index is not None:
            return fret_index, string_index

        return None, None

    def render(self, screen):

        # draw nut
        pygame.draw.line(screen, (0, 0, 0), (50, self._start_y), (50, self._end_y), 3)

        # draw frets
        for fret in self._frets:
            pygame.draw.line(screen, (0, 0, 0), (fret.x, self._start_y), (fret.x, self._end_y), 1)

        # draw strings
        for string in self._strings:
            pygame.draw.line(screen, (0, 0, 0), (self._start_x, string.y), (self._end_x, string.y), 1)

        for fret_index, string_index in const.GUITAR_DOTS:
            pygame.draw.circle(screen, (0, 0, 0),
                               (int(self._frets[fret_index].mid_x + config.FRET_SPACING),
                                int(self._strings[string_index].mid_y + config.STRING_SPACING / 2)), 5, 0)

    def render_dot(self, screen, fret, string, colour=(64, 224, 208), shape=1):
        """Draw a dot in teh middle of the string"""
        x = int(self._frets[fret].mid_x)
        y = int(self._strings[string].mid_y)

        if shape == 1:
            pygame.draw.circle(screen, colour, (x, y), 10, 0)
        elif shape == 2:
            pygame.draw.rect(screen, colour, (x - 10, y - 10, 20, 20))
        else:
            pygame.draw.rect(screen, colour, (x - 5, y - 5, 10, 10))

    def render_scale(self, screen, scale, offset):
        for string_index, string in enumerate(scale):
            for fret in string:
                self.render_dot(screen, fret + offset, string_index, (204, 153, 255))

    def draw_bounding_box(self, screen, min_fret, max_fret, min_string, max_string, colour=(255, 0, 0)):
        rect = pygame.Rect(
            self._frets[min_fret].region_x - (10 if min_fret != 0 else 0),
            self._strings[min_string].region_y,
            self._frets[max_fret].region_x + self._frets[max_fret].region_width - self._frets[min_fret].region_x + 10,
            self._strings[max_string].region_y + self._strings[max_string].region_height - self._strings[min_string].region_y
        )

        pygame.draw.rect(screen, colour, rect, 2)


class Button(Element):
    CENTRE = -1

    def __init__(self, value, text, x, y, padding=10, width=None, height=None, font=None):
        self._x = x
        self._y = y
        self._text = text
        font = font or config.FONTS['button']
        self.value = value

        text_image = font.render(text, True, config.COLOUR_DEFAULT)

        if not width:
            width = 2 * padding + text_image.get_width()

        if not height:
            height = 2 * padding + text_image.get_height()

        self._button = pygame.Surface((width, height))

        self._button.fill(config.COLOUR_BACKGROUND)

        # put a box around the button
        pygame.draw.rect(
            self._button,
            config.COLOUR_DEFAULT,
            pygame.Rect(0, 0, self._button.get_width()-1, self._button.get_height()-1),
            1
        )

        # draw text onto the button
        text_rect = text_image.get_rect(center=(self._button.get_width()/2, self._button.get_height()/2))

        self._button.blit(text_image, text_rect)

        self._button_rect = None

    def render(self, screen):
        x_pos = self._x
        y_pos = self._y

        if self._x == self.CENTRE:
            x_pos = screen.get_width() / 2 - self._button.get_width() / 2

        if self._y == self.CENTRE:
            y_pos = screen.get_height() / 2 - self._button.get_height() / 2

        self._button_rect = screen.blit(self._button, (int(x_pos), int(y_pos),))

    def is_clicked(self, mouse_x, mouse_y):
        return self._button_rect.collidepoint(mouse_x, mouse_y)


class Text(Element):
    CENTRE = -1

    def __init__(self, text, x, y, font=None, colour=config.COLOUR_DEFAULT, *args, **kwargs):
        self._x = x
        self._y = y
        self._coords = None
        self._image = (font or config.FONTS['default']).render(text, True, colour)

    def render(self, screen):
        if not self._coords:
            if self._x == self.CENTRE:
                x_pos = screen.get_width() / 2 - self._image.get_width() / 2
            else:
                x_pos = self._x

            if self._y == self.CENTRE:
                y_pos = screen.get_height() / 2 - self._image.get_height() / 2
            else:
                y_pos = self._y

            self._coords = (x_pos, y_pos)

        screen.blit(self._image, self._coords)

    def is_clicked(self, *args):
        return False
