from datetime import timedelta
import threading
import time


class GameTimer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._paused = False
        self._duration = 0
        self._stopped = False

    def pause(self):
        self._paused = True

    def stop(self):
        self._stopped = True

    def resume(self):
        self._paused = False

    def run(self):
        while not self._stopped:
            if not self._paused:
                self._duration += 1
            time.sleep(1)

    @property
    def duration(self):
        return self._duration

    def __str__(self):
        return str(timedelta(seconds=self._duration))
