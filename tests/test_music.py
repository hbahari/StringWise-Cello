import math

import pytest

from stringwise.content.lessons import LESSONS
from stringwise.content.theory import SECTIONS
from stringwise.music import fingering
from stringwise.music.notes import Note, ledger_steps, nearest_note, parse_sequence
from stringwise.music.pieces import BEATS_PER_BAR, PIECES, bars


def test_note_frequencies():
    assert Note("A", 4).freq == pytest.approx(440.0)
    # the cello's open strings
    assert Note("C", 2).freq == pytest.approx(65.41, abs=0.01)
    assert Note("G", 2).freq == pytest.approx(98.00, abs=0.01)
    assert Note("D", 3).freq == pytest.approx(146.83, abs=0.01)
    assert Note("A", 3).freq == pytest.approx(220.00, abs=0.01)


def test_open_strings_on_the_staff():
    # Bass clef: C2 below two ledger lines, G2 on the bottom line,
    # D3 on the middle line, A3 on the top line.
    assert Note("C", 2).staff_step == -4 and ledger_steps(-4) == [-2, -4]
    assert Note("G", 2).staff_step == 0 and ledger_steps(0) == []
    assert Note("D", 3).staff_step == 4
    assert Note("A", 3).staff_step == 8 and ledger_steps(8) == []
    assert Note("C#", 4).staff_step == 10 and ledger_steps(10) == [10]     # middle C line
    assert Note("D", 4).staff_step == 11 and ledger_steps(11) == [10]


def test_nearest_note():
    heard = nearest_note(440.0)
    assert (heard.name, heard.octave, round(heard.cents)) == ("A", 4, 0)
    heard = nearest_note(440.0 * 2 ** (20 / 1200))
    assert heard.name == "A" and round(heard.cents) == 20
    heard = nearest_note(65.4)
    assert (heard.name, heard.octave) == ("C", 2)


def test_finger_pattern_spacing():
    gaps = [b - a for a, b in zip(fingering.FINGER_OFFSETS, fingering.FINGER_OFFSETS[1:])]
    assert gaps == [2, 1, 1, 1]          # whole step to finger 1, then a half step per finger
    for string in fingering.STRINGS:
        for finger, note in enumerate(string.notes):
            assert note.midi - string.open_note.midi == fingering.FINGER_OFFSETS[finger]


def test_fourth_finger_is_an_octave_above_the_string_below():
    # This is the ring test the lessons teach: finger 4 sets the open string below ringing.
    for lower, upper in zip(fingering.STRINGS, fingering.STRINGS[1:]):
        assert upper.notes[4].midi == lower.open_note.midi + 12
        assert upper.open_note.midi - lower.notes[4].midi == 2     # a whole step short of the next string
    assert fingering.target_note("A", 4) == Note("D", 4)
    assert fingering.target_note("G", 2) == Note("Bb", 2)


def test_flats_for_the_low_second_finger():
    from stringwise.music.notes import pretty
    assert Note("Bb", 2).midi == Note("A#", 2).midi
    assert Note("Eb", 2).is_flat and not Note("Eb", 2).is_sharp
    assert Note("F#", 3).is_sharp and not Note("F#", 3).is_flat
    assert not Note("B", 2).is_flat
    assert pretty("Bb") == "B♭" and pretty("C#") == "C♯"
    assert fingering.fingering_for(Note("A#", 2)) == ("G", 2)


def test_tritone_above_an_open_string_needs_an_extension():
    for name, octave in (("F#", 2), ("C#", 3), ("G#", 3), ("D#", 4)):
        assert fingering.fingering_for(Note(name, octave)) is None


def test_parse_sequence():
    notes = parse_sequence("A4:1 C#5:.5 | B4:1.5")
    assert [(n.name, n.octave, n.beats) for n in notes] == [("A", 4, 1), ("C#", 5, .5), ("B", 4, 1.5)]
    with pytest.raises(ValueError):
        parse_sequence("H4:1")


@pytest.mark.parametrize("piece", PIECES.values(), ids=lambda p: p.id)
def test_piece_is_playable_and_bars_add_up(piece):
    for bar in bars(piece):
        assert math.isclose(sum(n.beats for n in bar), BEATS_PER_BAR), piece.id
    for note in piece.notes:
        assert fingering.fingering_for(note) is not None, f"{piece.id}: {note.label} out of reach"


def test_lessons():
    assert [l.week for l in LESSONS] == list(range(1, 13))
    used = []
    for lesson in LESSONS:
        assert lesson.total_minutes == 60, lesson.week
        assert len(lesson.goals) == 3
        if lesson.week >= 2:
            assert len(lesson.pieces) == 2
        for piece_id in lesson.pieces:
            assert piece_id in PIECES
            used.append(piece_id)
    assert sorted(used) == sorted(PIECES)      # every piece is used exactly once


def test_pieces_only_use_strings_already_taught():
    # Week a string's fingered notes are introduced (open strings are fine from week 2).
    taught = {"D": 3, "G": 5, "C": 6, "A": 6}
    for lesson in LESSONS:
        for piece_id in lesson.pieces:
            for note in PIECES[piece_id].notes:
                string, finger = fingering.fingering_for(note)
                if finger:
                    assert lesson.week >= taught[string], (lesson.week, piece_id, note.label)
                if finger == 4:
                    assert lesson.week >= 4


def test_theory_blocks_are_well_formed():
    kinds = {"p", "h", "list", "terms", "open_strings"}
    for section in SECTIONS:
        assert section.blocks
        for block in section.blocks:
            assert block[0] in kinds


def test_reference_pitch_retunes_everything():
    from stringwise.music import notes
    try:
        notes.set_reference(442)
        assert Note("A", 4).freq == pytest.approx(442.0)
        assert Note("G", 3).freq == pytest.approx(442 * 2 ** (-14 / 12))
        heard = nearest_note(442.0)
        assert (heard.name, round(heard.cents)) == ("A", 0)
        notes.set_reference(999)                    # not a choice: back to concert pitch
        assert notes.A4_HZ == 440.0
    finally:
        notes.set_reference(440)
