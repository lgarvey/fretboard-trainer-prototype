from collections import namedtuple

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_FLATS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
WHOLE_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

GUITAR_DOTS = [
    [2, 2],
    [4, 2],
    [6, 2],
    [8, 2],
    [11, 1],
    [11, 3]
]

GUITAR_STANDARD_TUNING = ['E', 'B', 'G', 'D', 'A', 'E']

# migrate to fret class?
FRET_WIDTH = 50
STRING_SPACING = 20
FRETBOARD_X_MARGIN = 50
FRET_SPACING = (SCREEN_WIDTH - 2 * FRETBOARD_X_MARGIN) / 12

Fret = namedtuple('Fret', ['x', 'mid_x', 'region_x', 'region_width'])
String = namedtuple('String', ['y', 'mid_y', 'region_y', 'region_height'])


class FretboardDisplay:
    """The fretboard display component"""

    def __init__(self, frets=13, strings=6):
        self._frets = []
        self._strings = []
        self._start_x = FRETBOARD_X_MARGIN
        self._end_x = SCREEN_WIDTH - FRETBOARD_X_MARGIN
        self._start_y = SCREEN_HEIGHT / 2 - ((strings / 2) * STRING_SPACING)
        self._end_y = self._start_y + (strings - 1) * STRING_SPACING

        self.generate_board(frets, strings)

    def generate_board(self, frets, strings):
        for i in range(frets):
            fret_x = self._start_x + i * FRET_SPACING
            self._frets.append(
                Fret(
                    fret_x,
                    fret_x - FRET_SPACING / 2 if i != 0 else fret_x,
                    fret_x - FRET_SPACING if i != 0 else fret_x - 10,
                    FRET_SPACING if i != 0 else 10,
                )
            )
        for i in range(strings):
            string_y = self._start_y + i * STRING_SPACING
            self._strings.append(
                String(
                    string_y,
                    string_y,
                    string_y - STRING_SPACING / 2,
                    STRING_SPACING
                )
            )

    def get_index(self, mouse_x, mouse_y):
        """Take mouse coords and determine the fret and string that have been clicked"""

        string_index = None
        fret_index = None

        # import pdb; pdb.set_trace()

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

        # # draw dot markers
        for fret_index, string_index in GUITAR_DOTS:
            pygame.draw.circle(screen, (0, 0, 0),
                               (int(self._frets[fret_index].mid_x + FRET_SPACING),
                                int(self._strings[string_index].mid_y + STRING_SPACING / 2)), 5, 0)

    def render_dot(self, screen, fret, string, colour=(64, 224, 208)):
        """Draw a dot in teh middle of the string"""
        x = int(self._frets[fret].mid_x)
        y = int(self._strings[string].mid_y)

        pygame.draw.circle(screen, colour, (x, y), 10, 0)

    def draw_bounding_box(self, screen, min_fret, max_fret, min_string, max_string, colour=(255, 0, 0)):
        rect = pygame.Rect(
            self._frets[min_fret].region_x - (10 if min_fret != 0 else 0),
            self._strings[min_string].region_y,
            self._frets[max_fret].region_x + self._frets[max_fret].region_width - self._frets[min_fret].region_x + 10,
            self._strings[max_string].region_y + self._strings[max_string].region_height - self._strings[min_string].region_y
        )

        pygame.draw.rect(screen, colour, rect, 2)


def main_loop():
    running = True

    fretboard = FretboardDisplay()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.fill((255, 255, 255))

            mouse_x, mouse_y = handle_mouse_input()

            input_box_x, input_box_y, input_box_width, input_box_height = render_input_box(screen, None)

            if mouse_x:
                fret, string = fretboard.get_index(mouse_x, mouse_y)

                if fret is not None:
                    fretboard.render_dot(screen, fret, string)
                    note = fretboard_indices_to_note(fret, string, GUITAR_STANDARD_TUNING)
                    text = font.render(note, True, (0, 0, 0))
                    text_x = input_box_x + input_box_width / 2 - text.get_width() / 2
                    text_y = input_box_y + input_box_height / 2 - text.get_height() / 2
                    screen.blit(text, (text_x, text_y))

            pygame.event.get()
            fretboard.render(screen)
            # fretboard.draw_bounding_box(screen, 0, 4, 0, 5)
            fretboard.draw_bounding_box(screen, 0, 12, 0, 0)

            pygame.display.flip()

            clock.tick(60)


def handle_mouse_input():

    btn, _, _ = pygame.mouse.get_pressed()

    if btn:
        x, y = pygame.mouse.get_pos()

        return x, y

    return None, None


def render_input_box(screen, display_text):
    x = SCREEN_WIDTH / 2 - 50
    y = 40

    rect = pygame.Rect(x, y, 100, 100)

    pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    return x, y, 100, 100


def fretboard_indices_to_note(fret, string, tuning):
    open_note = tuning[string]

    start_index = NOTES.index(open_note)

    return NOTES[(start_index + fret) % 12]


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))

    font = pygame.font.SysFont(None, 72)
    main_loop()


