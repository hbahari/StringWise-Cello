"""Geometry for the tour overlay, kept free of Kivy so it can be tested anywhere.

Rectangles are (x, y, width, height) in window pixels, with y measured up from the
bottom of the window, as Kivy does.
"""

from __future__ import annotations

Rect = tuple[float, float, float, float]


def clip(rect: Rect, area: Rect) -> Rect | None:
    """The part of ``rect`` inside ``area``, or None if they do not overlap."""
    x, y, w, h = rect
    ax, ay, aw, ah = area
    left, bottom = max(x, ax), max(y, ay)
    right, top = min(x + w, ax + aw), min(y + h, ay + ah)
    if right <= left or top <= bottom:
        return None
    return left, bottom, right - left, top - bottom


def grow(rect: Rect, by: float) -> Rect:
    x, y, w, h = rect
    return x - by, y - by, w + 2 * by, h + 2 * by


def dim_cells(hole: Rect | None, width: float, height: float) -> list[Rect]:
    """Rectangles that cover the whole window except ``hole``.

    The window is cut into a strip below the hole, a strip above it, and the pieces
    to its left and right. With no hole, one rectangle covers everything.
    """
    if hole is None:
        return [(0.0, 0.0, width, height)]
    hole = clip(hole, (0.0, 0.0, width, height))
    if hole is None:
        return [(0.0, 0.0, width, height)]
    x, y, w, h = hole
    cells = [
        (0.0, 0.0, width, y),                       # below
        (0.0, y + h, width, height - (y + h)),      # above
        (0.0, y, x, h),                             # left
        (x + w, y, width - (x + w), h),             # right
    ]
    return [cell for cell in cells if cell[2] > 0 and cell[3] > 0]


def place_bubble(hole: Rect | None, bubble_height: float, bottom: float, top: float,
                 gap: float) -> float:
    """The y of the bubble's bottom edge.

    Below the highlight if it fits between the highlight and ``bottom``, otherwise
    above it if it fits under ``top``, otherwise low on the screen over the highlight.
    With no highlight the bubble is centred.
    """
    if hole is None:
        return max(bottom, (bottom + top - bubble_height) / 2)
    _x, y, _w, h = hole
    below = y - gap - bubble_height
    if below >= bottom:
        return below
    above = y + h + gap
    if above + bubble_height <= top:
        return above
    return bottom


def count_label(index: int, steps) -> str:
    """'3 of 8' for steps with a target, counting only those; '' for the others."""
    if not steps[index].target:
        return ""
    targeted = [i for i, step in enumerate(steps) if step.target]
    return f"{targeted.index(index) + 1} of {len(targeted)}"


def page_of(widget, is_page):
    """The nearest ancestor for which ``is_page`` is true, or None.

    The Kivy Window is its own parent, so walking up ``parent`` never reaches None
    at the top. A seen-set stops the walk.
    """
    seen = set()
    node = getattr(widget, "parent", None)
    while node is not None and id(node) not in seen:
        if is_page(node):
            return node
        seen.add(id(node))
        node = getattr(node, "parent", None)
    return None
