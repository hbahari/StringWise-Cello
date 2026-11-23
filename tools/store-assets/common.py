"""Shared set-up for the store-asset scripts.

Set APP_DIR to the app's project folder (the one with main.py). Every script runs the
real app headless under xvfb-run and feeds it simulated playing, so nothing is mocked up.
"""
import json
import os
import sys

APP_DIR = os.path.abspath(os.environ.get("APP_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)
sys.path.insert(0, os.path.join(APP_DIR, "tests"))     # test_takecheck.record() simulates a take

# Text that names the instrument.
APP_NAME = "StringWise Cello"
TAGLINE = "A cello tutor that listens."
FEATURE_LINE = "Tuner  •  Lessons  •  Metronome  •  Play-along"
HEAD_FONT = os.path.join(APP_DIR, "stringwise", "assets", "fonts", "CrimsonText-SemiBold.ttf")

# The string and finger used for the tuner, finger map and finger check captures.
# Cello first position in this course uses fingers 1, 3 and 4, so the check shows finger 3.
SHOW_STRING = "A"
CHECK_FINGER = 3


def kivy_setup(width, height, density, tag):
    os.environ["KIVY_NO_ARGS"] = "1"
    os.environ["KIVY_METRICS_DENSITY"] = str(density)
    os.environ["KIVY_HOME"] = os.path.join(HERE, "kivyhome_" + tag.replace("/", "_"))
    from kivy.config import Config
    Config.set("graphics", "width", str(width))
    Config.set("graphics", "height", str(height))


def skip_tour(app):
    """Mark the first-launch tour as seen, so it doesn't cover the screens being captured.
    Call before app.run()."""
    folder = app.user_data_dir
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "progress.json")
    data = {}
    try:
        with open(path) as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        pass
    data["tour"] = {"done": True}
    with open(path, "w") as handle:
        json.dump(data, handle)


def scroll_top(page, widget, offset=12, animate=0.0):
    """Scroll a Page so the top of ``widget`` sits ``offset`` dp below the top of the page."""
    from kivy.animation import Animation
    from kivy.metrics import dp
    body = page.body
    distance = body.to_window(body.x, body.top)[1] - widget.to_window(widget.x, widget.top)[1]
    spare = body.height - page.height
    target = 1.0 if spare <= 0 else max(0.0, min(1.0, 1 - (distance - dp(offset)) / spare))
    if animate:
        Animation(scroll_y=target, duration=animate, t="in_out_quad").start(page)
    else:
        page.scroll_y = target


def cents(freq, amount):
    return freq * 2 ** (amount / 1200)
