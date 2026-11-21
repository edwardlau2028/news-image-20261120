#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summarising Friday 20 November 2026.

Everything is drawn in code with PIL. No external image is used.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 242, 231)      # warm off-white
NAVY = (22, 35, 63)          # masthead band
GOLD = (198, 158, 62)        # masthead date line and rule
INK = (28, 28, 28)           # body text
CARD = (255, 255, 255)
CARD_BORDER = (216, 210, 196)
FOOTER_GREY = (110, 108, 100)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
SERIF_BOLD = FONT_DIR + "NotoSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
SANS_REG = FONT_DIR + "NotoSans-Regular.ttf"

# (tag, colour, headline, summary)
STORIES = [
    ("NATO", (139, 30, 30), "Russian missiles land in Poland",
     "Three objects cross NATO airspace; Rutte calls it a grave violation."),
    ("UKRAINE", (29, 78, 137), "Russian barrage kills 8 in Kyiv",
     "400 drones and 110 missiles hit three bridges and the power grid."),
    ("EUROPE", (46, 107, 79), "UK and EU strike landmark deal",
     "Youth mobility for 100,000 and freer food trade agreed in Brussels."),
    ("MARKETS", (122, 62, 0), "Stocks plunge as AI rout deepens",
     "S&P 500 drops 3.7%; Nasdaq turns negative for the year."),
    ("BALTICS", (91, 45, 142), "Estonia to shut Russia border",
     "Crossings close from Dec 1 for at least six months; Moscow warns."),
    ("PROTESTS", (176, 58, 46), "Italy strikes as Europe protests",
     "General strike in 100 cities; youth march across Europe."),
    ("MIDDLE EAST", (107, 78, 0), "Iraq retakes militia stronghold",
     "Troops enter Jurf al-Sakhar in an oil-smuggling crackdown deal."),
    ("CULTURE", (15, 118, 110), "GTA VI makes $3.79bn in a day",
     "Take-Two hails the biggest entertainment launch in history."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that each fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def wrap_balanced(draw, text, fnt, max_width):
    """Wrap a headline so two lines are as even as possible.

    Greedy wrapping leaves a single orphan word on the second line
    ("Russian missiles land in" / "Poland"); trying every split point
    and keeping the most even pair reads much better.
    """
    words = text.split()
    if len(words) < 2:
        return [text]
    best = None
    for split in range(1, len(words)):
        first = " ".join(words[:split])
        second = " ".join(words[split:])
        w1 = draw.textlength(first, font=fnt)
        w2 = draw.textlength(second, font=fnt)
        if w1 > max_width or w2 > max_width:
            continue
        score = abs(w1 - w2)
        if best is None or score < best[0]:
            best = (score, [first, second])
    if best is not None:
        return best[1]
    return wrap(draw, text, fnt, max_width)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    band_h = 160
    d.rectangle([0, 0, W, band_h], fill=NAVY)
    title_f = font(SERIF_BOLD, 54)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 26), title, font=title_f, fill=(255, 255, 255))
    date_f = font(SANS_BOLD, 28)
    date_line = "FRIDAY \u00b7 20 NOVEMBER 2026"
    dw = d.textlength(date_line, font=date_f)
    d.text(((W - dw) / 2, 102), date_line, font=date_f, fill=GOLD)
    d.rectangle([0, band_h, W, band_h + 4], fill=GOLD)

    # ---- Story grid ------------------------------------------------------
    margin = 40
    gap = 16
    grid_top = 180
    grid_bottom = 960
    grid_left = margin
    grid_right = W - margin
    cols, rows = 2, 4
    card_w = (grid_right - grid_left - gap * (cols - 1)) // cols
    card_h = (grid_bottom - grid_top - gap * (rows - 1)) // rows

    pad = 20
    tag_f = font(SANS_BOLD, 17)
    head_f = font(SERIF_BOLD, 29)
    summ_f = font(SANS_REG, 21)
    head_lh = 35
    summ_lh = 27
    chip_h = 26

    inner_w = card_w - 2 * pad

    for i, (tag, colour, headline, summary) in enumerate(STORIES):
        col = i % cols
        row = i // cols
        x0 = grid_left + col * (card_w + gap)
        y0 = grid_top + row * (card_h + gap)
        x1 = x0 + card_w
        y1 = y0 + card_h

        d.rounded_rectangle([x0, y0, x1, y1], radius=10,
                            fill=CARD, outline=CARD_BORDER, width=1)

        # Tag chip.
        tag_w = d.textlength(tag, font=tag_f) + 22
        chip_x0 = x0 + pad
        chip_y0 = y0 + 12
        d.rounded_rectangle([chip_x0, chip_y0, chip_x0 + tag_w,
                             chip_y0 + chip_h], radius=8, fill=colour)
        d.text((chip_x0 + 11, chip_y0 + 4), tag, font=tag_f,
               fill=(255, 255, 255))

        # Headline, at most 3 lines (balanced wrap avoids orphan words).
        head_lines = wrap_balanced(d, headline, head_f, inner_w)
        assert len(head_lines) <= 3, f"headline too long: {headline!r}"
        hy = chip_y0 + chip_h + 8
        for line in head_lines:
            d.text((x0 + pad, hy), line, font=head_f, fill=INK)
            hy += head_lh

        # Summary, at most 2 lines.
        summ_lines = wrap(d, summary, summ_f, inner_w)
        assert len(summ_lines) <= 2, f"summary too long: {summary!r}"
        sy = hy + 5
        for line in summ_lines:
            d.text((x0 + pad, sy), line, font=summ_f, fill=INK)
            sy += summ_lh

        # Nothing may overflow the card.
        assert sy <= y1 - 6, f"card overflow: {headline!r}"

    # ---- Footer ----------------------------------------------------------
    foot_f = font(SANS_REG, 18)
    src = "Sources: Reuters \u00b7 AP \u00b7 The Times \u00b7 CNN \u00b7 NPR"
    date_note = "All events happened, or were first reported, on 20 November 2026."
    for j, line in enumerate((src, date_note)):
        lw = d.textlength(line, font=foot_f)
        d.text(((W - lw) / 2, 968 + j * 26), line, font=foot_f,
               fill=FOOTER_GREY)

    img.save(OUT, format="PNG", optimize=True)
    return img


if __name__ == "__main__":
    draw_page()
    print("wrote", OUT)
