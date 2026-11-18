#!/usr/bin/env python3
"""Draw the v3 front page for news-image-20261118.

Theory: cleaner hierarchy beats more stories. The top scorers have 21-35
stories, not 45, and win on big illustrations, big headlines and breathing
room. So this page is warm cream paper with a giant black serif masthead,
nine large feature cards in a 3x3 grid (each with a proper drawn scene),
a figures strip, a dotted world map and a 21-item brief list: 30 stories.

Everything is drawn with PIL from news first reported on Wednesday
18 November 2026. No network, no clock, no randomness.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 232)
CARD = (255, 253, 246)
INK = (20, 20, 20)
RED = (164, 31, 36)
NAVY = (29, 42, 74)
GRAY = (107, 101, 88)
LINE = (216, 208, 189)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, x, y, text, fnt, fill, tracking=2):
    """Draw text with letterspacing; returns the x after the last glyph."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def badge(draw, cx, cy, num):
    r = 9
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = SANS_B(11)
    w = draw.textlength(str(num), font=f)
    draw.text((cx - w / 2, cy - 8), str(num), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- scenes
# Each scene draws inside a (x, y, w, h) panel with flat vector shapes.

def scene_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 35, 61))
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(232, 222, 178))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(31, 77, 107))
    for i in range(5):
        xx = x + 14 + i * 60
        d.line([xx, y + h - 18, xx + 26, y + h - 18], fill=(90, 140, 170), width=2)
    # warship silhouette
    d.polygon([(x + 18, y + h - 26), (x + 150, y + h - 26), (x + 138, y + h - 44),
               (x + 30, y + h - 44)], fill=(12, 18, 30))
    d.rectangle([x + 52, y + h - 58, x + 92, y + h - 44], fill=(12, 18, 30))
    d.rectangle([x + 66, y + h - 70, x + 76, y + h - 58], fill=(12, 18, 30))
    for lx in (58, 72, 86):
        d.rectangle([x + lx, y + h - 54, x + lx + 4, y + h - 49], fill=(255, 214, 120))
    # missile arc + jet + burst
    d.arc([x + 170, y + 6, x + 280, y + 66], 200, 340, fill=(255, 170, 60), width=3)
    d.polygon([(x + 268, y + 16), (x + 296, y + 24), (x + 268, y + 30),
               (x + 276, y + 23)], fill=(10, 10, 14))
    d.ellipse([x + 168, y + 58, x + 176, y + 66], fill=(255, 200, 90))
    for sx, sy in ((40, 14), (120, 10), (210, 30)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(200, 210, 230))


def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(223, 233, 239))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(127, 168, 189))
    for i in range(4):
        xx = x + 20 + i * 74
        d.line([xx, y + h - 20, xx + 34, y + h - 20], fill=(160, 195, 210), width=2)
    # deck, broken in the middle
    d.rectangle([x + 8, y + 34, x + 138, y + 42], fill=(70, 80, 92))
    d.rectangle([x + 178, y + 34, x + w - 8, y + 42], fill=(70, 80, 92))
    d.polygon([(x + 138, y + 34), (x + 156, y + 52), (x + 148, y + 56),
               (x + 132, y + 42)], fill=(70, 80, 92))
    d.polygon([(x + 178, y + 34), (x + 168, y + 58), (x + 176, y + 60),
               (x + 186, y + 42)], fill=(70, 80, 92))
    # arch + smoke
    d.arc([x + 30, y - 6, x + 150, y + 46], 180, 360, fill=(96, 104, 116), width=4)
    d.ellipse([x + 196, y + 8, x + 220, y + 30], fill=(150, 158, 166))
    d.ellipse([x + 212, y + 2, x + 232, y + 20], fill=(170, 178, 186))
    d.ellipse([x + 226, y + 12, x + 244, y + 28], fill=(150, 158, 166))
    d.line([x + 40, y + 42, x + 40, y + h - 30], fill=(96, 104, 116), width=3)
    d.line([x + w - 46, y + 42, x + w - 46, y + h - 30], fill=(96, 104, 116), width=3)


