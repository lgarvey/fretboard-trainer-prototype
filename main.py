import pygame

from games.notes import NameTheNote
import constants as const


def main_loop(global_config):

    game_config = {
        'tuning': const.GUITAR_STANDARD_TUNING
    }

    game = NameTheNote(global_config, game_config)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                game.handle_mouse_input(x, y)

            if event.type == pygame.KEYDOWN:
                game.handle_keyboard_input(event.key)

        game.render(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))

    game_config = {
        'fonts': {
            'heading': pygame.font.Font('fonts/Amatic-Bold.ttf', 72),
            'button': pygame.font.Font('fonts/Amatic-Bold.ttf', 32),
            'default': pygame.font.Font('fonts/Amatic-Bold.ttf', 25),
        }
    }

    main_loop(game_config)
