"""Words for the first-launch tour.

Each step names the screen to open, the bottom tab to outline, and the thing to
spotlight (see ``ui/tour.py`` for what each target name points at). The first and
last steps have no target: they show a bubble in the middle of the dimmed screen.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TourStep:
    title: str
    text: str
    target: str | None = None    # what to spotlight, or None for a centred bubble
    screen: str | None = None    # screen to open first, or None to stay where we are
    tab: str | None = None       # bottom tab to outline


SKIP = "Skip"
NEXT = "Next"
FIRST = "Show me around"
LAST = "Start week 1"

STEPS: tuple[TourStep, ...] = (
    TourStep(
        "Welcome to StringWise Cello",
        "A twelve-week course for beginner cellists, with a tuner, a metronome and a "
        "practice log. Here is a quick look round. It takes under a minute.",
    ),
    TourStep(
        "Tune up first",
        "Tap C, G, D or A, press Start listening and play that open string. The needle "
        "shows whether it is flat or sharp, and green means in tune.",
        target="tuner.dial", screen="tuner", tab="tuner",
    ),
    TourStep(
        "Keep a steady beat",
        "Set a tempo, or tap one in, and press Start. The click keeps going while you move "
        "to other tabs.",
        target="metronome.panel", screen="metronome", tab="metronome",
    ),
    TourStep(
        "Pause it from anywhere",
        "Once the metronome has been started, the beat dots and a Pause button stay up "
        "here, so you can stop and restart the click without leaving the page you are on.",
        target="header.metronome", screen="metronome", tab="metronome",
    ),
    TourStep(
        "One week at a time",
        "Each week has goals, a 60-minute practice plan and two pieces to play along with. "
        "Tick the plan as you go and the next week opens.",
        target="lessons.weeks", screen="lessons", tab="lessons",
    ),
    TourStep(
        "Where the fingers go",
        "A map of first position on all four strings, C, G, D and A. Tap a dot to hear its "
        "note, and use the live check below it to test your own fingers.",
        target="fingers.board", screen="fingers", tab="fingers",
    ),
    TourStep(
        "The reading behind it",
        "Short sections on the bass clef, rhythm, the parts of the bow and how the cello is "
        "tuned. The lessons point you here when you need them.",
        target="theory.first", screen="theory", tab="theory",
    ),
    TourStep(
        "A rhythm a day",
        "A short rhythm to clap and play each day, drawn from the weeks you have reached. "
        "The tempo ladder and a daily routine are further down.",
        target="practice.rhythm", screen="practice", tab="practice",
    ),
    TourStep(
        "Settings",
        "The gear opens Settings: tuning pitch, feedback, sharing, resetting your progress, "
        "and this tour again if you want it.",
        target="header.gear",
    ),
    TourStep(
        "You're ready",
        "Start with week 1: sitting with the cello, the bow hold and your first open "
        "strings. Tune up before every practice.",
    ),
)

# Steps that spotlight something; the bubble counts these ("3 of 8").
TARGETED = tuple(step for step in STEPS if step.target)