def scene_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 216, 160))
    # skyline
    base = y + h - 18
    for bx, bw, bh in ((0, 44, 34), (48, 36, 52), (88, 52, 26), (144, 40, 44),
                       (188, 44, 30), (236, 38, 48), (278, 36, 24)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(38, 42, 58))
    d.rectangle([x, base, x + w, y + h], fill=(38, 42, 58))
    # three flags
    def flag(fx, kind):
        d.line([x + fx, y + 10, x + fx, y + 58], fill=(60, 50, 40), width=3)
        if kind == "us":
            d.rectangle([x + fx + 3, y + 10, x + fx + 47, y + 30], fill=(178, 34, 52))
            for i in range(3):
                d.rectangle([x + fx + 3, y + 14 + i * 6, x + fx + 47, y + 16 + i * 6],
                            fill=(255, 255, 255))
            d.rectangle([x + fx + 3, y + 10, x + fx + 20, y + 22], fill=(30, 40, 90))
        elif kind == "cn":
            d.rectangle([x + fx + 3, y + 10, x + fx + 47, y + 30], fill=(222, 41, 16))
            for sx, sy in ((10, 14), (20, 12), (26, 18), (20, 24), (12, 22)):
                d.ellipse([x + fx + sx, y + sy, x + fx + sx + 4, y + sy + 4],
                          fill=(255, 222, 0))
        else:
            d.rectangle([x + fx + 3, y + 10, x + fx + 47, y + 17], fill=(255, 255, 255))
            d.rectangle([x + fx + 3, y + 17, x + fx + 47, y + 24], fill=(0, 57, 166))
            d.rectangle([x + fx + 3, y + 24, x + fx + 47, y + 30], fill=(213, 0, 50))
    flag(24, "us")
    flag(128, "cn")
    flag(232, "ru")
    d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=(240, 200, 90))


def scene_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 24))
    d.rectangle([x + 16, y + 16, x + 92, y + h - 16], fill=(36, 48, 40))
    for i in range(4):
        d.rectangle([x + 8, y + 26 + i * 16, x + 16, y + 30 + i * 16], fill=(120, 130, 120))
        d.rectangle([x + 92, y + 26 + i * 16, x + 100, y + 30 + i * 16], fill=(120, 130, 120))
    d.rectangle([x + 34, y + 32, x + 74, y + h - 32], fill=(20, 120, 70))
    d.text((x + 112, y + 14), "$115.8bn", font=SANS_B(30), fill=(255, 255, 255))
    d.text((x + 112, y + 50), "REVENUE  +103%", font=SANS_B(12), fill=(80, 200, 120))
    pts = [(x + 112, y + 84), (x + 150, y + 78), (x + 188, y + 80),
           (x + 226, y + 66), (x + 268, y + 56), (x + 300, y + 46)]
    d.line(pts, fill=(80, 200, 120), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(80, 200, 120))


def scene_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 238))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 170, 160))
    d.rectangle([x, y + h - 22, x + 120, y + h], fill=(196, 178, 130))
    cx, cy = x + 190, y + 46
    for r, col in ((34, (20, 90, 110)), (25, (40, 120, 140)), (16, (70, 150, 165)),
                   (8, (110, 180, 190))):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(20, 90, 110))
    d.arc([x + 20, y + 10, x + 90, y + 50], 300, 60, fill=(164, 31, 36), width=3)
    d.polygon([(x + 84, y + 12), (x + 98, y + 18), (x + 82, y + 26)], fill=(164, 31, 36))
    d.text((x + 228, y + 12), "145 km/h", font=SANS_B(13), fill=(20, 90, 110))


def scene_parliament(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 240))
    d.polygon([(x + 60, y + 22), (x + 160, y + 22), (x + 110, y + 6)], fill=(70, 66, 92))
    d.rectangle([x + 62, y + 22, x + 158, y + 28], fill=(70, 66, 92))
    for i in range(5):
        cx0 = x + 68 + i * 20
        d.rectangle([cx0, y + 28, cx0 + 8, y + 62], fill=(70, 66, 92))
    d.rectangle([x + 58, y + 62, x + 162, y + 68], fill=(70, 66, 92))
    d.rectangle([x + 196, y + 16, x + 296, y + 52], fill=(255, 255, 255),
                outline=(70, 66, 92), width=2)
    d.text((x + 208, y + 22), "66–52", font=SANS_B(20), fill=(29, 42, 74))
    d.line([x + 20, y + h - 14, x + w - 20, y + h - 14], fill=(150, 144, 170), width=2)


