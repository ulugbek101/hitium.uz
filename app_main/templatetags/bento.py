from django import template

register = template.Library()

BENTO_GRID = "grid grid-cols-2 lg:grid-cols-4 auto-rows-[150px] sm:auto-rows-[190px] lg:auto-rows-[200px] gap-2 lg:gap-3"

SMALL = ""
WIDE = "col-span-2"
BIG = "col-span-2 row-span-2"
HERO = "col-span-2 lg:col-span-4 row-span-2"

# Every block fills whole rows of the 4-column grid (and of the 2-column mobile grid),
# so any combination of blocks leaves no holes. The second variant is the mirrored one.
BLOCKS = {
    5: ([BIG, SMALL, SMALL, SMALL, SMALL], [SMALL, SMALL, BIG, SMALL, SMALL]),
    4: ([SMALL] * 4, [SMALL] * 4),
    3: ([WIDE, SMALL, SMALL], [SMALL, SMALL, WIDE]),
    2: ([WIDE, WIDE], [WIDE, WIDE]),
}
REMAINDER_BLOCKS = {0: [], 1: [3, 3], 2: [2], 3: [3], 4: [4]}

# Opening blocks of a featured grid: the first tile is always the big one, and each block fills whole rows too.
FEATURED_HEADS = {
    0: [],
    1: [HERO],
    2: [BIG, BIG],
    3: [BIG, WIDE, WIDE],
    4: [BIG, WIDE, SMALL, SMALL],
    5: BLOCKS[5][0],
}


def block_sizes(count):
    """Split `count` tiles (0 or 2 and more) into block sizes, as many 5-tile blocks as possible."""
    full, rest = divmod(count, 5)
    sizes = [5] * full + REMAINDER_BLOCKS[rest]
    if rest == 1:
        sizes.remove(5)  # 5 + 1 is laid out as 3 + 3
    return sizes


def block_spans(sizes, start=0):
    """Span classes for consecutive blocks, alternating plain and mirrored variants from block number `start`."""
    spans = []
    for i, size in enumerate(sizes, start):
        spans += BLOCKS[size][i % 2]
    return spans


def bento_spans(count):
    """Span classes for `count` tiles: a plain row up to 4 tiles, bento blocks from 5 on."""
    if count <= 4:
        return [SMALL] * count
    return block_spans(block_sizes(count))


def featured_bento_spans(count):
    """Span classes for `count` tiles where the first one is featured: it gets the big tile for any count."""
    head = min(count, 5)
    if count - head == 1:
        head = 4  # a lone tile can't fill a row, so 6 is laid out as 4 + 2
    # The head block has its big tile on the left, so the blocks after it start from the mirrored variant
    return FEATURED_HEADS[head] + block_spans(block_sizes(count - head), start=1)


@register.filter
def bento(items):
    """Pair each item with its tile span: {% for item, span in items|bento %}."""
    items = list(items)
    return zip(items, bento_spans(len(items)))


@register.filter
def featured_bento(items):
    """Like `bento`, but the first item always gets the big tile: {% for item, span in items|featured_bento %}."""
    items = list(items)
    return zip(items, featured_bento_spans(len(items)))


@register.simple_tag
def bento_grid():
    return BENTO_GRID
