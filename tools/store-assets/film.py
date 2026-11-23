"""Films the running app: one short clip per feature, written to video/.

    APP_DIR=/path/to/app xvfb-run -a -s "-screen 0 1300x1400x24" python3 film.py
"""
import os
import subprocess
import time

import common

W, H, FPS = 720, 1280, 15
common.kivy_setup(W, H, 2, "film")

import numpy as np
from kivy.clock import Clock
from kivy.graphics.opengl import GL_RGBA, GL_UNSIGNED_BYTE, glReadPixels
from kivy.metrics import dp

from stringwise.app import StringWiseApp
from stringwise.audio.mic import SAMPLE_RATE
from stringwise.content.timing import TIMING
from stringwise.music.fingering import STRING_BY_NAME, target_note
from stringwise.music.pieces import PIECES
from test_takecheck import record

HERE = common.HERE
os.makedirs(os.path.join(HERE, "video"), exist_ok=True)
app = StringWiseApp()
common.skip_tour(app)
scr = lambda name: app.shell.manager.get_screen(name)
STRING = common.SHOW_STRING
OPEN = STRING_BY_NAME[STRING].open_hz
TUNE = PIECES["hotcrossbuns"].notes


class Recorder:
    """Reads the window every frame and pipes it into ffmpeg at a constant frame rate."""
    def start(self, name):
        self.path = os.path.join(HERE, "video", name + ".part.mp4")
        self.final = os.path.join(HERE, "video", name + ".mp4")
        self.proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-vf", "vflip", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "12",
             "-pix_fmt", "yuv420p", self.path], stdin=subprocess.PIPE)
        self.t0, self.written = time.monotonic(), 0
        self.event = Clock.schedule_interval(self.grab, 1 / FPS)
    def grab(self, _dt):
        due = int((time.monotonic() - self.t0) * FPS) + 1 - self.written
        if due <= 0:
            return
        frame = glReadPixels(0, 0, W, H, GL_RGBA, GL_UNSIGNED_BYTE)
        for _ in range(due):
            self.proc.stdin.write(frame)
        self.written += due
    def stop(self):
        self.event.cancel(); self.proc.stdin.close(); code = self.proc.wait()
        if code == 0:
            os.replace(self.path, self.final)
        print("clip", os.path.basename(self.final), self.written, "frames, exit", code)
rec = Recorder()


class ScriptMic:
    """Plays (frequency, seconds) pairs like a bowed string; a (from, to) frequency glides."""
    def __init__(self, script): self.script = script
    def open(self):
        parts = []
        for freq, seconds in self.script:
            n = int(seconds * SAMPLE_RATE); t = np.arange(n) / SAMPLE_RATE
            if freq is None:
                parts.append(np.zeros(n)); continue
            f = np.linspace(freq[0], freq[1], n) if isinstance(freq, tuple) else np.full(n, float(freq))
            phase = 2 * np.pi * np.cumsum(f) / SAMPLE_RATE
            wave = sum(np.sin(k * phase) / k for k in (1, 2, 3, 4))
            env = np.minimum(1, t / 0.03) * np.minimum(1, (seconds - t) / 0.05)
            parts.append(0.05 * wave * env)
        self.audio = np.concatenate(parts).astype(np.float32); self.pos = 0
    def read(self, n):
        time.sleep(n / SAMPLE_RATE)
        chunk = self.audio[self.pos:self.pos + n]; self.pos += n
        return chunk if len(chunk) == n else np.zeros(n, dtype=np.float32)
    def close(self): pass
def mic(script): app.listener._mic_factory = lambda: ScriptMic(script)


class ReplayMic:
    def __init__(self, audio): self.audio, self.pos = audio, 0
    def open(self): self.pos = 0
    def read(self, n):
        time.sleep(n / SAMPLE_RATE / 8)
        chunk = self.audio[self.pos:self.pos + n]; self.pos += n
        return chunk if len(chunk) == n else np.zeros(n, dtype=np.float32)
    def close(self): pass


steps = []
def step(delay, fn): steps.append((delay, fn))
def nxt(_dt=0):
    if steps:
        d, fn = steps.pop(0); Clock.schedule_once(lambda dt: (fn(), nxt()), d)
