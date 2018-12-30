import pygame

# ----------
# dimensions

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# fretboard dimensions
FRET_WIDTH = 50
STRING_SPACING = 20
FRETBOARD_X_MARGIN = 50
FRET_SPACING = (SCREEN_WIDTH - 2 * FRETBOARD_X_MARGIN) / 12

# ----------
# Colours

COLOUR_SUCCESS = (153, 255, 153)
COLOUR_FAILURE = (255, 153, 153)
COLOUR_DEFAULT = (0, 0, 0)
COLOUR_BACKGROUND = (255, 255, 255)

# ----------
# fonts

FONTS = {
    'heading': ('fonts/Amatic-Bold.ttf', 72),
    'button': ('fonts/Amatic-Bold.ttf', 32),
    'default': ('fonts/Amatic-Bold.ttf', 25),

}

# ----------

def init_fonts():
    """
    initialise fonts - this must be called after pygame.init()
    """
    for key, args in FONTS.items():
        FONTS[key] = pygame.font.Font(*args)
