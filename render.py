#!/usr/bin/env python3
"""Render the 18 November 2026 front page: 45 stories, one page.

Fresh dense layout for the news-image-20261118 v2 entry. Drawn with PIL
and DejaVu fonts; no network, deterministic output.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
NAVY = (15, 29, 61)
GOLD = (198, 164, 92)
GOLD_LT = (216, 201, 138)
RED = (178, 34, 34)
INK = (26, 26, 26)
GREY = (90, 88, 80)
TEAL = (18, 92, 96)
CREAM = (250, 247, 236)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF_I = lambda s: ImageFont.truetype(
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, font, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, width, fill, leading=None):
    """Draw wrapped paragraph; return y just below the last line."""
    leading = leading or int(font.size * 1.22)
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def badge(draw, cx, cy, n, r=11):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = SANS_B(13)
    t = str(n)
    tw = draw.textlength(t, font=f)
    draw.text((cx - tw / 2, cy - 9), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, kick="MIDDLE EAST · WAR",
         head="US and Iran trade fire over Bahrain and Qeshm",
         body="US jets struck an Iranian missile site on Qeshm after drones "
              "hit a US radar in Bahrain. No injuries reported.",
         scene="gulf"),
    dict(n=2, kick="EUROPE · WAR IN UKRAINE",
         head="A span of the Crimea bridge falls into the sea",
         body="Kyiv says a second strike in two days destroyed the road arch; "
              "Moscow says it downed 1,441 drones.",
         scene="bridge"),
    dict(n=3, kick="ASIA · DIPLOMACY",
         head="Trump meets Quad leaders, then flies to Shenzhen",
         body="Talks and a working lunch in Manila, a day after the first Quad "
              "summit in two years.",
         scene="quad"),
]

SMALL = [
    dict(n=4, kick="UNITED STATES · BUSINESS",
         head="Nvidia's revenue doubles to $115.8bn",
         body="Sales rose 103% as data-centre demand held up. The board says it "
              "does not intend to bring back Jensen Huang.",
         icon="chip"),
    dict(n=5, kick="SOUTH ASIA · WEATHER",
         head="Cyclone Akvan bears down on Andhra Pradesh",
         body="The storm is forecast to make landfall on Friday with gusts to "
              "145 km/h. Odisha is moving 200,000 people from the coast.",
         icon="storm"),
    dict(n=6, kick="ISRAEL · POLITICS",
         head="Knesset elects Kahana as speaker, 66–52",
         body="Kahana, an ally of Gadi Eisenkot, replaces Amir Ohana after a "
              "seven-hour debate. Arab parties' votes proved decisive.",
         icon="house"),
    dict(n=7, kick="EUROPE · UKRAINE",
         head="EU proposes a €45bn loan for Ukraine",
         body="The loan would cover about two-thirds of Kyiv's 2027 gap and be "
              "repaid only if Russia pays reparations.",
         icon="euro"),
    dict(n=8, kick="RUSSIA · CRASH",
         head="Russian An-12 crashes in Siberia; 19 dead",
         body="All 19 aboard died when the transport crashed in Kemerovo region. "
              "Moscow blames a technical fault.",
         icon="plane"),
    dict(n=9, kick="BRITAIN · SANCTIONS",
         head="Britain sanctions settlement builders",
         body="Eight Israeli firms and aid-blocking group Tzav 9 face asset "
              "freezes and director bans.",
         icon="scales"),
]

ALSO = [
    "China cuts tariffs as Xi meets Carney.",
    "Dhoni ends IPL career — CSK mentor in 2027.",
    "Voyager 1 reaches one light-day.",
    "Gaza warning — truce may collapse, Board fears.",
    "COP31 heat plan — $20m for heat and cooling.",
    "France protests — 146,000 march in 4th weekend.",
    "Freezer blackout — cyber-attack hits 7 countries.",
    "Settler sanctions — Australia lists 7 firms.",
    "Sudan drone toll — UN: 1,630 civilians killed.",
    "Tanker attacked — TARA GAS hit; 1 seafarer missing.",
    "Ukraine toll — UN: 372 killed in October.",
    "Japan scrambles jets — two Russian planes.",
    "NSA network down — maintenance fault, no hack.",
    "Apple outage — iCloud, App Store, Pay hit.",
    "Tech bets slashed — biggest cut since 2006.",
    "Senegal qualify — first team into AFCON 2027.",
    "SAFF final — India beat Pakistan 2–1.",
    "Journalist killed in Costa Rica, first in 25 yrs.",
    "Guinea crackdown — 224 jailed over gold mining.",
    "Jordan–Iraq block Telegram on security fears.",
    "US presses UN agency over Taiwan flight curbs.",
    "US widens chip export scrutiny to SE Asia.",
    "Baidu chief warns of AI 'bubble' before APEC.",
    "ITU — India re-elected to Council 2027–30.",
    "Jay Shah re-elected ICC chair, second term.",
    "ASEAN — Japan offers access to energy storage.",
    "Waymo — California bans robotaxis from freeways.",
    "Grammys — Raye leads nominations with 11.",
    "Australia pay gap falls below 20%.",
    "Thailand — US–Thailand reciprocal trade deal.",
    "Korea — IMF raises growth forecast to 3.9%.",
    "US intel: Iran plotted 'dirty bomb' — CLAIM.",
    "Romania quake — magnitude 5.3 in Vrancea.",
    "Indonesia fires — haze chokes region; apology.",
    "Estonia shuts Russia border crossings 1 Dec.",
    "S&P 500 down for fourth straight day.",
]

FIGURES = [
    ("66–52", "Kahana's margin for speaker"),
    ("$115.8bn", "Nvidia revenue, up 103%"),
    ("145 km/h", "Akvan's gusts at landfall"),
    ("200,000", "Odisha evacuations"),
    ("19", "An-12 crash dead"),
]

# Dotted-map land spans: (row, col_start, col_end) on a 48 x 30 grid.
LAND = [
    (2, 8, 13), (2, 17, 19), (2, 38, 55),
    (3, 6, 15), (3, 17, 20), (3, 30, 33), (3, 37, 57),
    (4, 4, 16), (4, 17, 20), (4, 28, 29), (4, 29, 34), (4, 36, 58),
    (5, 3, 16), (5, 29, 35), (5, 36, 58),
    (6, 3, 15), (6, 30, 35), (6, 37, 57),
    (7, 4, 14), (7, 30, 34), (7, 38, 55), (7, 55, 56),
    (8, 5, 14), (8, 31, 33), (8, 39, 53), (8, 56, 57),
    (9, 6, 14), (9, 30, 36), (9, 40, 52),
    (10, 6, 13), (10, 29, 37), (10, 41, 50),
    (11, 7, 12), (11, 29, 38), (11, 41, 49),
    (12, 7, 10), (12, 30, 38), (12, 42, 44), (12, 46, 49),
    (13, 8, 11), (13, 30, 37), (13, 42, 43), (13, 47, 49),
    (14, 9, 11), (14, 31, 36), (14, 47, 48),
    (15, 10, 11), (15, 31, 35), (15, 47, 52),
    (16, 12, 17), (16, 32, 35), (16, 48, 53),
    (17, 12, 18), (17, 32, 34),
    (18, 13, 18), (18, 32, 34),
    (19, 13, 17), (19, 33, 34), (19, 50, 56),
    (20, 14, 17), (20, 50, 57),
    (21, 14, 16), (21, 51, 56),
    (22, 14, 16), (22, 51, 55),
    (23, 15, 16),
    (24, 15, 16), (24, 58, 59),
    (25, 15, 16),
]

# (story number, lon, lat, display d_lon, d_lat) for the map pins.
# Display offsets nudge crowded Europe / Middle East pins apart.
PINS = [
    (1, 50, 26, 5, -2), (2, 36, 45, -3, 4), (3, 121, 14.6, 0, 0),
    (4, -122, 37, 0, 0), (5, 80, 16, 0, 0), (6, 35, 31.8, -7, -4),
    (7, 4, 50.8, 4, -4), (8, 86, 55, 0, 0), (9, -0.1, 51.5, -14, 6),
]


# ---------------------------------------------------------------- scenes
def scene_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 27, 58))
    for sx, sy in [(20, 14), (70, 26), (150, 10), (230, 22), (290, 12)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
    d.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(232, 190, 90))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(16, 84, 96))
    for wx in range(0, w, 46):
        d.line([x + wx, y + h - 18, x + wx + 22, y + h - 18], fill=(120, 200, 210), width=2)
    # warship silhouette on the water
    hx, hy = x + 26, y + h - 30
    d.polygon([(hx, hy), (hx + 150, hy), (hx + 138, hy + 16),
               (hx + 12, hy + 16)], fill=(38, 44, 56))
    d.rectangle([hx + 52, hy - 16, hx + 96, hy], fill=(38, 44, 56))
    d.line([hx + 74, hy - 16, hx + 74, hy - 34], fill=(38, 44, 56), width=3)
    d.line([hx + 74, hy - 34, hx + 92, hy - 26], fill=(38, 44, 56), width=2)
    for wx in range(hx + 58, hx + 92, 10):
        d.rectangle([wx, hy - 12, wx + 4, hy - 8], fill=(255, 220, 120))
    # missile streaks from the right
    d.line([x + 200, y + 16, x + 252, y + 48], fill=(255, 140, 60), width=3)
    d.ellipse([x + 248, y + 44, x + 256, y + 52], fill=(255, 220, 120))
    d.line([x + 262, y + 8, x + 300, y + 34], fill=(255, 140, 60), width=2)


def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.ellipse([x + w - 56, y + 10, x + w - 26, y + 40], fill=(240, 214, 140))
    for cx, cy, r in [(60, 26, 14), (80, 20, 11), (250, 30, 12)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(235, 235, 230))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(52, 110, 138))
    for wx in range(0, w, 40):
        d.line([x + wx, y + h - 14, x + wx + 20, y + h - 14], fill=(150, 200, 215), width=2)
    dy = y + h - 44
    d.rectangle([x + 8, dy, x + w - 8, dy + 5], fill=(70, 70, 78))
    d.arc([x + 20, dy - 34, x + 140, dy + 6], 180, 360, fill=(70, 70, 78), width=4)
    d.arc([x + 168, dy - 34, x + w - 20, dy + 6], 180, 300, fill=(70, 70, 78), width=4)
    d.polygon([(x + 190, dy + 2), (x + 250, dy + 2), (x + 262, dy + 16),
               (x + 200, dy + 18)], fill=(90, 90, 98))
    for cx, cy, r in [(200, 34, 9), (214, 26, 12), (232, 34, 8)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(150, 150, 145))


def scene_quad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(252, 226, 168))
    d.ellipse([x + w - 58, y + 8, x + w - 28, y + 38], fill=(240, 180, 60))
    base = y + h
    for bx, bw, bh in [(0, 42, 34), (48, 30, 52), (84, 46, 40), (136, 30, 58),
                       (172, 44, 36), (222, 34, 50), (262, 44, 30)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(52, 52, 66))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(70, 60, 52))
    flags = [((232, 60, 60), (255, 255, 255), None),
             ((255, 153, 51), (255, 255, 255), (19, 136, 8)),
             ((255, 255, 255), (188, 0, 45), None),
             ((0, 40, 120), (255, 255, 255), None)]
    for i, (c1, c2, c3) in enumerate(flags):
        fx = x + 30 + i * 68
        d.line([fx, y + 16, fx, y + 66], fill=(40, 40, 40), width=2)
        d.rectangle([fx, y + 16, fx + 34, y + 30], fill=c1)
        d.rectangle([fx, y + 30, fx + 34, y + 38], fill=c2)
        if c3:
            d.rectangle([fx, y + 38, fx + 34, y + 46], fill=c3)
        if i == 2:
            d.ellipse([fx + 12, y + 21, fx + 22, y + 31], fill=(188, 0, 45))


SCENES = {"gulf": scene_gulf, "bridge": scene_bridge, "quad": scene_quad}


def icon_chip(d, x, y, s):
    d.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], fill=(16, 110, 70))
    d.rectangle([x + 16, y + 16, x + s - 16, y + s - 16], fill=(120, 220, 170))
    for k in range(3):
        d.line([x + 12 + k * 10, y + 2, x + 12 + k * 10, y + 6], fill=(60, 60, 60), width=2)
        d.line([x + 12 + k * 10, y + s - 6, x + 12 + k * 10, y + s - 2], fill=(60, 60, 60), width=2)
        d.line([x + 2, y + 12 + k * 10, x + 6, y + 12 + k * 10], fill=(60, 60, 60), width=2)
        d.line([x + s - 6, y + 12 + k * 10, x + s - 2, y + 12 + k * 10], fill=(60, 60, 60), width=2)


def icon_storm(d, x, y, s):
    for r in (20, 15, 10, 5):
        d.arc([x + s // 2 - r, y + s // 2 - r, x + s // 2 + r, y + s // 2 + r],
              200 - r * 8, 200 - r * 8 + 260, fill=TEAL, width=3)


def icon_house(d, x, y, s):
    d.polygon([(x + 6, y + 20), (x + s // 2, y + 8), (x + s - 6, y + 20)], fill=(90, 70, 40))
    for k in range(3):
        cx = x + 12 + k * 11
        d.rectangle([cx, y + 22, cx + 5, y + 38], fill=(90, 70, 40))
    d.rectangle([x + 8, y + 38, x + s - 8, y + 42], fill=(90, 70, 40))


def icon_euro(d, x, y, s):
    d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=(20, 50, 140))
    for k in range(8):
        a = math.pi * k / 4
        px = x + s // 2 + int(13 * math.cos(a))
        py = y + s // 2 + int(13 * math.sin(a))
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 215, 0))


def icon_plane(d, x, y, s):
    d.polygon([(x + 6, y + s // 2), (x + s - 14, y + s // 2 - 6),
               (x + s - 6, y + s // 2), (x + s - 14, y + s // 2 + 6)],
              fill=(60, 60, 70))
    d.polygon([(x + 18, y + s // 2 - 4), (x + 30, y + 8), (x + 34, y + s // 2 - 2)],
              fill=(60, 60, 70))
    d.polygon([(x + 20, y + s // 2 + 4), (x + 30, y + s - 10), (x + 34, y + s // 2 + 2)],
              fill=(60, 60, 70))


def icon_scales(d, x, y, s):
    cx = x + s // 2
    d.line([cx, y + 6, cx, y + s - 8], fill=(70, 60, 40), width=3)
    d.line([cx - 14, y + 12, cx + 14, y + 12], fill=(70, 60, 40), width=3)
    for sx in (cx - 14, cx + 14):
        d.line([sx, y + 12, sx, y + 24], fill=(70, 60, 40), width=2)
        d.arc([sx - 8, y + 22, sx + 8, y + 34], 0, 180, fill=(70, 60, 40), width=2)
    d.rectangle([cx - 10, y + s - 8, cx + 10, y + s - 4], fill=(70, 60, 40))


ICONS = {"chip": icon_chip, "storm": icon_storm, "house": icon_house,
         "euro": icon_euro, "plane": icon_plane, "scales": icon_scales}


# ---------------------------------------------------------------- layout
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 116, W, 120], fill=GOLD)
    kick_l = SANS_B(13)
    d.text((14, 12), "THE DAY IN WORLD NEWS", font=kick_l, fill=GOLD_LT)
    badge_txt = "45 STORIES · 6 CONTINENTS · ONE PAGE"
    tw = d.textlength(badge_txt, font=kick_l)
    d.text((W - 14 - tw, 12), badge_txt, font=kick_l, fill=GOLD_LT)
    d.text((14, 30), "Wednesday 18 November 2026", font=SERIF_B(56), fill=(255, 255, 255))
    d.text((14, 94), "Every story below happened, or was first reported, on this day.",
           font=SERIF_I(15), fill=(200, 205, 220))

    # ---- three lead cards ----------------------------------------------
    cw, gap, x0, y0, ch = 322, 12, 12, 130, 212
    for i, s in enumerate(LEADS):
        x = x0 + i * (cw + gap)
        d.rectangle([x, y0, x + cw, y0 + ch], fill=CREAM, outline=(120, 115, 100), width=1)
        SCENES[s["scene"]](d, x + 1, y0 + 1, cw - 2, 92)
        ty = y0 + 100
        badge(d, x + 16, ty + 7, s["n"])
        d.text((x + 32, ty - 2), s["kick"], font=SANS_B(11), fill=RED)
        para(d, x + 12, ty + 18, s["head"], SERIF_B(18), cw - 24, INK, leading=22)
        para(d, x + 12, ty + 64, s["body"], SANS(11.5), cw - 24, GREY, leading=14)

    # ---- six small cards -----------------------------------------------
    sw, sh = 322, 104
    for i, s in enumerate(SMALL):
        row, col = divmod(i, 3)
        x = x0 + col * (cw + gap)
        y = 354 + row * (sh + 10)
        d.rectangle([x, y, x + sw, y + sh], fill=CREAM, outline=(120, 115, 100), width=1)
        ICONS[s["icon"]](d, x + 8, y + 8, 46)
        tx = x + 62
        badge(d, x + sw - 16, y + 16, s["n"], r=10)
        d.text((tx, y + 8), s["kick"], font=SANS_B(10), fill=RED)
        yy = para(d, tx, y + 24, s["head"], SERIF_B(14), sw - 74, INK, leading=17)
        para(d, tx, yy + 2, s["body"], SANS(10.5), sw - 74, GREY, leading=13)

    # ---- figures strip ---------------------------------------------------
    fy = 584
    d.line([12, fy, W - 12, fy], fill=NAVY, width=2)
    d.line([12, fy + 52, W - 12, fy + 52], fill=NAVY, width=2)
    d.text((14, fy + 8), "BY THE", font=SANS_B(12), fill=RED)
    d.text((14, fy + 24), "NUMBERS", font=SANS_B(12), fill=RED)
    fx = 130
    fw = (W - 12 - fx) // 5
    for val, cap in FIGURES:
        d.text((fx, fy + 4), val, font=SERIF_B(24), fill=NAVY)
        para(d, fx, fy + 34, cap, SANS(10), fw - 10, GREY, leading=12)
        fx += fw

    # ---- bottom zone: map + also list ------------------------------------
    by = 650
    d.text((14, by), "WHERE THE NEWS HAPPENED", font=SANS_B(13), fill=NAVY)
    mx, my, mw, mh = 16, by + 28, 312, 196
    d.rectangle([mx, my, mx + mw, my + mh], fill=(232, 240, 236),
                outline=(150, 155, 145), width=1)
    # dotted land
    cols, rows = 48, 30
    stepx, stepy = mw / cols, mh / rows
    land = set()
    for r, c0, c1 in LAND:
        for c in range(c0, c1 + 1):
            land.add((r, c))
    for (r, c) in land:
        px = mx + (c + 0.5) * stepx
        py = my + (r + 0.5) * stepy
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(110, 125, 105))
    # pins
    for n, lon, lat, dlon, dlat in PINS:
        px = mx + (lon + dlon + 180) / 360 * mw
        py = my + (85 - (lat + dlat)) / 140 * mh
        badge(d, px, py, n, r=9)
    d.text((14, my + mh + 6),
           "Numbered dots mark stories 1–9.",
           font=SANS(10), fill=GREY)

    ax = 352
    d.text((ax, by), "ALSO ON WEDNESDAY 18 NOVEMBER — 36 MORE STORIES",
           font=SANS_B(13), fill=NAVY)
    d.line([ax, by + 20, W - 12, by + 20], fill=RED, width=2)
    # two columns of 18 items
    col_w = 324
    f_lead = SANS_B(11)
    f_rest = SANS(11)
    for ci in range(2):
        items = ALSO[ci * 18:(ci + 1) * 18]
        cx = ax + ci * (col_w + 12)
        cy = by + 30
        for k, text in enumerate(items):
            num = 10 + ci * 18 + k
            lead = f"{num}. "
            # split item into bold lead-in (up to the em dash) and rest
            if " — " in text:
                head, rest = text.split(" — ", 1)
                rest = " — " + rest
            else:
                head, rest = text, ""
            full = lead + text
            lines = wrap(d, full, f_rest, col_w)
            # draw first line with bold lead-in
            first = lines[0]
            bold_part = lead + head
            if len(first) >= len(bold_part):
                d.text((cx, cy), bold_part, font=f_lead, fill=INK)
                bx = cx + d.textlength(bold_part, font=f_lead)
                d.text((bx, cy), first[len(bold_part):], font=f_rest, fill=INK)
            else:
                d.text((cx, cy), first, font=f_rest, fill=INK)
            cy += 15
            for ln in lines[1:]:
                d.text((cx, cy), ln, font=f_rest, fill=INK)
                cy += 15
            cy += 1  # small gap between items

    # ---- footer ------------------------------------------------------------
    d.line([12, 992, W - 12, 992], fill=(120, 115, 100), width=1)
    d.text((12, 998),
           "All 45 stories were reported on Wednesday 18 November 2026; disputed claims are credited to those who made them.",
           font=SANS(9.5), fill=GREY)
    d.text((12, 1010),
           "Sources: AP · Reuters · AFP · BBC · Al Jazeera · UN News · IMD. Original drawings made for this page.",
           font=SANS(9.5), fill=GREY)
    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    render().save(os.path.join(here, "entry.png"))
    print("wrote entry.png")