CLIP = 5.6
def clip(name, setup, during=()):
    step(0.4, setup)
    step(0.5, lambda: rec.start(name))
    last = 0.0
    for at, action in during:
        step(at - last, action); last = at
    step(CLIP - last, rec.stop)


# 1 tuner: a flat A slides up into tune
clip("1-tuner", lambda: (mic([(None, 0.5), ((common.cents(OPEN, -52), common.cents(OPEN, 1)), 2.6),
                               (common.cents(OPEN, 1), 4.0)]),
                          app.go_to("tuner"), scr("tuner").toggle_listening()))
step(0.1, lambda: scr("tuner").stop_listening())
# 2 lessons: week 4, scrolling to the sheet music
def lessons(): app.go_to("lessons"); scr("lessons").show_week(4)
clip("2-lessons", lessons, [(1.2, lambda: common.scroll_top(scr("lessons").page, scr("lessons").lesson_box.children[-2], animate=2.4))])
# 3 play-along: the tune played correctly
def playalong():
    script = [(None, 0.6)] + [x for n in TUNE for x in ((n.freq, 0.42 * n.beats), (None, 0.08))]
    mic(script); app.open_play_along("hotcrossbuns"); scr("playalong").toggle_listening()
    Clock.schedule_once(lambda dt: common.scroll_top(scr("playalong").page, scr("playalong").picker), 0.2)
clip("3-play-along", playalong)
step(0.1, lambda: scr("playalong").stop_listening())
# 4 timing lesson, metronome starting in the title bar
def timing():
    app.go_to("lessons"); L = scr("lessons"); L.show_week(5)
    Clock.schedule_once(lambda dt: common.scroll_top(L.page, L.lesson_box.children[-4]), 0.2)
clip("4-timing", timing, [(0.9, lambda: scr("lessons")._start_metronome(TIMING[5], 66)),
                          (1.6, lambda: common.scroll_top(scr("lessons").page, scr("lessons").lesson_box.children[-4], offset=-150, animate=2.0))])
# 5 metronome tab, tempo change
clip("5-metronome", lambda: (app.go_to("metronome"), app.metronome.ensure_running(bpm=72, subdivide=False, gaps=False)),
     [(2.6, lambda: app.metronome.configure(bpm=96))])
step(0.1, lambda: app.metronome.stop())
# 6 record and check: run a take off camera, then film the result
audio = record(TUNE, 66, shift={1: 0.2}, cents={4: 46})
def take():
    app.open_take(4); T = scr("take"); T.picker.text = next(v for v in T.picker.values if "Hot Cross" in v)
    app.metronome.configure(bpm=66); app.listener._mic_factory = lambda: ReplayMic(audio); T._pressed()
step(0.3, take)
step(len(audio) / SAMPLE_RATE / 8 + 1.2, lambda: scr("take")._finish())
step(2.5, lambda: common.scroll_top(scr("take").page, scr("take").picker))
clip("6-take", lambda: None, [(1.8, lambda: common.scroll_top(scr("take").page, scr("take").scroller, offset=4, animate=2.2))])
# 7 finger map, tapping notes up the A string
def tap(string, finger):
    board = next(w for w in scr("fingers").walk() if w.__class__.__name__ == "Fingerboard")
    board._pressed = (string, finger); board._draw(); Clock.schedule_once(board._release, 0.45)
clip("7-fingers", lambda: (app.go_to("fingers"), setattr(scr("fingers").page, "scroll_y", 1)),
     [(0.8, lambda: tap(STRING, 0)), (1.5, lambda: tap(STRING, 1)), (2.2, lambda: tap(STRING, 2)),
      (2.9, lambda: tap(STRING, 3)), (3.6, lambda: tap(STRING, 4))])
# 8 finger check: a sharp finger slides into place
def check():
    F = scr("fingers"); F._choose(string=STRING, finger=common.CHECK_FINGER)
    target = target_note(STRING, common.CHECK_FINGER).freq
    mic([(None, 0.5), ((common.cents(target, 55), common.cents(target, 1)), 2.4), (common.cents(target, 1), 4.0)])
    F.toggle_listening()
    Clock.schedule_once(lambda dt: F.page.scroll_to(F.mic_button, padding=dp(24), animate=False), 0.2)
clip("8-check", check)
step(0.3, app.stop)
Clock.schedule_once(nxt, 0.8)
app.run()
