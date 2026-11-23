"""The first-launch tour: a dimmed screen with one thing lit up and a note beside it.

The overlay sits on top of the whole window and takes every touch, so the app
underneath cannot be used until the tour is finished or skipped. Each step opens
its screen, scrolls the target into view, cuts a hole in the dimming around it,
outlines the matching bottom tab, and puts a paper bubble below or above the hole.
"""

from __future__ import annotations

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout

from .. import theme
from ..content import tour as text
from ..logic import tour_layout as layout
from ..theme import rgba
from .widgets import Box, Btn, Page, Txt, small, subtitle

DIM = 0.74             # how dark everything outside the spotlight gets
SETTLE = 0.12          # seconds to let a screen switch or a scroll lay itself out


def _find_class(root, class_name):
    for widget in root.walk(restrict=True):
        if type(widget).__name__ == class_name:
            return widget
    return None


def target_widget(app, target):
    """The widget a step's target name points at, or None if it cannot be found."""
    if not target:
        return None
    shell = app.shell
    if target == "header.gear":
        return shell.gear
    if target == "header.metronome":
        return shell.header_metronome
    screen_name, _, _part = target.partition(".")
    try:
        screen = shell.manager.get_screen(screen_name)
    except Exception:
        return None
    if target == "tuner.dial":
        return getattr(screen, "dial", None)
    if target == "metronome.panel":
        bar = _find_class(screen, "MetronomeBar")
        return bar.parent if bar is not None else None
    if target == "lessons.weeks":
        return getattr(screen, "chip_scroller", None)
    if target == "fingers.board":
        return _find_class(screen, "Fingerboard")
    if target == "theory.first":
        sections = getattr(screen, "sections", None)
        return sections[0]["header"] if sections else None
    if target == "practice.rhythm":
        picker = getattr(screen, "rhythm_picker", None)
        return picker.parent if picker is not None else None
    return None


def window_rect(widget):
    x, y = widget.to_window(widget.x, widget.y)
    return float(x), float(y), float(widget.width), float(widget.height)