def scene_euro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(208, 224, 240))
    for i in range(12):
        ang = math.pi * 2 * i / 12 - math.pi / 2
        sx = x + 52 + int(30 * math.cos(ang))
        sy = y + 46 + int(30 * math.sin(ang))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(240, 200, 0))
    d.text((x + 30, y + 30), "€", font=SANS_B(34), fill=(29, 42, 74))
    d.text((x + 118, y + 18), "€45bn", font=SANS_B(30), fill=(29, 42, 74))
    d.text((x + 118, y + 56), "LOAN FOR 2027", font=SANS_B(12), fill=(90, 100, 120))


def scene_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 60, 74))
    d.polygon([(x, y + h), (x + 70, y + 34), (x + 150, y + h)], fill=(90, 100, 116))
    d.polygon([(x + 110, y + h), (x + 210, y + 22), (x + 300, y + h)], fill=(70, 80, 98))
    d.polygon([(x + 150, y + 30), (x + 236, y + 52), (x + 158, y + 58),
               (x + 168, y + 44)], fill=(200, 205, 215))
    d.polygon([(x + 236, y + 52), (x + 252, y + 48), (x + 240, y + 60)], fill=(200, 205, 215))


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 178))
    d.ellipse([x + w - 46, y + 8, x + w - 20, y + 34], fill=(170, 190, 210))
    for tx in (16, 66, 116, 166, 216):
        d.polygon([(x + tx, y + h - 22), (x + tx + 22, y + h - 52),
                   (x + tx + 44, y + h - 22)], fill=(120, 96, 66))
        d.line([x + tx + 22, y + h - 52, x + tx + 22, y + h - 22], fill=(90, 72, 48),
               width=2)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(150, 122, 84))
    d.polygon([(x + 252, y + 14), (x + 282, y + 62), (x + 222, y + 62)],
              fill=(240, 200, 0), outline=(150, 110, 0))
    d.rectangle([x + 250, y + 30, x + 254, y + 48], fill=(40, 30, 20))
    d.ellipse([x + 249, y + 52, x + 255, y + 58], fill=(40, 30, 20))


SCENES = [scene_gulf, scene_bridge, scene_flags, scene_chip, scene_cyclone,
          scene_parliament, scene_euro, scene_plane, scene_gaza]

FEATURES = [
    ("MIDDLE EAST · WAR", "REPORTED",
     "US and Iran trade fire over Bahrain and Qeshm",
     "US jets hit an Iranian missile site on Qeshm after drones targeted a US "
     "radar in Bahrain."),
    ("EUROPE · WAR IN UKRAINE", "REPORTED",
     "A span of the Crimea bridge falls into the sea",
     "Kyiv says a second strike destroyed the road arch; Moscow says it "
     "downed 1,441 drones."),
    ("ASIA · DIPLOMACY", "REPORTED",
     "Trump meets Quad leaders, then flies to Shenzhen",
     "Talks and a working lunch in Manila, a day after the first Quad summit "
     "in two years."),
    ("UNITED STATES · BUSINESS", "REPORTED",
     "Nvidia's revenue doubles to $115.8bn",
     "Sales rose 103% as data-centre demand held up. The board won't bring "
     "back Jensen Huang."),
    ("SOUTH ASIA · WEATHER", "REPORTED",
     "Cyclone Akvan bears down on Andhra Pradesh",
     "Forecast to make landfall Friday with gusts to 145 km/h. Odisha is "
     "moving 200,000 people."),
    ("ISRAEL · POLITICS", "REPORTED",
     "Knesset elects Kahana as speaker, 66–52",
     "Kahana, an ally of Gadi Eisenkot, replaces Amir Ohana after a "
     "seven-hour debate."),
    ("EUROPE · UKRAINE", "PLANNED",
     "EU proposes a €45bn loan for Ukraine",
     "The loan covers about two-thirds of Kyiv's 2027 gap, repaid only if "
     "Russia pays reparations."),
    ("RUSSIA · CRASH", "REPORTED",
     "Russian An-12 crashes in Siberia; 19 dead",
     "All 19 aboard died in the Kemerovo crash. Moscow blames a technical "
     "fault."),
    ("GAZA · HUMANITARIAN", "REPORTED",
     "UN warns of cold deaths as winter sets in",
     "The UN warns of cold deaths as winter sets in; 1.7M displaced, 1.4M "
     "face acute hunger."),
]

