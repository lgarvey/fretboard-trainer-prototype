import time
from datetime import timedelta

from ui import Button


class GameBase:
    # game states
    READY = 1
    PLAYING = 2
    PAUSED = 3
    FINISHED = 4

    def __init__(self, global_config, *args, **kwargs):
        self._game_data = {}

        self.state = self.READY

        self._config = global_config

        self._active_elements = []

        self._start_button = Button(
            'start_button', 'Start Game!', Button.CENTRE, 400, font=self._config['fonts']['button'])

        self._pause_button = Button(
            'pause_button', 'Pause', Button.CENTRE, 400, font=self._config['fonts']['button'])

        self._resume_button = Button(
            'resume_button', 'Resume!', Button.CENTRE, 400, font=self._config['fonts']['button'])

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
            screen.fill((255, 255, 255))

    def flash_background(self, colour, duration):
        self._game_data['_flash_background'] = {
            'colour': colour,
            'duration': duration
        }

    def render_header(self, screen):
        text = self._config['fonts']['heading'].render(self.TITLE, True, (0, 0, 0))
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 50))

    def render_time(self, screen):
        current_time = str(timedelta(seconds=int(time.time() - self._start_time)))

        text = self._config['fonts']['default'].render(current_time, True, (0, 0, 0))
        screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))

    def render(self, screen):
        self.clear_screen(screen)
        self.render_header(screen)

        for elem in self._active_elements:
            elem.render(screen)

        if self.state == self.READY:
            self.render_start_screen(screen)

        elif self.state == self.PLAYING:
            self.render_time(screen)

            self.render_game_screen(screen)

        elif self.state == self.PAUSED:
            self.render_time(screen)

        elif self.state == self.FINISHED:
            raise NotImplemented

    def start(self):
        assert self.state == self.READY

        self._start_time = time.time()
        self.state = self.PLAYING

        self._active_elements = [
            self._pause_button
        ]

    def resume(self):
        assert self.state == self.PAUSED

        self.state = self.PLAYING

        # TODO: handle time logic

        self._active_elements = [
            self._pause_button
        ]

    def pause(self):
        assert self.state == self.PLAYING

        self.state = self.PAUSED

        self._active_elements = [
            self._resume_button
        ]

    def quit(self):
        self.state = self.FINISHED

    def handle_mouse_input(self, mouse_x, mouse_y):
        for elem in self._active_elements:
            if elem.is_clicked(mouse_x, mouse_y):
                if elem.value == 'start_button':
                    self.start()
                elif elem.value == 'resume_button':
                    self.resume()
                elif elem.value == 'pause_button':
                    self.pause()

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

    def render_start_screen(self, screen):
        raise NotImplemented

    def render_game_screen(self, screen):
        raise NotImplemented
