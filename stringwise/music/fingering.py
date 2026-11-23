"""Cello first-position fingering, the pattern the course teaches.

On the cello each finger sits a half step from the next, so the hand covers a
minor third from finger 1 to finger 4. The one whole step is from the open string
to finger 1. Major keys use fingers 1, 3 and 4; finger 2 plays the minor third
(F on the D string, C on the A string) and otherwise rests behind finger 3.
"""

from __future__ import annotations

from dataclasses import dataclass

from .notes import Note

# Semitones above the open string for: open, finger 1, 2, 3, 4.
# Gaps: open-1 whole, 1-2 half, 2-3 half, 3-4 half.
FINGER_OFFSETS = (0, 2, 3, 4, 5)


@dataclass(frozen=True)
class CelloString:
    name: str
    open_note: Note
    notes: tuple[Note, ...]   # open, 1, 2, 3, 4

    @property
    def open_hz(self) -> float:
        return self.open_note.freq


def _build(name: str, octave: int, names: tuple[str, ...], octaves: tuple[int, ...]) -> CelloString:
    notes = tuple(Note(n, o) for n, o in zip(names, octaves))
    return CelloString(name, Note(name, octave), notes)


# Lowest string first.
STRINGS: tuple[CelloString, ...] = (
    _build("C", 2, ("C", "D", "Eb", "E", "F"), (2, 2, 2, 2, 2)),
    _build("G", 2, ("G", "A", "Bb", "B", "C"), (2, 2, 2, 2, 3)),
    _build("D", 3, ("D", "E", "F", "F#", "G"), (3, 3, 3, 3, 3)),
    _build("A", 3, ("A", "B", "C", "C#", "D"), (3, 3, 4, 4, 4)),
)
STRING_BY_NAME = {s.name: s for s in STRINGS}

# How far along the string each finger lands, as a fraction of the string length
# from the nut. This is plain physics: a note n semitones up stops the string at
# 1 - 2^(-n/12) of its length.
FINGER_POSITIONS = tuple(1 - 2 ** (-n / 12) for n in FINGER_OFFSETS)


def target_note(string_name: str, finger: int) -> Note:
    return STRING_BY_NAME[string_name].notes[finger]


def fingering_for(note: Note) -> tuple[str, int] | None:
    """Where a beginner would play ``note``: (string name, finger), or None if out of reach.

    In first position on the cello no note can be played two ways, so this is a
    straight lookup. Notes a tritone above an open string (F♯ on the C string,
    C♯ on the G string, G♯ on the D string) need an extension and are out of reach.
    """
    if note.is_rest:
        return None
    for string in STRINGS:
        for finger, candidate in enumerate(string.notes):
            if candidate.midi == note.midi:
                return string.name, finger
    return None