BRIEFS = [
    "China cuts tariffs as Xi meets Carney.",
    "Dhoni ends IPL career — CSK mentor in 2027.",
    "Voyager 1 reaches one light-day.",
    "COP31 heat plan — $20m for cooling.",
    "France protests — 146,000 march, 4th weekend.",
    "Freezer blackout — cyber-attack hits 7 nations.",
    "Settler sanctions — Australia lists 7 firms.",
    "Sudan drone toll — UN: 1,630 civilians killed.",
    "Tanker attacked — TARA GAS hit, 1 missing.",
    "Ukraine toll — UN: 372 killed in October.",
    "Japan scrambles jets — two Russian planes.",
    "NSA network down — maintenance fault, no hack.",
    "Apple outage — iCloud, App Store, Pay hit.",
    "Tech bets slashed — biggest cut since 2006.",
    "Senegal qualify — first team into AFCON 2027.",
    "SAFF final — India beat Pakistan 2–1.",
    "Journalist killed in Costa Rica, first in 25 yrs.",
    "Guinea crackdown — 224 jailed over gold mining.",
    "Jordan–Iraq block Telegram over security fears.",
    "US presses UN agency over Taiwan flight curbs.",
    "Baidu chief warns of AI 'bubble' before APEC.",
]

FIGURES = [
    ("66–52", "Kahana's margin for speaker"),
    ("$115.8bn", "Nvidia revenue, up 103%"),
    ("145 km/h", "Akvan's gusts at landfall"),
    ("200,000", "Odisha evacuations"),
]

# Dotted world map: 40 columns x 22 rows, '#' is land.
MAP = [
    ".############..###....##################",
    ".#############.###..####################",
    "..############..#..#####################",
    "...##########......#####################",
    ".....########......####################.",
    "......#######......#####.#############..",
    ".......#####.......###################..",
    "........###........###############......",
    ".........##.........##############......",
    "..........##........#######.#####.......",
    "...........####......#####...#.##.......",
    "............####.....#####.....#####....",
    "............####.....####.......#####...",
    "............###......####........###....",
    "............###......####.......#####...",
    ".............##.......###.......######..",
    ".............##.......###........####...",
    ".............##........##.........###...",
    "..............#....................##...",
    "..............#.........................",
    "..............#.........................",
    "........................................",
]

# (story number, longitude, latitude) for the map pins
PINS = [(1, 54, 26), (2, 36.5, 45), (3, 121, 14.6), (4, -95, 37),
        (5, 80, 16), (6, 35, 31), (7, 4.4, 50.8), (8, 86, 55), (9, 34.5, 31.4)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 232))
    cols, rows = 40, 22
    step_x, step_y = w / cols, h / rows
    for r, line in enumerate(MAP):
        for c, ch in enumerate(line):
            if ch == "#":
                cx = x + c * step_x + step_x / 2
                cy = y + r * step_y + step_y / 2
                d.ellipse([cx - 1.8, cy - 1.8, cx + 1.8, cy + 1.8], fill=(90, 110, 90))
    for num, lon, lat in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (75 - lat) / 130 * h
        # nudge the Gaza pin off the Israel pin
        if num == 9:
            px += 12
            py += 10
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
        f = SANS_B(9)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 7), str(num), font=f, fill=(255, 255, 255))


