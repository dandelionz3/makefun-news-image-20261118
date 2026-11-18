#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

One image summing up the world's news of Wednesday 18 November 2026:
lead story (US-Iran exchanges of fire) + four panels (APEC trilateral,
Nvidia, Deutsche Bank leak, EU Ukraine loan) + an ALSO TODAY strip.
Wording verified against live reporting on 18 November 2026; claims are
attributed where the sources attribute them (IRGC drone claims vs
US/Bahrain interceptions, the confirmed trilateral, the EU proposal).

Deterministic: fixed text, fixed layout, no network, no timestamps.
Run: python3 draw_infographic.py  ->  entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
LEAD_BLUE = (27, 42, 74)
STRIP_DARK = (17, 17, 17)
STEEL = (143, 163, 200)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
assert os.path.exists(FONT_BOLD), "bold font missing"
assert os.path.exists(FONT_REG), "regular font missing"


def font(bold, size):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            assert cur, "single word wider than panel"
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        assert draw.textlength(ln, font=fnt) <= max_w, "line overflows: %r" % ln
    return lines


def fit_text(draw, text, max_w, max_h, sizes, leading_extra=5):
    """Largest font size from sizes whose wrapped text fits max_w x max_h."""
    for size in sizes:
        fnt = font(False, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) * (size + leading_extra) <= max_h:
            return fnt, lines, size
    raise AssertionError("text does not fit %dx%d: %r" % (max_w, max_h, text[:60]))


def draw_lines(draw, lines, x, y, fnt, fill, leading_extra=5):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading_extra
    return y


def draw_icon(draw, kind, x, y, w, h, colour):
    """Simple geometric icon (rectangles / lines / polygons only)."""
    if kind == "tanker":
        draw.rectangle([x, y + h - 12, x + 150, y + h - 3], fill=(120, 30, 25))
        draw.polygon([(x + 150, y + h - 12), (x + 172, y + h - 3),
                      (x + 150, y + h - 3)], fill=(120, 30, 25))
        for i, cw in enumerate((26, 22, 26)):
            draw.rectangle([x + 12 + i * 34, y + h - 26, x + 12 + i * 34 + cw,
                            y + h - 12], fill=(90, 90, 96))
        draw.polygon([(x + 96, y + 2), (x + 102, y + 12), (x + 90, y + 12)],
                     fill=(230, 120, 20))
        draw.line([x + 180, y + h - 6, x + 210, y + h - 6], fill=(90, 110, 150), width=2)
        draw.line([x + 190, y + h - 1, x + 216, y + h - 1], fill=(90, 110, 150), width=2)
    elif kind == "flags":
        for i, fc in enumerate(((29, 78, 216), (180, 35, 24), (21, 128, 61))):
            px = x + 24 + i * 64
            draw.line([px, y + 2, px, y + h - 2], fill=INK, width=3)
            draw.rectangle([px, y + 2, px + 42, y + 18], fill=fc)
    elif kind == "bank":
        draw.polygon([(x + 8, y + 10), (x + 62, y + 2), (x + 116, y + 10)],
                     fill=(110, 100, 80))
        for i in range(3):
            cx0 = x + 16 + i * 36
            draw.rectangle([cx0, y + 12, cx0 + 10, y + h - 6], fill=(110, 100, 80))
        draw.rectangle([x + 8, y + h - 6, x + 116, y + h - 2], fill=(110, 100, 80))
        draw.polygon([(x + 140, y + 2), (x + 156, y + 26), (x + 124, y + 26)],
                     fill=(230, 180, 20))
        draw.text((x + 140, y + 8), "!", font=font(True, 14), fill=INK, anchor="ma")
    elif kind == "chip":
        draw.rectangle([x + 8, y + 4, x + 34, y + 30], fill=(40, 40, 44))
        draw.rectangle([x + 14, y + 10, x + 28, y + 24], fill=(90, 160, 220))
        for i in range(3):
            draw.rectangle([x + 12 + i * 8, y, x + 15 + i * 8, y + 4], fill=(40, 40, 44))
            draw.rectangle([x + 12 + i * 8, y + 30, x + 15 + i * 8, y + 34],
                           fill=(40, 40, 44))
        pts = [(x + 48, y + 28), (x + 72, y + 20), (x + 92, y + 22),
               (x + 116, y + 8), (x + 140, y + 4)]
        draw.line(pts, fill=(21, 128, 61), width=3)
        draw.polygon([(x + 140, y + 4), (x + 130, y + 2), (x + 132, y + 12)],
                     fill=(21, 128, 61))
    elif kind == "files":
        # two stacked documents + red exclamation stamp
        draw.rectangle([x + 22, y + 6, x + 118, y + h - 2], fill=(226, 222, 210),
                       outline=(120, 116, 106), width=1)
        draw.rectangle([x + 8, y + 2, x + 104, y + h - 6], fill=WHITE,
                       outline=(120, 116, 106), width=1)
        for i, ly in enumerate((y + 8, y + 15, y + 22)):
            draw.line([x + 16, ly, x + 96, ly], fill=(90, 90, 96), width=2)
        draw.ellipse([x + 128, y + 2, x + 156, y + 30], fill=(180, 35, 24))
        draw.text((x + 142, y + 16), "!", font=font(True, 18), fill=WHITE, anchor="mm")


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 28
report = []

