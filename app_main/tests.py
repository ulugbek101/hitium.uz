from django.test import SimpleTestCase

from .templatetags.bento import BIG, HERO, bento_spans, featured_bento_spans


def tile_size(span, desktop):
    """(columns, rows) a tile takes on mobile or, with the lg: classes applied, on desktop."""
    size = {"col": 1, "row": 1}
    for cls in sorted(span.split(), key=lambda cls: cls.startswith("lg:")):
        if cls.startswith("lg:") and not desktop:
            continue
        axis, _, count = cls.removeprefix("lg:").rpartition("-span-")
        size[axis] = int(count)
    return size["col"], size["row"]


def area(row, col, width, height):
    return {(row + dr, col + dc) for dr in range(height) for dc in range(width)}


def place(spans, columns, desktop):
    """Cells taken by the tiles when CSS grid auto-places them row by row, as the browser does."""
    taken = set()
    row = col = 0
    for span in spans:
        width, height = tile_size(span, desktop)
        while col + width > columns or area(row, col, width, height) & taken:
            col += 1
            if col + width > columns:
                row, col = row + 1, 0
        taken |= area(row, col, width, height)
        col += width
    return taken


class BentoLayoutTests(SimpleTestCase):
    def assert_no_holes(self, spans):
        for columns, desktop in ((2, False), (4, True)):
            taken = place(spans, columns, desktop)
            rows = max((r for r, _ in taken), default=-1) + 1
            self.assertEqual(taken, {(r, c) for r in range(rows) for c in range(columns)},
                             f"{len(spans)} tiles leave holes in the {columns}-column grid")

    def test_featured_fills_whole_rows_for_any_count(self):
        for count in range(41):
            spans = featured_bento_spans(count)
            self.assertEqual(len(spans), count)
            self.assert_no_holes(spans)

    def test_featured_first_tile_is_big(self):
        for count in range(1, 41):
            self.assertIn(featured_bento_spans(count)[0], (BIG, HERO))

    def test_bento_fills_whole_rows_from_five(self):
        for count in range(5, 41):
            self.assert_no_holes(bento_spans(count))
