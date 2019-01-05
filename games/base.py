from ui import Button
from timer import GameTimer
import pygame

import config


class Scene:
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_event(self, event):
        raise NotImplementedError


class GameBase(Scene):
    READY = 1
    PLAYING = 2
    PAUSED = 3
    FINISHED = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._game_data = {}

        self.state = self.READY

        self._timer = GameTimer()

        self._active_elements = []

        self._start_button = Button(
            'start_button', 'Start Game!', Button.CENTRE, 400)

        self._pause_button = Button(
            'pause_button', 'Pause', Button.CENTRE, 400)

        self._resume_button = Button(
            'resume_button', 'Resume!', Button.CENTRE, 400)

        self._active_elements = [
            self._start_button
        ]

    def clear_screen(self, screen):
        if '_flash_background' in self._game_data:
            self._game_data['_flash_background']['duration'] -= 1
            screen.fill(self._game_data['_flash_background']['colour'])

            if self._game_data['_flash_background']['duration'] == 0:
                self._game_data.pop('_flash_background')
        else:
            screen.fill(config.COLOUR_BACKGROUND)

    def flash_background(self, colour, duration):
        self._game_data['_flash_background'] = {
            'colour': colour,
            'duration': duration
        }

    def draw_header(self, screen):
        text = config.FONTS['heading'].render(self.TITLE, True, config.COLOUR_DEFAULT)
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 10))

    def draw_time(self, screen):
        text = config.FONTS['default'].render(str(self._timer), True, config.COLOUR_DEFAULT)
        screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))

    def draw(self, screen):
        self.clear_screen(screen)
        self.draw_header(screen)

        for elem in self._active_elements:
            elem.render(screen)

        if self.state == self.READY:
            self.draw_start_screen(screen)

        elif self.state == self.PLAYING:
            self.draw_time(screen)

            self.draw_game_screen(screen)

        elif self.state == self.PAUSED:
            self.draw_time(screen)

            self.draw_pause_screen(screen)

        elif self.state == self.FINISHED:
            self.draw_final_screen(screen)

    def start(self):
        assert self.state == self.READY

        self._timer.start()
        self.state = self.PLAYING

        self._active_elements = [
            self._pause_button
        ]

    def resume(self):
        assert self.state == self.PAUSED

        self.state = self.PLAYING

        self._timer.resume()

        self._active_elements = [
            self._pause_button
        ]

    def pause(self):
        assert self.state == self.PLAYING

        self.state = self.PAUSED

        self._timer.pause()

        self._active_elements = [
            self._resume_button
        ]

    def quit(self):
        self.state = self.FINISHED

        self._timer.stop()

        self._active_elements = [
            Button('main_menu', 'Return to main menu', Button.CENTRE, 400)
        ]

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            return self._handle_mouse_input(x, y)

        if event.type == pygame.KEYDOWN:
            self.handle_keyboard_input(event.key)

    def update(self):
        pass

    def _handle_mouse_input(self, mouse_x, mouse_y):
        for elem in self._active_elements:
            if elem.is_clicked(mouse_x, mouse_y):
                if elem.value == 'start_button':
                    self.start()
                    return
                elif elem.value == 'resume_button':
                    self.resume()
                    return
                elif elem.value == 'pause_button':
                    self.pause()
                    return
                elif elem.value == 'main_menu':
                    from scenes import MenuScene
                    self.cleanup()
                    return MenuScene()

        return self.handle_mouse_input(mouse_x, mouse_y)

    def handle_mouse_input(self, x, y):
        raise NotImplementedError

    def handle_keyboard_input(self, key_pressed):
        key = chr(key_pressed).upper()

        if key == 'P':
            if self.state == self.PLAYING:
                self.pause()
            else:
                self.resume()
            return True

        elif key == 'Q':
            self.quit()
            return True

        return False

    def cleanup(self):
        if self._timer:
            self._timer.stop()

    def draw_start_screen(self, screen):
        raise NotImplementedError

    def draw_game_screen(self, screen):
        raise NotImplementedError

    def draw_final_screen(self, screen):
        raise NotImplementedError

    def draw_pause_screen(self, screen):
        raise NotImplementedError
