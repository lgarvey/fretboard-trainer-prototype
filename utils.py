import constants as const


class NoteIterator:
    def __init__(self, start_note, stop):
        self._index = const.NOTES.index(start_note)
        self._required_notes = stop

    def __iter__(self):
        return self

    def __next__(self):

        if self._required_notes == 0:
            raise StopIteration

        self._required_notes -= 1

        note = const.NOTES[self._index]

        self._index += 1

        if self._index >= len(const.NOTES):
            self._index = 0

        return note


def fretboard_indices_to_note(fret, string, tuning):
    open_note = tuning[string]

    start_index = const.NOTES.index(open_note)

    return const.NOTES[(start_index + fret) % 12]