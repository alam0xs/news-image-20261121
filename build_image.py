#!/usr/bin/env python3
"""Draw poster v3 for news-image-20261121 (1024x1024, RGB, <=1 MiB).

v3 keeps the v2 font recipe (Ivan: "fontnya jelek" -> DM Serif Display +
Lato, verified from rank 1-3) but swaps the procedural vector panels for
the 13 ChatGPT illustrations Ivan sent, and makes the art panels TALLER
(Ivan: v2 panels were too thin/pipih). Hero art 324x165 (~2:1, was 84px
in v2), mid art 190x100 (~1.9:1, was 40px in v2). Header strips and the
map/briefs area are tightened to pay for the taller art; all 34 stories,
the 6-number band, map, DATE CHECK and footer are kept. Hierarchy:
  1. Date headline: DM Serif Display, one line, very large, black.
  2. Subheadline: DM Serif Display Italic, red, smaller.
  3. ALL long text (kickers, descriptions, briefs, sources, labels):
     Lato (Regular / Bold / Black), never serif.
Layout is deliberately re-ordered vs rank 1-3 (numbers BEFORE the
timeline; black top bar with split masthead; region bar under the
timeline), but the font hierarchy is the same.
Stories/facts unchanged from brief-muse.txt (imported from build_image.py).
Build-time only: Pillow here, never at runtime (repo/main.py decodes).
Deterministic: fixed data, fixed fonts, no timestamps, no randomness.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont

from build_image import (  # data only; importing does not build v1
    HEROES, MIDS, BAND, BRIEFS, PINS, DOTS, DATE_CHECK, CONTINENTS,
    REGION_COLOURS,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "chatgpt-images")
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry-1024-v4.png")

# ---------------------------------------------------------------- palette
PAPER = (244, 237, 224)
INK = (21, 21, 21)
RULE = (43, 43, 43)
NAVY = (18, 35, 74)
RED = (179, 38, 30)
GREY = (74, 74, 74)
HEADLINE = (16, 16, 16)      # #101010 -- card headlines, near-black
DESC = (92, 92, 92)          # #5C5C5C -- card descriptions, clear grey
BRIEF = (85, 85, 85)         # #555555 -- briefs list text
SRC = (119, 119, 119)        # #777777 -- small source lines
LIGHTGREY = (120, 116, 104)
BAND_BG = (238, 230, 212)
LAND = (203, 196, 175)
LAND_EDGE = (138, 132, 113)
DOT_GREY = (140, 135, 120)
CREAM = (244, 237, 224)

# ---------------------------------------------------------------- fonts (OFL)
DM = os.path.join(FONTS, "DMSerifDisplay-Regular.ttf")
DM_I = os.path.join(FONTS, "DMSerifDisplay-Italic.ttf")
LATO = os.path.join(FONTS, "Lato-Regular.ttf")
LATO_B = os.path.join(FONTS, "Lato-Bold.ttf")
LATO_X = os.path.join(FONTS, "Lato-Black.ttf")
LATO_I = os.path.join(FONTS, "Lato-Italic.ttf")
for p in (DM, DM_I, LATO, LATO_B, LATO_X, LATO_I):
    assert os.path.exists(p), p


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, s, f_path, size, max_w, max_lines, min_size=9):
    while size >= min_size:
        f = font(f_path, size)
        lines = wrap(draw, s, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = font(f_path, min_size)
    return f, wrap(draw, s, f, max_w)[:max_lines]


def fit_one_line(draw, s, f_path, size, max_w, min_size=10):
    while size >= min_size:
        f = font(f_path, size)
        if text_w(draw, s, f) <= max_w:
            return f
        size -= 1
    return font(f_path, min_size)


def draw_tracked(draw, s, f, x, y, fill, tracking=-1):
    """Draw one line with tight letter tracking (v4 date headline)."""
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx


def tracked_w(draw, s, f, tracking=-1):
    return sum(draw.textlength(ch, font=f) + tracking for ch in s) - tracking


def crop_cover(im, tw, th, bias=0.42):
    w, h = im.size
    target = tw / th
    cur = w / h
    if cur > target:
        nw = int(h * target)
        x0 = (w - nw) // 2
        box = (x0, 0, x0 + nw, h)
    else:
        nh = int(w / target)
        y0 = int((h - nh) * bias)
        box = (0, y0, w, y0 + nh)
    return im.crop(box).resize((tw, th), Image.LANCZOS)


# ---------------------------------------------------------------- extra data
# Timeline: only UTC times verified in the brief (§3/§7).
TIMELINE = [
    ("02:35", "Wall Street close confirmed"),
    ("04:00", "\u2018El Chapo\u2019 to Mexico City"),
    ("05:00", "First tanker struck, Khasab"),
    ("05:50", "Second tanker near Hormuz"),
    ("12:30", "Riemann debate (AP)"),
]
# Source lines per card (from the brief's source lists), small caps Lato.
HERO_SOURCES = [
    "REUTERS \u00b7 WSJ \u00b7 CNN",
    "CNN \u00b7 AP \u00b7 UNITED24",
    "AP \u00b7 CNN \u00b7 MEXICAN DEFENCE MINISTRY",
]
MID_SOURCES = [
    "REUTERS \u00b7 AP \u00b7 NPR",
    "REUTERS \u00b7 THE TIMES",
    "UKMTO VIA AP \u00b7 AL JAZEERA",
    "REUTERS \u00b7 AL JAZEERA",
    "BBC \u00b7 THE TIMES",
    "ISW \u00b7 REUTERS \u00b7 CNN",
    "AP \u00b7 NATURE \u00b7 BBC",
    "GUARDIAN \u00b7 BBC",
    "REUTERS \u00b7 TBS",
    "SAPS VIA BBC",
]


# Mid descriptions tightened (same facts as the brief) so each one ends as a
# complete sentence in 2 Lato lines -- v2's first pass cut several mid-sentence.
MID_DESCS = [
    "Talks ran into a second day of overtime, ~200 countries split over fossil fuels.",
    "Three Russian objects came down in south-east Poland. No one was hurt.",
    "Two tankers were struck near the Strait of Hormuz on Saturday morning, hours apart.",
    "Saudi defences downed three Houthi missiles fired at Riyadh early on Saturday.",
    "Britain and the EU agreed three post-Brexit deals, including a 100,000-a-year youth scheme.",
    "Two drones struck the sanctioned cargo ship Sparta II; all 16 crew were evacuated.",
    "An Anthropic mathematician claims its AI proved the Riemann hypothesis. No proof yet.",
    "In a 61-patient trial, daraxonrasib plus chemo shrank or cleared tumours in six in ten.",
    "An Israeli strike hit a vehicle carrying food in Gaza City on Saturday, killing three people.",
    "Police figures: 581 women murdered in July\u2013September, 13 dumped near Johannesburg.",
]


def build():
    W, H = 1024, 1024
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    MX = 14

    # ---------------------------------------------------------------- top bar
    # Modification vs rank 1-3: black bar, split left/right, no red centre.
    d.rectangle([0, 0, W, 16], fill=INK)
    f_top = font(LATO_X, 11)
    d.text((MX, 1), "THE WORLD IN ONE DAY", font=f_top, fill=CREAM)
    right = "34 STORIES  \u00b7  9 REGIONS  \u00b7  ALL TIMES UTC"
    f_top2 = font(LATO_B, 10)
    d.text((W - MX - text_w(d, right, f_top2), 2), right,
           font=f_top2, fill=CREAM)

    # ---------------------------------------------------------------- date headline
    # DM Serif Display, one line, very large, black (rank recipe).
    f_date = fit_one_line(d, "Saturday 21 November 2026", DM, 80,
                          W - 2 * MX, min_size=60)
    dw = tracked_w(d, "Saturday 21 November 2026", f_date)
    draw_tracked(d, "Saturday 21 November 2026", f_date,
                 (W - dw) / 2, -11, INK)
    # Subheadline: DM Serif Italic, red (rank recipe, our own wording).
    sub = "Markets fall, a cartel boss falls, and the climate talks stall."
    f_sub = fit_one_line(d, sub, DM_I, 17, W - 2 * MX, min_size=12)
    d.text(((W - text_w(d, sub, f_sub)) / 2, 93), sub,
           font=f_sub, fill=RED)
    d.line([(MX, 118), (W - MX, 118)], fill=INK, width=2)
    d.line([(MX, 121), (W - MX, 121)], fill=INK, width=1)

    # ---------------------------------------------------------------- number band
    # Modification vs rank: numbers come BEFORE the timeline. Figures in
    # red DM Serif (rank recipe); labels in Lato Bold.
    band_y0, band_y1 = 126, 156
    d.rectangle([MX, band_y0, W - MX, band_y1], fill=BAND_BG)
    d.line([(MX, band_y0), (W - MX, band_y0)], fill=INK, width=1)
    d.line([(MX, band_y1), (W - MX, band_y1)], fill=INK, width=1)
    cell_w = (W - 2 * MX) / 6
    for i, (fig, label) in enumerate(BAND):
        cx = MX + cell_w * (i + 0.5)
        f_fig = fit_one_line(d, fig, DM, 18, cell_w - 10, min_size=16)
        d.text((cx - text_w(d, fig, f_fig) / 2, band_y0 + 2), fig,
               font=f_fig, fill=RED)
        f_lab = fit_one_line(d, label, LATO_B, 7, cell_w - 8, min_size=6)
        d.text((cx - text_w(d, label, f_lab) / 2, band_y0 + 21), label,
               font=f_lab, fill=GREY)
        if i:
            x = MX + cell_w * i
            d.line([(x, band_y0 + 4), (x, band_y1 - 4)], fill=LIGHTGREY, width=1)

    # ---------------------------------------------------------------- timeline
    # Tightened to ONE line per entry (time + short label) to pay for the
    # taller art; times/labels are the same verified facts as v2.
    tl_y0, tl_y1 = 160, 176
    d.rectangle([MX, tl_y0, MX + 108, tl_y1], fill=INK)
    f_tl = font(LATO_X, 10)
    d.text((MX + 8, tl_y0 + 3), "THE DAY IN UTC", font=f_tl, fill=CREAM)
    tl_x0 = MX + 118
    tl_w = (W - MX) - tl_x0
    cell = tl_w / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        x = tl_x0 + cell * i
        f_t = font(LATO_X, 10)
        d.text((x + 4, tl_y0 + 3), t, font=f_t, fill=RED)
        tx = x + 4 + text_w(d, t, f_t) + 5
        f_l = fit_one_line(d, label, LATO, 9, (x + cell - 4) - tx, min_size=8)
        d.text((tx, tl_y0 + 4), label, font=f_l, fill=INK)
        if i:
            d.line([(x, tl_y0 + 3), (x, tl_y1 - 3)], fill=LIGHTGREY, width=1)

    # ---------------------------------------------------------------- region bar
    counts = {}
    for _, region, _, _, _, _ in HEROES + MIDS:
        counts[region] = counts.get(region, 0) + 1
    order = ["Europe", "Middle East", "Americas", "World", "Africa"]
    total = sum(counts[r] for r in order)
    rb_y0, rb_y1 = 180, 190
    x = MX
    f_rb = font(LATO_X, 8)
    for r in order:
        w_seg = (W - 2 * MX) * counts[r] / total
        col = REGION_COLOURS[r]
        d.rectangle([x, rb_y0, x + w_seg, rb_y1], fill=col)
        lab = f"{r.upper()} {counts[r]}"
        tw = text_w(d, lab, f_rb)
        if tw < w_seg - 6:
            d.text((x + (w_seg - tw) / 2, rb_y0 + 1), lab,
                   font=f_rb, fill=CREAM)
        x += w_seg

    # ---------------------------------------------------------------- art + chips
    panels = {}
    for i in range(1, 14):
        panels[i] = Image.open(os.path.join(ART, f"panel{i:02d}.png")).convert("RGB")

    def card_box(draw, x, y, w, h):
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)

    def chip(draw, x, y, label, region):
        col = REGION_COLOURS[region]
        f_chip = font(LATO_X, 10)
        draw.rectangle([x + 5, y + 3, x + 12, y + 10], fill=col)
        draw.text((x + 16, y + 1), label, font=f_chip, fill=col)

    def badge(draw, x, y, text, col):
        f_b = font(LATO_X, 8)
        tw = text_w(draw, text, f_b)
        draw.rectangle([x - tw - 10, y + 1, x - 2, y + 11], fill=col)
        draw.text((x - tw - 6, y + 2), text, font=f_b, fill=CREAM)

    # ---------------------------------------------------------------- heroes
    hero_y0, hero_h = 196, 295
    hero_xs = [14, 349, 684]
    hero_w = 326
    for idx, (label, region, head, desc, number, panel) in enumerate(HEROES):
        x = hero_xs[idx]
        y = hero_y0
        card_box(d, x, y, hero_w, hero_h)
        chip(d, x, y, label, region)
        badge(d, x + hero_w, y, "CONFIRMED", (46, 125, 79))
        art = crop_cover(panels[idx + 1], hero_w - 2, 160)
        im.paste(art, (x + 1, y + 15))
        f_head, head_lines = fit_lines(d, head, LATO_X, 20, hero_w - 14, 2,
                                       min_size=16)
        hy = y + 183
        for ln in head_lines:
            d.text((x + 7, hy), ln, font=f_head, fill=HEADLINE)
            hy += int(f_head.size * 1.12)
        f_desc, desc_lines = fit_lines(d, desc, LATO, 11, hero_w - 14, 3)
        dy = hy + 3  # dynamic: right under the headline, never over the number
        for ln in desc_lines:
            d.text((x + 7, dy), ln, font=f_desc, fill=DESC)
            dy += 13
        if number:
            d.line([(x + 7, y + hero_h - 24), (x + hero_w - 8, y + hero_h - 24)],
                   fill=LIGHTGREY, width=1)
            f_num = fit_one_line(d, number, LATO_X, 11, hero_w - 14)
            d.text((x + 7, y + hero_h - 21), number, font=f_num, fill=NAVY)
        f_src = fit_one_line(d, HERO_SOURCES[idx], LATO_B, 8, hero_w - 14,
                             min_size=7)
        d.text((x + 7, y + hero_h - 11), HERO_SOURCES[idx], font=f_src,
               fill=SRC)

    # ---------------------------------------------------------------- mids (5 x 2)
    mid_h, mid_w = 190, 192
    mid_xs = [14, 212, 410, 608, 806]
    mid_ys = [497, 693]
    for idx, (label, region, head, _desc, number, panel) in enumerate(MIDS):
        desc = MID_DESCS[idx]
        row, col = divmod(idx, 5)
        x = mid_xs[col]
        y = mid_ys[row]
        card_box(d, x, y, mid_w, mid_h)
        chip(d, x, y, label, region)
        badge(d, x + mid_w, y, "CLAIM" if idx == 6 else "CONFIRMED",
              (179, 38, 30) if idx == 6 else (46, 125, 79))
        art = crop_cover(panels[idx + 4], mid_w - 2, 100)
        im.paste(art, (x + 1, y + 13))
        f_head, head_lines = fit_lines(d, head, LATO_X, 12, mid_w - 10, 3,
                                       min_size=10)
        hy = y + 117
        for ln in head_lines:
            d.text((x + 5, hy), ln, font=f_head, fill=HEADLINE)
            hy += int(f_head.size * 1.18)
        f_desc, desc_lines = fit_lines(d, desc, LATO, 9, mid_w - 10, 2,
                                       min_size=8)
        dy = hy + 2
        for ln in desc_lines:
            d.text((x + 5, dy), ln, font=f_desc, fill=DESC)
            dy += 10
        if number:
            f_num = fit_one_line(d, number, LATO_X, 9, mid_w - 10, min_size=8)
            d.text((x + 5, y + mid_h - 10), number, font=f_num, fill=NAVY)

    # ---------------------------------------------------------------- map + briefs
    map_x0, map_y0, map_w, map_h = 14, 903, 330, 90
    f_map_t = font(LATO_X, 11)
    d.text((map_x0, 889), "WHERE IT HAPPENED", font=f_map_t, fill=INK)
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                outline=RULE, width=1)

    def project(lon, lat):
        px = map_x0 + (lon + 180.0) / 360.0 * map_w
        py = map_y0 + (78.0 - lat) / 136.0 * map_h
        return px, py

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)

    pin_centres = []
    for i, (lon, lat, dx, dy) in enumerate(PINS, 1):
        px, py = project(lon, lat)
        cx, cy = px + dx, py + dy
        pin_centres.append((cx, cy))
        if dx or dy:
            d.line([(px, py), (cx, cy)], fill=NAVY, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=NAVY)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=NAVY, outline=PAPER,
                  width=1)
        f_pin = font(LATO_X, 9 if i < 10 else 8)
        num = str(i)
        d.text((cx - text_w(d, num, f_pin) / 2, cy - 5), num, font=f_pin,
               fill=PAPER)
    for lon, lat in DOTS:
        px, py = project(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=DOT_GREY)

    # Legend counts live in the region bar above; no room for a
    # second legend under the shortened map.

    # briefs column (Lato, not serif -- the v1 fix)
    bx0, bx1 = 356, 1010
    f_bhead = font(LATO_X, 13)
    d.text((bx0, 889), "ALSO ON SATURDAY", font=f_bhead, fill=INK)
    col_w = (bx1 - bx0 - 12) // 2
    for i, line in enumerate(BRIEFS):
        col, row = divmod(i, 11)
        x = bx0 + col * (col_w + 12)
        y = 903 + row * 8
        num = f"{i + 1}. "
        f_b = fit_one_line(d, num + line, LATO, 9, col_w, min_size=8)
        d.text((x, y), num, font=f_b, fill=HEADLINE)
        d.text((x + text_w(d, num, f_b), y), line, font=f_b, fill=BRIEF)

    # ---------------------------------------------------------------- DATE CHECK
    dc_y0, dc_y1 = 995, 1013
    d.rectangle([MX, dc_y0, W - MX, dc_y1], outline=RED, width=1)
    f_dc = font(LATO, 8)
    # Same three DATE_CHECK strings, reflowed into 2 lines so the footer
    # below still fits on the 1024 canvas; no words changed.
    dc_lines = [DATE_CHECK[0] + " \u00b7 " + DATE_CHECK[1], DATE_CHECK[2]]
    dy = dc_y0 + 1
    for ln in dc_lines:
        d.text((MX + 6, dy), ln, font=f_dc, fill=RED)
        dy += 8
    footer = ("Every story on this page happened or was first reported on Saturday "
              "21 November 2026, in any time zone.")
    f_foot = fit_one_line(d, footer, LATO, 8, W - 2 * MX)
    d.text(((W - text_w(d, footer, f_foot)) / 2, 1015), footer,
           font=f_foot, fill=GREY)

    im.save(OUT, optimize=True)
    print("wrote", OUT)
    return OUT, pin_centres


if __name__ == "__main__":
    path, pins = build()
    import hashlib
    data = open(path, "rb").read()
    print("size:", len(data), "bytes")
    print("sha256:", hashlib.sha256(data).hexdigest())
    print("mode/size:", Image.open(path).size, Image.open(path).mode)
    worst = 999
    for i in range(len(pins)):
        for j in range(i + 1, len(pins)):
            dist = ((pins[i][0] - pins[j][0]) ** 2 +
                    (pins[i][1] - pins[j][1]) ** 2) ** 0.5
            worst = min(worst, dist)
            if dist < 17:
                print(f"PIN OVERLAP RISK: pins {i + 1} and {j + 1} are "
                      f"{dist:.1f}px apart")
    print(f"closest pin pair: {worst:.1f}px apart (pin diameter 16px)")
