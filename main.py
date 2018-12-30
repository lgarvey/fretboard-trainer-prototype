import pygame

import config
from scenes import MenuScene


def game_loop():

    current_scene = MenuScene()

    while True:
        if pygame.event.get(pygame.QUIT):
            current_scene.cleanup()
            break

        for event in pygame.event.get():
            new_scene = current_scene.handle_event(event)

            if new_scene:
                current_scene = new_scene

        current_scene.draw(screen)
        current_scene.update()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    config.init_fonts()

    game_loop()

    pygame.quit()
