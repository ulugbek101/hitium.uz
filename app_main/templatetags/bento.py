from django import template

register = template.Library()

BENTO_GRID = "grid grid-cols-2 lg:grid-cols-4 auto-rows-[150px] sm:auto-rows-[190px] lg:auto-rows-[200px] gap-2 lg:gap-3"

SMALL = ""
WIDE = "col-span-2"
BIG = "col-span-2 row-span-2"

# Every block fills whole rows of the 4-column grid (and of the 2-column mobile grid),
# so any combination of blocks leaves no holes. The second variant is the mirrored one.
BLOCKS = {
    5: ([BIG, SMALL, SMALL, SMALL, SMALL], [SMALL, SMALL, BIG, SMALL, SMALL]),
    4: ([SMALL] * 4, [SMALL] * 4),
    3: ([WIDE, SMALL, SMALL], [SMALL, SMALL, WIDE]),
    2: ([WIDE, WIDE], [WIDE, WIDE]),
}
REMAINDER_BLOCKS = {0: [], 1: [3, 3], 2: [2], 3: [3], 4: [4]}


def bento_spans(count):
    """Span classes for `count` tiles: a plain row up to 4 tiles, bento blocks from 5 on."""
    if count <= 4:
        return [SMALL] * count
    full, rest = divmod(count, 5)
    sizes = [5] * full + REMAINDER_BLOCKS[rest]
    if rest == 1:
        sizes.remove(5)  # 5 + 1 is laid out as 3 + 3
    spans = []
    for i, size in enumerate(sizes):
        spans += BLOCKS[size][i % 2]
    return spans


@register.filter
def bento(items):
    """Pair each item with its tile span: {% for item, span in items|bento %}."""
    items = list(items)
    return zip(items, bento_spans(len(items)))


@register.simple_tag
def bento_grid():
    return BENTO_GRID
