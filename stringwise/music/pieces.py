"""Practice pieces. Two per week from week 2 onward.

Traditional tunes are simplified arrangements. Everything else was written for
this course. Every piece stays inside the cello first-position pattern in
``fingering.py`` and every bar adds up to four beats; the tests check both.
"""

from __future__ import annotations

from dataclasses import dataclass

from .notes import Note, parse_sequence

BEATS_PER_BAR = 4


@dataclass(frozen=True)
class Piece:
    id: str
    title: str
    info: str
    notes: tuple[Note, ...]


def _piece(id: str, title: str, info: str, sequence: str) -> Piece:
    return Piece(id, title, info, tuple(parse_sequence(sequence)))


_ALL = [
    _piece("openwarmup", "Open String Warm-Up",
           "All four open strings, low to high and back.",
           "C2:2 G2:2 | D3:2 A3:2 | A3:2 D3:2 | G2:2 C2:2 | C2:4"),
    _piece("crossings", "Open String Crossings",
           "Open strings only. Keep the bow moving at one speed while your arm changes level.",
           "D3:1 D3:1 G2:1 G2:1 | D3:1 D3:1 A3:1 A3:1 | G2:1 G2:1 C2:1 C2:1 | G2:1 D3:1 A3:1 D3:1 | D3:4"),
    _piece("firstpattern", "First Pattern Warm-Up",
           "D string: open, then fingers 1 and 3.",
           "D3:1 E3:1 F#3:2 | F#3:1 E3:1 D3:2 | D3:1 E3:1 F#3:1 E3:1 | D3:4"),
    _piece("hotcrossbuns", "Hot Cross Buns",
           "D string: open, finger 1 and finger 3.",
           "F#3:1 E3:1 D3:2 | F#3:1 E3:1 D3:2 | D3:1 D3:1 E3:1 E3:1 | F#3:1 E3:1 D3:2"),
    _piece("skips", "Steps and Skips",
           "D string, open to finger 4. Some notes move to the next finger, some jump over one.",
           "D3:1 E3:1 F#3:2 | G3:1 F#3:1 E3:2 | D3:1 F#3:1 E3:1 G3:1 | F#3:1 E3:1 D3:2"),
    _piece("ode", "Ode to Joy",
           "D string, open to finger 4. The top note, A, is the open A string. Rhythm slightly simplified.",
           "F#3:1 F#3:1 G3:1 A3:1 | A3:1 G3:1 F#3:1 E3:1 | D3:1 D3:1 E3:1 F#3:1 | F#3:1 E3:1 E3:2 | "
           "F#3:1 F#3:1 G3:1 A3:1 | A3:1 G3:1 F#3:1 E3:1 | D3:1 D3:1 E3:1 F#3:1 | E3:1 D3:1 D3:2"),
    _piece("mary", "Mary Had a Little Lamb",
           "G string: open, finger 1 and finger 3, with one visit to the open D.",
           "B2:1 A2:1 G2:1 A2:1 | B2:1 B2:1 B2:2 | A2:1 A2:1 A2:2 | B2:1 D3:1 D3:2 | "
           "B2:1 A2:1 G2:1 A2:1 | B2:1 B2:1 B2:1 B2:1 | A2:1 A2:1 B2:1 A2:1 | G2:4"),
    _piece("twinkle", "Twinkle, Twinkle, Little Star",
           "G and D strings. The first half of the tune, in G major.",
           "G2:1 G2:1 D3:1 D3:1 | E3:1 E3:1 D3:2 | C3:1 C3:1 B2:1 B2:1 | A2:1 A2:1 G2:2"),
    _piece("lightlyrow", "Lightly Row",
           "D string, plus the open A for the top note.",
           "A3:1 F#3:1 F#3:2 | G3:1 E3:1 E3:2 | D3:1 E3:1 F#3:1 G3:1 | A3:1 A3:1 A3:2 | "
           "A3:1 F#3:1 F#3:2 | G3:1 E3:1 E3:2 | D3:1 F#3:1 A3:1 A3:1 | D3:4"),
    _piece("auclair", "Au Clair de la Lune",
           "C string only: open, finger 1 and finger 3.",
           "C2:1 C2:1 C2:1 D2:1 | E2:2 D2:2 | C2:1 E2:1 D2:1 D2:1 | C2:4"),
    _piece("reading", "Reading Study",
           "G and D strings. A short study written for this week. Name each note before you play it.",
           "G2:1 A2:1 B2:1 C3:1 | D3:1 C3:1 B2:1 A2:1 | G2:2 B2:1 D3:1 | C3:1 B2:1 A2:2 | G2:4"),
    _piece("oldmac", "Old MacDonald",
           "G and D strings. You know how it goes, so let your eyes follow the page.",
           "G2:1 G2:1 G2:1 D3:1 | E3:1 E3:1 D3:2 | B2:1 B2:1 A2:1 A2:1 | G2:4"),
    _piece("dynamics", "Loud and Soft Study",
           "D string. Play it through once forte and once piano.",
           "D3:1 E3:1 F#3:1 E3:1 | D3:4 | F#3:1 G3:1 F#3:1 E3:1 | D3:4"),
    _piece("london", "London Bridge",
           "G and D strings, rhythm simplified. Try each phrase loud, then repeat it soft like an echo.",
           "D3:1 E3:1 D3:1 C3:1 | B2:1 C3:1 D3:2 | A2:1 B2:1 C3:2 | B2:1 C3:1 D3:2 | "
           "D3:1 E3:1 D3:1 C3:1 | B2:1 C3:1 D3:2 | A2:2 D3:2 | B2:2 G2:2"),
    _piece("rhythmecho", "Rhythm Echo",
           "D string. Eighth notes in the first two bars, dotted quarters in the third. Clap it first.",
           "D3:1 D3:.5 D3:.5 E3:1 E3:.5 E3:.5 | F#3:1 F#3:.5 F#3:.5 G3:2 | "
           "G3:1.5 F#3:.5 E3:1.5 D3:.5 | E3:1 F#3:.5 E3:.5 D3:2"),
    _piece("longlongago", "Long, Long Ago",
           "D and A strings. The long-short-short rhythm repeats all the way through.",
           "D3:1 D3:.5 E3:.5 F#3:1 F#3:.5 G3:.5 | A3:1 B3:.5 A3:.5 F#3:2 | "
           "A3:1 G3:.5 F#3:.5 E3:2 | G3:1 F#3:.5 E3:.5 D3:2"),
    _piece("scale", "G Major Scale",
           "One octave. G string open to finger 4, then D string open to finger 4, and back down.",
           "G2:1 A2:1 B2:1 C3:1 | D3:1 E3:1 F#3:1 G3:1 | G3:1 F#3:1 E3:1 D3:1 | C3:1 B2:1 A2:1 G2:1 | G2:4"),
    _piece("thirds", "G Major Scale in Thirds",
           "G and D strings. The same scale, skipping a note each time.",
           "G2:1 B2:1 A2:1 C3:1 | B2:1 D3:1 C3:1 E3:1 | D3:1 F#3:1 E3:1 G3:1 | G3:4"),
    _piece("etude", "Etude in G",
           "G and D strings. Built on the notes of the G major chord.",
           "G2:1 B2:1 D3:1 G3:1 | G3:2 D3:2 | B2:1 D3:1 G3:1 B2:1 | G2:4"),
    _piece("andante", "Andante in G",
           "G and D strings. A slow tune for long, smooth bows.",
           "G2:1 B2:1 D3:1 B2:1 | C3:1 E3:1 D3:2 | B2:1 D3:1 G3:1 D3:1 | E3:1 C3:1 B2:2 | "
           "A2:1 C3:1 B2:1 A2:1 | G2:4"),
    _piece("recital", "Recital Piece",
           "All four strings. It climbs from the open C to the open A, then comes home.",
           "C2:1 D2:1 E2:1 F2:1 | G2:1 A2:1 B2:1 C3:1 | D3:1 E3:1 F#3:1 G3:1 | A3:2 E3:2 | C3:2 G2:2 | C2:4"),
    _piece("arpeggio", "G Major Arpeggio",
           "G, D and A strings. The G major chord from open G up to D on the A string and back.",
           "G2:1 B2:1 D3:1 G3:1 | B3:1 D4:1 B3:1 G3:1 | D3:1 B2:1 G2:2"),
]

PIECES: dict[str, Piece] = {p.id: p for p in _ALL}


def bars(piece: Piece) -> list[list[Note]]:
    """Split a piece into bars of four beats."""
    result, current, total = [], [], 0.0
    for note in piece.notes:
        current.append(note)
        total += note.beats
        if total >= BEATS_PER_BAR - 1e-9:
            result.append(current)
            current, total = [], 0.0
    if current:
        result.append(current)
    return result
