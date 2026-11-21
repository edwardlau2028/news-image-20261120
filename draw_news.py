#!/usr/bin/env python3
"""Render the news-image-20261120 entry: a 1024x1024 newspaper front page
summing up Friday 20 November 2026, drawn with PIL and Noto fonts.

Eight verified stories, two columns by four rows of cards under a navy
masthead. The script measures every headline and summary before drawing and
shrinks the type until all eight cards fit, so the output is deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "entry.png")

CANVAS = (1024, 1024)
PAPER = (247, 242, 231)
NAVY = (20, 38, 74)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
BODY_GREY = (74, 72, 66)
FOOT_GREY = (110, 108, 100)
CARD = (255, 255, 255)
CARD_EDGE = (205, 198, 184)

NOTO = "/usr/share/fonts/truetype/noto"


def serif(size):
    return ImageFont.truetype(os.path.join(NOTO, "NotoSerif-Bold.ttf"), size)


def sans(size):
    return ImageFont.truetype(os.path.join(NOTO, "NotoSans-Regular.ttf"), size)


def sans_bold(size):
    return ImageFont.truetype(os.path.join(NOTO, "NotoSans-Bold.ttf"), size)


# tag, chip colour, headline, one-line summary
STORIES = [
    ("NATO", (31, 78, 121),
     "Russian missiles land in Poland",
     "Three objects cross NATO airspace; Rutte calls it a grave violation."),
    ("UKRAINE", (139, 26, 26),
     "Russian barrage kills 8 in Kyiv",
     "400 drones and 110 missiles hit three bridges and the power grid."),
    ("EUROPE", (67, 56, 202),
     "UK and EU strike landmark deal",
     "Youth mobility for 100,000 and freer food trade agreed in Brussels."),
    ("MARKETS", (14, 116, 144),
     "Stocks plunge as AI rout deepens",
     "S&P 500 drops 3.7%; Nasdaq turns negative for the year."),
    ("BALTICS", (22, 101, 52),
     "Estonia to shut Russia border",
     "Crossings close from Dec 1 for at least six months; Moscow warns."),
    ("PROTESTS", (180, 83, 9),
     "Italy strikes as Europe protests",
     "General strike in 100 cities; youth march across Europe."),
    ("MIDDLE EAST", (157, 23, 77),
     "Iraq retakes militia stronghold",
     "Troops enter Jurf al-Sakhar in an oil-smuggling crackdown deal."),
    ("CULTURE", (87, 83, 78),
     "GTA VI makes $3.79bn in a day",
     "Take-Two hails the biggest entertainment launch in history."),
]


def split_lines(draw, text, font, width):
    """Greedy wrap: pack as many words per line as fit inside width."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            longer = line + " " + word
            if draw.textlength(longer, font=font) <= width:
                line = longer
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def measure_all(draw, head_px, sum_px, inner_w):
    """Wrap every story at the given sizes; return (cards, head font, sum font)."""
    head_font = serif(head_px)
    sum_font = sans(sum_px)
    cards = []
    for tag, colour, headline, summary in STORIES:
        heads = split_lines(draw, headline, head_font, inner_w)
        sums = split_lines(draw, summary, sum_font, inner_w)
        cards.append((tag, colour, heads, sums))
    return cards, head_font, sum_font


def draw_chip(draw, x, y, tag, colour, font):
    """A coloured pill with the tag text, returning its width."""
    label_w = int(draw.textlength(tag, font=font)) + 20
    height = 24
    draw.rounded_rectangle([x, y, x + label_w, y + height],
                           radius=height // 2, fill=colour)
    draw.text((x + 10, y + 3), tag, font=font, fill=(255, 255, 255))
    return label_w


def render():
    page = Image.new("RGB", CANVAS, PAPER)
    draw = ImageDraw.Draw(page)
    width, height = CANVAS

    # Masthead: navy band, centred serif title, gold date line, gold rule.
    draw.rectangle([0, 0, width, 160], fill=NAVY)
    title_font = serif(56)
    title = "THE WORLD IN ONE DAY"
    title_w = draw.textlength(title, font=title_font)
    draw.text(((width - title_w) / 2, 26), title,
              font=title_font, fill=(255, 255, 255))
    date_font = sans_bold(30)
    dateline = "FRIDAY \u00b7 20 NOVEMBER 2026"
    date_w = draw.textlength(dateline, font=date_font)
    draw.text(((width - date_w) / 2, 100), dateline,
              font=date_font, fill=GOLD)
    draw.rectangle([0, 160, width, 164], fill=GOLD)

    # Story grid geometry.
    margin, gap = 40, 20
    top, bottom = 176, 962
    cols, rows = 2, 4
    span_w = width - 2 * margin
    span_h = bottom - top
    cell_w = (span_w - (cols - 1) * gap) // cols
    cell_h = (span_h - (rows - 1) * gap) // rows
    pad = 12
    inner_w = cell_w - 2 * pad

    # Pick the largest type that still fits every card, then draw.
    picked = None
    for head_px, sum_px in [(30, 22), (28, 21), (25, 19)]:
        cards, head_font, sum_font = measure_all(draw, head_px, sum_px, inner_w)
        head_step = int(head_px * 1.18)
        sum_step = int(sum_px * 1.25)
        chip_h = 24
        fits = True
        for _tag, _c, heads, sums in cards:
            if len(heads) > 3 or len(sums) > 2:
                fits = False
                break
            needed = (pad + chip_h + 7 + len(heads) * head_step
                      + 6 + len(sums) * sum_step + pad)
            if needed > cell_h:
                fits = False
                break
        if fits:
            picked = (cards, head_font, sum_font, head_step, sum_step, chip_h)
            break
    assert picked is not None, "no type size fits the cards"
    cards, head_font, sum_font, head_step, sum_step, chip_h = picked
    tag_font = sans_bold(17)

    for index, (tag, colour, heads, sums) in enumerate(cards):
        row, col = divmod(index, cols)
        x0 = margin + col * (cell_w + gap)
        y0 = top + row * (cell_h + gap)
        x1, y1 = x0 + cell_w, y0 + cell_h
        draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                               fill=CARD, outline=CARD_EDGE, width=1)

        # Centre the block vertically so one-line headlines leave no dead band.
        block_h = chip_h + 7 + len(heads) * head_step + 6 + len(sums) * sum_step
        y = y0 + (cell_h - block_h) // 2

        draw_chip(draw, x0 + pad, y, tag, colour, tag_font)
        y += chip_h + 7
        for line in heads:
            draw.text((x0 + pad, y), line, font=head_font, fill=INK)
            y += head_step
        y += 6
        for line in sums:
            draw.text((x0 + pad, y), line, font=sum_font, fill=BODY_GREY)
            y += sum_step
        assert y <= y1 - pad + sum_step, "card content overflow"

    # Footer: sources, then the date note.
    foot_font = sans(15)
    sources = "Sources: Reuters \u00b7 AP \u00b7 The Times \u00b7 CNN \u00b7 NPR"
    src_w = draw.textlength(sources, font=foot_font)
    draw.text(((width - src_w) / 2, 972), sources, font=foot_font, fill=FOOT_GREY)
    note = "All events happened, or were first reported, on 20 November 2026."
    note_w = draw.textlength(note, font=foot_font)
    draw.text(((width - note_w) / 2, 994), note, font=foot_font, fill=FOOT_GREY)

    page.save(TARGET, format="PNG", optimize=True)
    size = os.path.getsize(TARGET)
    print(f"wrote {TARGET}: {width}x{height}, {size} bytes")
    assert size <= 1048576, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    render()
