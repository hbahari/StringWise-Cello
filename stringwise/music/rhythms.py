"""Rhythm studies for the timing lessons and the rhythm of the day.

Most sit on one note, the open D, so all the attention goes on the timing.
Clap them, then play them. ``week`` is the first week a learner is ready for it.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from .notes import Note, parse_sequence


@dataclass(frozen=True)
class Rhythm:
    id: str
    week: int
    name: str
    notes: tuple[Note, ...]
    subdivide: bool = False     # the metronome clicks the eighth notes too


def _rhythm(id: str, week: int, name: str, sequence: str, subdivide: bool = False) -> Rhythm:
    return Rhythm(id, week, name, tuple(parse_sequence(sequence)), subdivide)


_ALL = [
    # one per week, used by the timing lessons
    _rhythm("w1", 1, "Clap the beat", "D3:1 D3:1 D3:1 D3:1 | D3:2 D3:2 | D3:1 D3:1 D3:2 | D3:4"),
    _rhythm("w2", 2, "Long bows", "D3:4 | D3:4 | D3:2 D3:2 | D3:4"),
    _rhythm("w3", 3, "Quarters on the click", "D3:1 D3:1 D3:1 D3:1 | D3:1 D3:1 D3:2 | D3:2 D3:1 D3:1 | D3:4"),
    _rhythm("w4", 4, "Long and short", "D3:2 D3:1 D3:1 | D3:1 D3:1 D3:2 | D3:1 D3:2 D3:1 | D3:4"),
    _rhythm("w5", 5, "Counting rests", "D3:1 R:1 D3:1 R:1 | D3:1 D3:1 R:2 | D3:2 R:1 D3:1 | D3:4"),
    _rhythm("w6", 6, "String crossings", "G2:1 G2:1 D3:1 D3:1 | A3:1 A3:1 D3:1 D3:1 | G2:1 D3:1 A3:1 D3:1 | G2:4"),
    _rhythm("w7", 7, "Read and clap", "D3:1 D3:1 D3:2 | D3:2 R:1 D3:1 | D3:1 R:1 D3:1 D3:1 | D3:4"),
    _rhythm("w8", 8, "Loud bar, soft bar", "D3:1 D3:1 D3:1 D3:1 | D3:1 D3:1 D3:1 D3:1 | D3:2 D3:2 | D3:4"),
    _rhythm("w9", 9, "Eighths and dots",
            "D3:1 D3:.5 D3:.5 D3:1 D3:.5 D3:.5 | D3:.5 D3:.5 D3:.5 D3:.5 D3:2 | "
            "D3:1.5 D3:.5 D3:1.5 D3:.5 | D3:.5 D3:.5 D3:1 D3:2", subdivide=True),
    # extras for the rhythm of the day
    _rhythm("y1", 1, "Two and two", "D3:2 D3:2 | D3:1 D3:1 D3:1 D3:1 | D3:2 D3:1 D3:1 | D3:4"),
    _rhythm("y2", 1, "Hold the last one", "D3:1 D3:1 D3:1 D3:1 | D3:1 D3:1 D3:2 | D3:1 D3:1 D3:1 D3:1 | D3:4"),
    _rhythm("y3", 1, "Long, then short", "D3:2 D3:1 D3:1 | D3:2 D3:1 D3:1 | D3:1 D3:1 D3:1 D3:1 | D3:4"),
    _rhythm("y4", 1, "Whole and halves", "D3:4 | D3:2 D3:2 | D3:1 D3:1 D3:2 | D3:4"),
    _rhythm("y5", 2, "Short, then long", "D3:1 D3:1 D3:2 | D3:1 D3:1 D3:2 | D3:2 D3:2 | D3:4"),
    _rhythm("y6", 2, "Halves and quarters", "D3:2 D3:2 | D3:2 D3:1 D3:1 | D3:1 D3:1 D3:1 D3:1 | D3:2 D3:2"),
    _rhythm("x1", 3, "Walk, then hold", "D3:1 D3:1 D3:2 | D3:2 D3:2 | D3:1 D3:1 D3:1 D3:1 | D3:4"),
    _rhythm("x2", 4, "Held in the middle", "D3:2 D3:2 | D3:1 D3:2 D3:1 | D3:1 D3:1 D3:1 D3:1 | D3:4"),
    _rhythm("x3", 5, "Rest on three", "D3:1 D3:1 R:1 D3:1 | D3:2 R:2 | D3:1 R:1 D3:2 | D3:4"),
    _rhythm("x4", 7, "Late start", "R:1 D3:1 D3:1 D3:1 | D3:2 R:1 D3:1 | D3:1 D3:1 R:1 D3:1 | D3:4"),
    _rhythm("x5", 9, "Running eighths",
            "D3:.5 D3:.5 D3:1 D3:.5 D3:.5 D3:1 | D3:1 D3:1 D3:2 | D3:1.5 D3:.5 D3:2 | D3:4", subdivide=True),
    _rhythm("x6", 9, "Dotted steps",
            "D3:1 D3:.5 D3:.5 D3:2 | D3:.5 D3:.5 D3:.5 D3:.5 D3:1 D3:1 | D3:1.5 D3:.5 D3:1 D3:1 | D3:4",
            subdivide=True),
]

RHYTHMS: dict[str, Rhythm] = {r.id: r for r in _ALL}


def rhythm_of_the_day(current_week: int, today: datetime.date | None = None) -> Rhythm:
    """One rhythm per day, chosen only from those the learner has met so far."""
    today = today or datetime.date.today()
    pool = [r for r in _ALL if r.week <= max(1, current_week)]
    return pool[today.toordinal() % len(pool)]


def rhythm_menu() -> list[Rhythm]:
    """Every rhythm, easiest first, for the picker on the Practice tab."""
    return sorted(_ALL, key=lambda r: r.week)