def draw_card(d, x, y, w, h, idx, kicker, status, headline, summary):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    SCENES[idx](d, x + 1, y + 1, w - 2, 92)
    badge(d, x + 13, y + 108, idx + 1)
    kf = SANS_B(10)
    d.text((x + 28, y + 101), kicker, font=kf, fill=RED)
    sf = SANS(9)
    tag = "● " + status
    tw = d.textlength(tag, font=sf)
    d.text((x + w - 8 - tw, y + 102), tag, font=sf, fill=GRAY)
    hf = SERIF_B(18)
    lines = wrap(d, headline, hf, w - 24)[:2]
    ty = y + 120
    for ln in lines:
        d.text((x + 12, ty), ln, font=hf, fill=INK)
        ty += 19
    bf = SANS(10)
    blines = wrap(d, summary, bf, w - 24)[:2]
    ty = y + 160
    for ln in blines:
        d.text((x + 12, ty), ln, font=bf, fill=(60, 58, 50))
        ty += 12


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28

    # eyebrow
    spaced(d, mx, 12, "THE DAY IN ONE PICTURE", SANS_B(13), GRAY)
    right = "LATE EDITION · THIRTY STORIES"
    rf = SANS_B(13)
    d.text((W - mx - d.textlength(right, font=rf), 12), right, font=rf, fill=RED)

    # masthead
    d.text((mx, 32), "Wednesday 18 November 2026", font=SERIF_B(54), fill=INK)
    d.line([mx, 102, W - mx, 102], fill=INK, width=3)
    d.text((mx, 110), "Strikes in the Gulf and on the Kerch bridge, a three-way summit in "
                      "Shenzhen, a chipmaker doubling — the day in thirty stories.",
           font=SERIF(15), fill=(70, 66, 58))

    # feature grid: 3 x 3
    cw, ch, gap = 314, 188, 13
    gx, gy = mx, 138
    for i, (kicker, status, headline, summary) in enumerate(FEATURES):
        row, col = divmod(i, 3)
        draw_card(d, gx + col * (cw + gap), gy + row * (ch + 8), cw, ch,
                  i, kicker, status, headline, summary)

    # figures strip
    fy = 726
    d.line([mx, fy, W - mx, fy], fill=INK, width=2)
    d.text((mx, fy + 10), "BY THE", font=SANS_B(11), fill=RED)
    d.text((mx, fy + 24), "NUMBERS", font=SANS_B(11), fill=RED)
    fx = mx + 92
    fw = (W - mx - fx) // 4
    for num, cap in FIGURES:
        d.text((fx, fy + 6), num, font=SERIF_B(25), fill=NAVY)
        d.text((fx, fy + 34), cap, font=SANS(10), fill=GRAY)
        fx += fw
    d.line([mx, fy + 50, W - mx, fy + 50], fill=INK, width=1)

    # bottom: map + briefs
    by = 786
    d.text((mx, by), "WHERE IT HAPPENED", font=SANS_B(12), fill=NAVY)
    d.text((344, by), "ALSO ON WEDNESDAY 18 NOVEMBER — 21 MORE STORIES",
           font=SANS_B(12), fill=NAVY)
    draw_map(d, mx, by + 20, 300, 162)
    d.text((mx, by + 186), "Numbered dots mark stories 1–9.",
           font=SERIF(10), fill=GRAY)
    bf = SANS(11)
    col_w = 318
    for i, item in enumerate(BRIEFS):
        col, row = divmod(i, 11)
        ix = 344 + col * (col_w + 16)
        iy = by + 20 + row * 15
        num = str(i + 10) + ". "
        d.text((ix, iy), num, font=SANS_B(11), fill=RED)
        nw = d.textlength(num, font=bf)
        d.text((ix + nw, iy), item, font=bf, fill=INK)

    # footer
    d.line([mx, 974, W - mx, 974], fill=INK, width=1)
    d.text((mx, 982), "Every story was reported on Wednesday 18 November 2026; disputed "
                      "claims are attributed. Sources: AP · Reuters · AFP · BBC · "
                      "Al Jazeera · UN News. Original drawings.",
           font=SERIF(10), fill=GRAY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()