class Tour(FloatLayout):
    def __init__(self, app, on_finish, steps=text.STEPS, **kwargs):
        super().__init__(size_hint=(None, None), size=Window.size, **kwargs)
        self.app = app
        self.steps = steps
        self.on_finish = on_finish
        self.index = -1
        self.hole = None
        self._shown_header_metronome = False
        self._pending = None

        with self.canvas.before:
            self._dim_color = Color(*rgba(theme.WOOD_DEEP, DIM))
            self._cells = [Rectangle(size=(0, 0)) for _ in range(4)]
        with self.canvas:
            self._hole_color = Color(*rgba(theme.CREAM))
            self._hole_line = Line(width=dp(1.6))
            self._tab_color = Color(*rgba(theme.WARN_LIGHT))
            self._tab_line = Line(width=dp(1.8))

        self.bubble = Box(bg=theme.PAPER, border=theme.PAPER_LINE, padding=dp(16), spacing=dp(10),
                          size_hint=(None, None), radius=14)
        self.heading = subtitle("")
        self.body = Txt("")
        self.skip_button = Btn(text.SKIP, kind="outline", height=dp(42), size_hint_x=None, width=dp(84),
                               on_release=lambda _b: self.skip())
        self.count = small("", halign="center")
        self.next_button = Btn(text.NEXT, height=dp(42), size_hint_x=None, width=dp(132),
                               on_release=lambda _b: self.next())
        from kivy.uix.boxlayout import BoxLayout
        buttons = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(42), spacing=dp(8))
        buttons.add_widget(self.skip_button)
        buttons.add_widget(self.count)
        buttons.add_widget(self.next_button)
        for widget in (self.heading, self.body, buttons):
            self.bubble.add_widget(widget)
        self.add_widget(self.bubble)
        self.bubble.bind(height=lambda *_: self._place_bubble())
        Window.bind(size=self._on_resize)

    # -- lifecycle ----------------------------------------------------------------
    def start(self):
        Window.add_widget(self)
        self.show(0)

    def next(self):
        if self.index >= len(self.steps) - 1:
            self._close(completed=True)
        else:
            self.show(self.index + 1)

    def skip(self):
        self._close(completed=False)

    def _close(self, completed):
        if self._pending is not None:
            self._pending.cancel()
        self._leave_step()
        Window.unbind(size=self._on_resize)
        if self.parent is not None:
            self.parent.remove_widget(self)
        self.on_finish(completed)

    # -- steps ----------------------------------------------------------------------
    def show(self, index):
        self._leave_step()
        self.index = index
        step = self.steps[index]
        last = index == len(self.steps) - 1
        self.heading.set(step.title)
        self.body.set(step.text)
        self.count.set(layout.count_label(index, self.steps))
        self.next_button.text = text.FIRST if index == 0 else text.LAST if last else text.NEXT
        self.next_button.width = dp(160) if (index == 0 or last) else dp(110)
        self.skip_button.disabled = last
        self.skip_button.opacity = 0 if last else 1      # after disabled, which fades the button

        if step.screen:
            self.app.go_to(step.screen)
        widget = target_widget(self.app, step.target)
        if step.target == "header.metronome" and not self.app.metronome.used:
            # Show the title-bar control for this step so there is something to point at.
            widget.opacity = 1.0
            self._shown_header_metronome = True
        if step.target == "lessons.weeks" and widget is not None:
            widget.scroll_x = 0
        page = layout.page_of(widget, lambda w: isinstance(w, Page)) if widget is not None else None
        if page is not None:
            page.scroll_to(widget, padding=dp(24), animate=False)
        self.hole = None
        self._draw()          # dim straight away; the hole appears once things settle
        self._pending = Clock.schedule_once(lambda _dt: self._settled(widget, page), SETTLE)

    def _settled(self, widget, page):
        self._pending = None
        hole = None
        if widget is not None and widget.get_root_window() is not None:
            hole = layout.grow(window_rect(widget), dp(6))
            if page is not None:
                hole = layout.clip(hole, window_rect(page))
        self.hole = hole
        self._draw()

    def _leave_step(self):
        if self._shown_header_metronome:
            self._shown_header_metronome = False
            self.app.shell.header_metronome.sync()

    # -- drawing ------------------------------------------------------------------
    def _on_resize(self, _window, size):
        self.size = size
        if 0 <= self.index < len(self.steps):
            self.show(self.index)

    def _draw(self):
        self.size = Window.size
        cells = layout.dim_cells(self.hole, self.width, self.height)
        for rect, cell in zip(self._cells, cells + [(0, 0, 0, 0)] * 4):
            rect.pos, rect.size = cell[:2], cell[2:]
        if self.hole is not None:
            self._hole_color.a = 1
            self._hole_line.rounded_rectangle = (*self.hole, dp(10))
        else:
            self._hole_color.a = 0
        tab = self.steps[self.index].tab if self.index >= 0 else None
        button = self.app.shell.nav_buttons.get(tab) if tab else None
        if button is not None:
            self._tab_color.a = 1
            self._tab_line.rounded_rectangle = (*layout.grow(window_rect(button), -dp(3)), dp(8))
        else:
            self._tab_color.a = 0
        self._place_bubble()

    def _place_bubble(self):
        width = min(self.width - dp(32), dp(440))
        self.bubble.width = width
        self.bubble.x = (self.width - width) / 2
        nav = next(iter(self.app.shell.nav_buttons.values()), None)
        bottom = (window_rect(nav)[1] + nav.height if nav is not None else 0) + dp(10)
        top = self.height - dp(10)
        self.bubble.y = layout.place_bubble(self.hole, self.bubble.height, bottom, top, dp(12))

    # -- touches: the bubble gets them, nothing underneath does ----------------------
    def on_touch_down(self, touch):
        if self.bubble.collide_point(*touch.pos):
            super().on_touch_down(touch)
        return True

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        return True

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        return True
