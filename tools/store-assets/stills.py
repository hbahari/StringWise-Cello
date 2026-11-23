"""Captures the eight store screens from the running app.

    APP_DIR=/path/to/app xvfb-run -a -s "-screen 0 1700x2900x24" python3 stills.py 1080 1920 3 raw/phone
    ... 1200 2132 2 raw/tab7
    ... 1600 2844 2 raw/tab10

Arguments: window width, height, Kivy density, output folder.
"""
import os
import sys
import time

import common

W, H, DENSITY, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
common.kivy_setup(W, H, DENSITY, OUT)

import numpy as np
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp

from stringwise.app import StringWiseApp
from stringwise.audio.mic import SAMPLE_RATE, SyntheticMic
from stringwise.content.timing import TIMING
from stringwise.music.fingering import STRING_BY_NAME, target_note
from stringwise.music.pieces import PIECES
from test_takecheck import record

OUT = os.path.join(common.HERE, OUT)
os.makedirs(OUT, exist_ok=True)
app = StringWiseApp()
common.skip_tour(app)
scr = lambda name: app.shell.manager.get_screen(name)
OPEN = STRING_BY_NAME[common.SHOW_STRING].open_hz
TUNE = PIECES["hotcrossbuns"].notes


def shot(name):
    Window.screenshot(name=os.path.join(OUT, name + ".png"))


def fake(freqs, each=1.0):
    app.listener._mic_factory = lambda: SyntheticMic(list(freqs), seconds_each=each)


class ReplayMic:
    """Feeds a prepared recording eight times faster than real time."""
    def __init__(self, audio): self.audio, self.pos = audio, 0
    def open(self): self.pos = 0
    def read(self, n):
        time.sleep(n / SAMPLE_RATE / 8)
        chunk = self.audio[self.pos:self.pos + n]; self.pos += n
        return chunk if len(chunk) == n else np.zeros(n, dtype=np.float32)
    def close(self): pass


def until(cond, then, timeout=12.0, every=0.05):
    start = time.time()
    def check(_dt):
        if cond() or time.time() - start > timeout:
            if not cond():
                print("TIMEOUT waiting for", getattr(then, "__name__", then))
            then()
            return False
    Clock.schedule_interval(check, every)


steps = []
def step(delay, fn): steps.append((delay, fn))
def nxt(_dt=0):
    if steps:
        d, fn = steps.pop(0)
        Clock.schedule_once(lambda dt: fn(), d)
def go(fn):
    def wrapped(): fn(); nxt()
    return wrapped


# 1 tuner, open A just in tune
def tuner_start():
    fake([common.cents(OPEN, 2)]); app.go_to("tuner"); scr("tuner").toggle_listening()
step(1.0, go(tuner_start))
step(1.6, go(lambda: shot("01-tuner")))
step(0.2, go(lambda: scr("tuner").stop_listening()))

# 2 lessons, week 4 scrolled to its first piece
def lessons():
    app.go_to("lessons"); scr("lessons").show_week(4)
def lessons_scroll():
    L = scr("lessons"); L.page.scroll_to(L.lesson_box.children[-2], padding=dp(12), animate=False)
step(0.2, go(lessons)); step(0.5, go(lessons_scroll)); step(0.5, go(lambda: shot("02-lessons")))

# 3 play-along: three notes right, the fourth played as a different note (red dot)
def pa_start():
    wrong = common.cents(TUNE[3].freq, -200)
    fake([TUNE[0].freq, TUNE[1].freq, TUNE[2].freq, wrong, wrong, wrong])
    app.open_play_along("hotcrossbuns"); scr("playalong").toggle_listening()
    Clock.schedule_once(lambda dt: common.scroll_top(scr("playalong").page, scr("playalong").picker), 0.2)
step(0.3, go(pa_start))
def pa_wait():
    P = scr("playalong")
    until(lambda: P.logic.view.index == 3 and P.logic.view.cursor_step is not None
          and P.logic.view.cursor_kind == "wrong",
          lambda: Clock.schedule_once(lambda dt: (shot("03-play-along"),
                  Clock.schedule_once(lambda dt: (P.stop_listening(), nxt()), 0.3)), 0.6))
step(0.5, pa_wait)

# 4 timing lesson with the metronome running in the title bar
def timing():
    app.go_to("lessons"); L = scr("lessons"); L.show_week(5); L._start_metronome(TIMING[5], 66)
def timing_scroll():
    L = scr("lessons"); L.page.scroll_to(L.lesson_box.children[-4], padding=dp(12), animate=False)
step(0.3, go(timing)); step(0.5, go(timing_scroll))
def beat_shot(name):
    def wait():
        until(lambda: (app.metronome.beat_state() or (9,))[0] == 0 and 0.1 < app.metronome.beat_state()[3] < 0.35,
              lambda: (shot(name), nxt()), every=0.01)
    return wait
step(0.4, beat_shot("04-timing-lesson"))

# 5 metronome tab
step(0.2, go(lambda: (app.go_to("metronome"), app.metronome.ensure_running(bpm=72, subdivide=False, gaps=False))))
step(0.5, beat_shot("05-metronome"))
step(0.2, go(lambda: app.metronome.stop()))

# 6 record and check: one late note and one sharp note
audio = record(TUNE, 66, shift={1: 0.2}, cents={4: 46})
def take_start():
    app.open_take(4); T = scr("take")
    T.picker.text = next(v for v in T.picker.values if "Hot Cross" in v)
    app.metronome.configure(bpm=66)
    app.listener._mic_factory = lambda: ReplayMic(audio); T._pressed()
step(0.3, go(take_start))
step(len(audio) / SAMPLE_RATE / 8 + 1.2, go(lambda: scr("take")._finish()))
def take_wait():
    T = scr("take")
    def done():
        common.scroll_top(T.page, T.picker)
        Clock.schedule_once(lambda dt: (shot("06-record-and-check"), nxt()), 0.6)
    until(lambda: T.state == "idle" and len(T.results.children) > 0,
          lambda: Clock.schedule_once(lambda dt: done(), 0.3))
step(0.3, take_wait)

# 7 finger map
step(0.3, go(lambda: (app.go_to("fingers"), setattr(scr("fingers").page, "scroll_y", 1))))
step(0.6, go(lambda: shot("07-fingers")))

# 8 live finger check, settled on a correct note
def check_start():
    F = scr("fingers"); F._choose(string=common.SHOW_STRING, finger=common.CHECK_FINGER)
    fake([common.cents(target_note(common.SHOW_STRING, common.CHECK_FINGER).freq, 1)]); F.toggle_listening()
    Clock.schedule_once(lambda dt: F.page.scroll_to(F.mic_button, padding=dp(24), animate=False), 0.2)
step(0.2, go(check_start))
def check_wait():
    F = scr("fingers")
    until(lambda: F.logic.view.settled,
          lambda: Clock.schedule_once(lambda dt: (shot("08-finger-check"), F.stop_listening(), nxt()), 0.2))
step(0.6, check_wait)
step(0.5, lambda: app.stop())
Clock.schedule_once(nxt, 0.5)
app.run()