# --- Masthead: black band + title ---
mast_y, mast_h = 20, 70
d.rectangle([MX, mast_y, W - MX, mast_y + mast_h], fill=INK)
d.text((W // 2, mast_y + mast_h // 2), "THE WORLD IN ONE DAY",
       font=font(True, 46), fill=WHITE, anchor="mm")
# --- Dateline ---
date_y = mast_y + mast_h + 6
d.text((W // 2, date_y + 14), "WEDNESDAY, 18 NOVEMBER 2026",
       font=font(True, 26), fill=INK, anchor="mm")

# --- Lead story: full-width dark-blue panel ---
lead_y, lead_h = 130, 276
d.rectangle([MX, lead_y, W - MX, lead_y + lead_h], fill=LEAD_BLUE)
lx, lw = MX + 16, W - 2 * MX - 32
d.text((lx, lead_y + 16), "U.S. AND IRAN TRADE FIRE",
       font=font(True, 52), fill=WHITE)
summary_y = lead_y + 16 + 64 + 8
icon_h = 40
icon_y = lead_y + lead_h - icon_h - 8
avail_h = icon_y - 6 - summary_y
lead_summary = (
    "Iran fires drones at a U.S. radar base in Bahrain, its third strike on "
    "American targets there in five days. Bahrain and U.S. forces say every "
    "drone was intercepted, with no damage. U.S. jets hit a missile site on "
    "Iran's Qeshm Island in reply, and Bahrain sounds a fresh alert overnight.")
sum_f, sum_lines, sum_size = fit_text(d, lead_summary, lw, avail_h, [22, 21, 20, 19])
draw_lines(d, sum_lines, lx, summary_y, sum_f, WHITE)
report.append(("LEAD", "U.S. AND IRAN TRADE FIRE", 52, sum_size, len(sum_lines)))
# radar + drone motif: dish with signal arcs, drone silhouette, blast star
ix0, ix1, iy = lx, lx + lw, icon_y
# radar mast + dish
d.line([ix0 + 30, iy + 38, ix0 + 30, iy + 8], fill=STEEL, width=4)
d.polygon([(ix0 + 30, iy + 4), (ix0 + 62, iy + 14), (ix0 + 30, iy + 18)],
          fill=STEEL)
for r in (14, 24, 34):
    d.arc([ix0 + 62 - r, iy + 20 - r, ix0 + 62 + r, iy + 20 + r],
          start=-70, end=70, fill=WHITE, width=2)
# drone: body + 4 rotors, mid-right
dx, dy = ix0 + 560, iy + 12
d.rectangle([dx, dy + 8, dx + 44, dy + 18], fill=WHITE)
d.line([dx - 8, dy + 4, dx + 52, dy + 4], fill=WHITE, width=2)
d.line([dx - 8, dy + 22, dx + 52, dy + 22], fill=WHITE, width=2)
d.ellipse([dx - 12, dy, dx - 4, dy + 8], fill=WHITE)
d.ellipse([dx + 48, dy, dx + 56, dy + 8], fill=WHITE)
d.ellipse([dx - 12, dy + 18, dx - 4, dy + 26], fill=WHITE)
d.ellipse([dx + 48, dy + 18, dx + 56, dy + 26], fill=WHITE)
# motion dashes behind the drone
for mx in (dx - 70, dx - 50, dx - 30):
    d.line([mx, dy + 13, mx + 12, dy + 13], fill=STEEL, width=2)
# blast star at the far right
bx0, by0 = ix0 + 800, iy + 20
for ang in range(0, 360, 45):
    import math
    x2 = bx0 + int(16 * math.cos(math.radians(ang)))
    y2 = by0 + int(16 * math.sin(math.radians(ang)))
    d.line([bx0, by0, x2, y2], fill=(230, 180, 20), width=3)
d.ellipse([bx0 - 6, by0 - 6, bx0 + 6, by0 + 6], fill=(230, 180, 20))

# --- 2x2 grid ---
panels = [
    ("APEC: THREE-WAY SUMMIT", (29, 78, 216),
     "Trump arrives in Shenzhen for APEC. On Thursday he meets Xi and Putin in "
     "the first three-way summit of the great powers, with nuclear arms at the "
     "top of the agenda.", "flags"),
    ("NVIDIA SAYS NO TO HUANG", (21, 128, 61),
     "Nvidia reports record revenue of $115.8 billion, up 103%, and shares jump "
     "5% after hours. But the board says it will not reinstate founder Jensen "
     "Huang as CEO, despite backing from Trump and Musk.", "chip"),
    ("DEUTSCHE BANK LEAK", (180, 35, 24),
     "More than 15 million leaked files show Deutsche Bank kept Russian oligarch "
     "clients despite staff warnings, and flagged $600 million in suspicious "
     "Epstein-linked payments. Shares fall.", "files"),
    ("EU SEEKS \u20ac45BN FOR KYIV", (90, 60, 140),
     "The European Commission puts a \u20ac45 billion loan for Ukraine to EU "
     "leaders on Wednesday, covering about two-thirds of Kyiv's extra \u20ac70 "
     "billion budget gap for 2027.", "bank"),
]
cell_w, cell_h, gap = 474, 212, 14
grid_y = 418
for i, (head, colour, body, icon) in enumerate(panels):
    cx = MX + (i % 2) * (cell_w + gap)
    cy = grid_y + (i // 2) * (cell_h + gap)
    d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=WHITE,
                outline=(200, 196, 186), width=1)
    d.rectangle([cx, cy, cx + cell_w, cy + 38], fill=colour)
    d.text((cx + 14, cy + 19), head, font=font(True, 25), fill=WHITE, anchor="lm")
    bx, bw = cx + 14, cell_w - 28
    by = cy + 38 + 8
    icon_h2 = 30
    icon_y2 = cy + cell_h - icon_h2 - 6
    avail = icon_y2 - 6 - by
    bf, blines, bsize = fit_text(d, body, bw, avail, [20, 19, 18, 17, 16])
    draw_lines(d, blines, bx, by, bf, INK)
    report.append(("PANEL %d" % (i + 1), head, 25, bsize, len(blines)))
    draw_icon(d, icon, bx, icon_y2, bw, icon_h2, colour)

# --- ALSO TODAY strip ---
strip_y, strip_h = 868, 118
d.rectangle([MX, strip_y, W - MX, strip_y + 28], fill=STRIP_DARK)
d.text((MX + 14, strip_y + 14), "ALSO TODAY", font=font(True, 20),
       fill=WHITE, anchor="lm")
items = [
    "U.S. loses measles elimination status after 26 years; 5,412 cases in 2026",
    "Britain sanctions Israeli settlement firms in two-state push",
    "Canada and China extend trade deals as Xi meets Carney",
    "Cyclone Akvan set to strengthen in the Bay of Bengal",
    "Dhoni retires from IPL; to mentor Chennai Super Kings",
    "U.S. presses U.N. agency over Taiwan flight rules; China hits back",
]
body_y = strip_y + 28 + 8
col_w = (W - 2 * MX - 2 * 14) // 3
row_h = 2 * (14 + 4)
for idx, item in enumerate(items):
    col, row = idx % 3, idx // 3
    ix = MX + 14 + col * (col_w + 14)
    iy2 = body_y + row * row_h
    fnt = font(False, 14)
    lines = wrap(d, "\u2022 " + item, fnt, col_w)
    assert len(lines) <= 2, "strip item too long: %r" % item
    draw_lines(d, lines, ix, iy2, fnt, INK, leading_extra=4)
report.append(("STRIP", "ALSO TODAY (6 items, 3 cols x 2 rows)", 20, 14, 2))

img.save("entry.png", format="PNG")
size = os.path.getsize("entry.png")
assert img.size == (1024, 1024)
assert size <= 1048576, "entry.png too big: %d" % size
print("entry.png: %dx%d px, %d bytes" % (img.size[0], img.size[1], size))
print("LAYOUT REPORT")
for name, head, hsize, bsize, nlines in report:
    print("  %s: headline %dpt, body %dpt, %d lines -- %s"
          % (name, hsize, bsize, nlines, head))
