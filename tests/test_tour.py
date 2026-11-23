"""The first-launch tour: its words, and the geometry of the overlay.

These run without Kivy, like the rest of the tests on the build server.
"""

from types import SimpleNamespace

from stringwise.content import tour
from stringwise.logic import tour_layout as layout

KNOWN_TARGETS = {"tuner.dial", "metronome.panel", "header.metronome", "lessons.weeks",
                 "fingers.board", "theory.first", "practice.rhythm", "header.gear"}
SCREENS = {"tuner", "metronome", "lessons", "fingers", "theory", "practice"}


def test_ten_steps_with_centred_first_and_last():
    assert len(tour.STEPS) == 10
    assert tour.STEPS[0].target is None and tour.STEPS[-1].target is None
    assert len(tour.TARGETED) == 8


def test_every_step_points_somewhere_real():
    for step in tour.TARGETED:
        assert step.target in KNOWN_TARGETS
        assert step.screen is None or step.screen in SCREENS
        assert step.tab is None or step.tab in SCREENS
    # every tab gets a step of its own
    assert {step.tab for step in tour.STEPS if step.tab} == SCREENS


def test_the_words_are_for_the_cello():
    words = " ".join(f"{step.title} {step.text}" for step in tour.STEPS)
    assert "C, G, D or A" in words and "C, G, D and A" in words
    assert "bass clef" in words and "how the cello is tuned" in words
    assert "violin" not in words.lower() and "E string" not in words
    assert tour.LAST == "Start week 1"


def test_share_message_points_at_the_cello_listing():
    from stringwise.content import settings
    assert "learning cello" in settings.SHARE_MESSAGE
    assert settings.SHARE_MESSAGE.endswith("id=golemapps.stringwisecello.app")


def test_count_only_counts_spotlit_steps():
    assert layout.count_label(0, tour.STEPS) == ""
    assert layout.count_label(1, tour.STEPS) == "1 of 8"
    assert layout.count_label(8, tour.STEPS) == "8 of 8"
    assert layout.count_label(9, tour.STEPS) == ""


def test_dimming_covers_everything_but_the_hole():
    width, height = 400, 800
    hole = (50, 300, 200, 100)
    cells = layout.dim_cells(hole, width, height)
    covered = sum(w * h for _x, _y, w, h in cells)
    assert covered == width * height - 200 * 100
    for cell in cells:
        assert layout.clip(cell, hole) is None          # nothing dims the hole itself
    assert layout.dim_cells(None, width, height) == [(0, 0, width, height)]


def test_hole_at_the_edge_is_clipped_to_the_window():
    cells = layout.dim_cells((-10, 760, 420, 60), 400, 800)     # e.g. the gear in the title bar
    assert sum(w * h for _x, _y, w, h in cells) == 400 * 800 - 400 * 40


def test_bubble_goes_below_then_above_then_low_over():
    bottom, top, gap = 60, 800, 12
    # room below
    assert layout.place_bubble((0, 500, 400, 100), 200, bottom, top, gap) == 500 - gap - 200
    # no room below, room above
    assert layout.place_bubble((0, 100, 400, 100), 200, bottom, top, gap) == 100 + 100 + gap
    # a tall target leaves no room either side
    assert layout.place_bubble((0, 100, 400, 600), 200, bottom, top, gap) == bottom
    # no target: centred
    assert layout.place_bubble(None, 200, bottom, top, gap) == (bottom + top - 200) / 2


def test_finding_the_page_stops_at_a_window_that_is_its_own_parent():
    window = SimpleNamespace()
    window.parent = window
    page = SimpleNamespace(parent=window, is_page=True)
    child = SimpleNamespace(parent=SimpleNamespace(parent=page))
    lonely = SimpleNamespace(parent=SimpleNamespace(parent=window))
    is_page = lambda w: getattr(w, "is_page", False)
    assert layout.page_of(child, is_page) is page
    assert layout.page_of(lonely, is_page) is None          # ends instead of looping forever
