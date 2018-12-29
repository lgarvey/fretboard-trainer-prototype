SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_FLATS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
WHOLE_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

INTERVALS = ['R', 'min 2nd', '2nd', 'min 3rd', '3rd', '4th', 'tritone',
             '5th', 'min 6th', 'maj 6th', 'min 7th', 'maj 7th']

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

C_SHAPE_MAJOR = [
    [0, 1, 3],
    [1, 3],
    [0, 2, 3],
    [0, 2, 3],
    [0, 1, 3],
    [1, 3],
]

# -----
# Colours

COLOUR_SUCCESS = (153, 255, 153)
COLOUR_FAILURE = (255, 153, 153)
