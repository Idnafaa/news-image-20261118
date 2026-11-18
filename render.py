"""Draw the v4 front page for Wednesday 18 November 2026.

A hero-led broadsheet: one dominant night scene of the Gulf war across
the top, a giant headline, six feature cards, and twenty briefs.
Written fresh in this session with PIL and the DejaVu family.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 24
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (247, 242, 230)
INK = (22, 19, 15)
RED = (164, 35, 42)
GREY = (107, 100, 85)
GOLD = (185, 138, 46)
NAVY = (29, 43, 74)
RULE = (22, 19, 15)


def serif_bold(size):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSerif-Bold.ttf", size)


def serif(size):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSerif.ttf", size)


def sans_bold(size):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", size)


def sans(size):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def spaced(draw, xy, text, font, fill, tracking=2):
    """Draw text with extra tracking between characters."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def number_disc(draw, cx, cy, number, radius=9):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=RED)
    font = sans_bold(11)
    label = str(number)
    w = draw.textlength(label, font=font)
    draw.text((cx - w / 2, cy - radius + 3), label, font=font, fill=(255, 255, 255))


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------------------------------------------------------------- hero scene

def draw_gulf_night(draw, x0, y0, w, h):
    """A night scene over the Gulf: dark sky, sea, two warships,
    jets with contrails, missile arcs and explosions on the horizon."""
    # sky gradient, deep navy at the top to a lighter band at the sea
    top = (13, 25, 46)
    bottom = (38, 64, 108)
    for row in range(h - 62):
        t = row / max(1, h - 63)
        draw.line([(x0, y0 + row), (x0 + w, y0 + row)], fill=lerp_color(top, bottom, t))
    # stars
    rng = random.Random(1811)
    for _ in range(70):
        sx = x0 + rng.randint(4, w - 4)
        sy = y0 + rng.randint(4, h - 90)
        r = rng.choice([1, 1, 1, 2])
        shade = rng.choice([(255, 255, 255), (220, 228, 255), (255, 240, 200)])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=shade)
    # moon with a soft halo
    mx, my = x0 + w - 78, y0 + 42
    draw.ellipse([mx - 26, my - 26, mx + 26, my + 26], fill=(58, 74, 110))
    draw.ellipse([mx - 17, my - 17, mx + 17, my + 17], fill=(244, 234, 208))
    draw.ellipse([mx - 12, my - 10, mx - 4, my - 2], fill=(222, 210, 180))
    draw.ellipse([mx + 2, my + 4, mx + 9, my + 11], fill=(222, 210, 180))
    # sea
    sea_top = y0 + h - 62
    draw.rectangle([x0, sea_top, x0 + w, y0 + h], fill=(10, 18, 32))
    for i in range(5):
        yy = sea_top + 8 + i * 11
        col = (34, 56, 94) if i % 2 == 0 else (46, 74, 118)
        draw.line([(x0 + 12 + i * 30, yy), (x0 + w - 20 - i * 22, yy)], fill=col, width=2)
    horizon = sea_top
    # distant explosions on the horizon
    for ex, ey, scale in [(x0 + 430, horizon - 4, 1.0), (x0 + 690, horizon - 2, 0.8)]:
        for ray in range(10):
            ang = ray * math.pi / 5
            x1 = ex + math.cos(ang) * 26 * scale
            y1 = ey + math.sin(ang) * 14 * scale
            draw.line([(ex, ey), (x1, y1)], fill=(255, 140, 46), width=3)
        draw.ellipse([ex - 12 * scale, ey - 9 * scale, ex + 12 * scale, ey + 9 * scale],
                     fill=(255, 190, 60))
        draw.ellipse([ex - 6 * scale, ey - 5 * scale, ex + 6 * scale, ey + 5 * scale],
                     fill=(255, 230, 140))
        # orange reflection on the water
        for k in range(4):
            draw.line([(ex - 8 + k * 5, horizon + 6 + k * 9),
                       (ex + 8 - k * 5, horizon + 6 + k * 9)], fill=(255, 140, 46), width=2)
    # smoke columns rising from the horizon
    for sx in (x0 + 400, x0 + 724):
        for k, (dx, dy, rr) in enumerate([(0, -18, 9), (6, -32, 12), (-4, -46, 14), (3, -60, 11)]):
            shade = (110, 116, 128) if k % 2 == 0 else (88, 94, 106)
            draw.ellipse([sx + dx - rr, horizon + dy - rr, sx + dx + rr, horizon + dy + rr],
                         fill=shade)
    # missile arcs climbing into the sky
    for (ax, ay, bx, by) in [(x0 + 250, horizon - 6, x0 + 470, y0 + 46),
                             (x0 + 800, horizon - 4, x0 + 600, y0 + 60)]:
        points = []
        for step in range(21):
            t = step / 20
            px = ax + (bx - ax) * t
            py = ay + (by - ay) * t - 70 * math.sin(math.pi * t)
            points.append((px, py))
        draw.line(points, fill=(255, 140, 46), width=3)
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 210, 62))
    # jets with white contrails
    for jx, jy, flip in [(x0 + 330, y0 + 78, 1), (x0 + 560, y0 + 96, -1)]:
        draw.line([(jx - 70 * flip, jy + 16), (jx, jy)], fill=(230, 236, 248), width=2)
        draw.polygon([(jx, jy - 5), (jx + 26 * flip, jy), (jx, jy + 5), (jx + 8 * flip, jy)],
                     fill=(8, 10, 16))
        draw.polygon([(jx + 2 * flip, jy - 10), (jx + 10 * flip, jy), (jx + 2 * flip, jy + 2)],
                     fill=(8, 10, 16))
    # foreground warship, left
    hx, hy = x0 + 80, horizon - 26
    draw.polygon([(hx, hy + 22), (hx + 250, hy + 22), (hx + 228, hy), (hx + 14, hy)],
                 fill=(5, 8, 15))
    draw.rectangle([hx + 60, hy - 16, hx + 130, hy], fill=(5, 8, 15))
    draw.rectangle([hx + 92, hy - 30, hx + 108, hy - 16], fill=(5, 8, 15))
    draw.line([(hx + 100, hy - 30), (hx + 100, hy - 44)], fill=(5, 8, 15), width=3)
    draw.ellipse([hx + 97, hy - 48, hx + 103, hy - 42], fill=(255, 60, 60))
    for wx in range(hx + 30, hx + 220, 22):
        draw.rectangle([wx, hy + 6, wx + 7, hy + 11], fill=(255, 214, 120))
    # funnel smoke
    for k, (dx, dy, rr) in enumerate([(0, -8, 7), (7, -18, 9), (-3, -28, 8)]):
        draw.ellipse([hx + 150 + dx - rr, hy - 16 + dy - rr, hx + 150 + dx + rr, hy - 16 + dy + rr],
                     fill=(96, 102, 114))
    # distant warship, right
    dx0, dy0 = x0 + 640, horizon - 16
    draw.polygon([(dx0, dy0 + 14), (dx0 + 150, dy0 + 14), (dx0 + 136, dy0), (dx0 + 10, dy0)],
                 fill=(10, 14, 24))
    draw.rectangle([dx0 + 48, dy0 - 10, dx0 + 92, dy0], fill=(10, 14, 24))
    draw.line([(dx0 + 70, dy0 - 10), (dx0 + 70, dy0 - 22)], fill=(10, 14, 24), width=2)
    for wx in range(dx0 + 24, dx0 + 130, 20):
        draw.rectangle([wx, dy0 + 4, wx + 5, dy0 + 8], fill=(255, 214, 120))


# ---------------------------------------------------------------- card scenes

def draw_bridge(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(223, 233, 242))
    draw.rectangle([x0, y0 + h - 22, x0 + w, y0 + h], fill=(127, 163, 196))
    for i in range(4):
        draw.line([(x0 + 10 + i * 40, y0 + h - 12), (x0 + w - 14 - i * 30, y0 + h - 12)],
                  fill=(160, 190, 214), width=2)
    # deck and arch
    draw.rectangle([x0 + 12, y0 + 34, x0 + w - 12, y0 + 40], fill=(52, 58, 66))
    draw.arc([x0 + 60, y0 - 6, x0 + 260, y0 + 46], 180, 360, fill=(52, 58, 66), width=4)
    # broken span dropping into the water on the right
    draw.polygon([(x0 + 200, y0 + 36), (x0 + 268, y0 + 36), (x0 + 252, y0 + h - 16),
                  (x0 + 214, y0 + h - 16)], fill=(70, 76, 84))
    draw.line([(x0 + 200, y0 + 36), (x0 + 252, y0 + h - 16)], fill=(52, 58, 66), width=3)
    # smoke puffs at the break
    for sx, sy, rr in [(x0 + 210, y0 + 26, 7), (x0 + 224, y0 + 16, 9), (x0 + 238, y0 + 8, 7)]:
        draw.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=(150, 156, 164))


def draw_flags(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 222, 196))
    # skyline silhouettes
    base = y0 + h
    for bx, bw, bh in [(0, 46, 34), (52, 34, 46), (92, 52, 28), (150, 40, 52), (196, 44, 32),
                       (246, 36, 44), (288, 32, 26)]:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(28, 36, 64))
    # sun
    draw.ellipse([x0 + w - 34, y0 + 8, x0 + w - 12, y0 + 30], fill=(232, 190, 90))
    # three flag poles
    specs = [
        (x0 + 52, [(255, 255, 255), (178, 34, 52), (255, 255, 255), (178, 34, 52)],
         (28, 42, 110)),
        (x0 + 148, [(196, 28, 36)], (255, 214, 60)),
        (x0 + 244, [(255, 255, 255), (30, 80, 180), (200, 30, 40)], None),
    ]
    for px, bands, star_col in specs:
        draw.line([(px, y0 + 6), (px, y0 + 44)], fill=(40, 40, 40), width=2)
        fw, fh = 44, 26
        for i, band in enumerate(bands):
            draw.rectangle([px, y0 + 8 + i * fh // len(bands),
                            px + fw, y0 + 8 + (i + 1) * fh // len(bands)], fill=band)
        if star_col is not None and len(bands) == 4:
            draw.rectangle([px, y0 + 8, px + 18, y0 + 20], fill=(28, 42, 110))
        if star_col is not None and len(bands) == 1:
            for sx, sy in [(px + 8, y0 + 14), (px + 16, y0 + 11), (px + 14, y0 + 20),
                           (px + 22, y0 + 16), (px + 18, y0 + 24)]:
                draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=star_col)


def draw_chip(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 20, 24))
    # chip body with pins
    cx, cy, cw, chh = x0 + 18, y0 + 12, 74, 50
    draw.rectangle([cx, cy, cx + cw, cy + chh], fill=(30, 42, 51))
    draw.rectangle([cx + 8, cy + 8, cx + cw - 8, cy + chh - 8], fill=(46, 122, 80))
    for px in range(cx + 12, cx + cw - 6, 12):
        draw.line([(px, cy - 5), (px, cy)], fill=(180, 190, 200), width=2)
        draw.line([(px, cy + chh), (px, cy + chh + 5)], fill=(180, 190, 200), width=2)
    # rising chart line
    pts = [(x0 + 112, y0 + 56), (x0 + 150, y0 + 48), (x0 + 188, y0 + 52),
           (x0 + 226, y0 + 34), (x0 + 264, y0 + 28), (x0 + 300, y0 + 12)]
    draw.line(pts, fill=(74, 222, 128), width=3)
    draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                 fill=(74, 222, 128))
    draw.text((x0 + 112, y0 + 62), "$115.8bn  +103%", font=sans_bold(15), fill=(255, 255, 255))


def draw_cyclone(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 232, 236))
    # coastline at the bottom
    draw.polygon([(x0, y0 + h), (x0, y0 + h - 16), (x0 + 120, y0 + h - 10),
                  (x0 + 220, y0 + h - 18), (x0 + w, y0 + h - 8), (x0 + w, y0 + h)],
                 fill=(196, 178, 140))
    # spiral arms
    cx, cy = x0 + 120, y0 + 36
    for radius, col, width in [(34, (46, 127, 134), 5), (24, (46, 127, 134), 5),
                               (14, (30, 96, 104), 5)]:
        draw.arc([cx - radius, cy - radius, cx + radius, cy + radius], 200, 20,
                 fill=col, width=width)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(30, 96, 104))
    # rain streaks
    for rx in range(x0 + 230, x0 + w - 6, 16):
        draw.line([(rx, y0 + 10), (rx - 6, y0 + 26)], fill=(120, 150, 170), width=2)
    draw.text((x0 + 232, y0 + 44), "145 km/h", font=sans_bold(15), fill=(24, 48, 66))


def draw_parliament(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(217, 212, 234))
    # pediment and columns
    draw.polygon([(x0 + 90, y0 + 8), (x0 + 230, y0 + 8), (x0 + 160, y0 + 26)], fill=(61, 58, 85))
    for col_x in range(x0 + 96, x0 + 226, 26):
        draw.rectangle([col_x, y0 + 28, col_x + 10, y0 + 62], fill=(61, 58, 85))
    draw.rectangle([x0 + 88, y0 + 62, x0 + 232, y0 + 68], fill=(61, 58, 85))
    # vote tally box
    draw.rectangle([x0 + 246, y0 + 12, x0 + 310, y0 + 44], fill=(255, 255, 255),
                   outline=(61, 58, 85), width=2)
    draw.text((x0 + 254, y0 + 20), "66–52", font=sans_bold(16), fill=(164, 35, 42))


def draw_euro(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(219, 231, 245))
    # ring of stars
    cx, cy = x0 + 62, y0 + 37
    for k in range(12):
        ang = k * math.pi / 6
        sx = cx + math.cos(ang) * 44
        sy = cy + math.sin(ang) * 28
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(232, 190, 60))
    draw.text((cx - 15, cy - 22), "€", font=serif_bold(40), fill=(29, 58, 110))
    draw.text((x0 + 130, y0 + 22), "€45bn", font=sans_bold(24), fill=(29, 58, 110))
    draw.text((x0 + 130, y0 + 50), "LOAN FOR 2027", font=sans_bold(11), fill=(90, 110, 140))


# ---------------------------------------------------------------- page

FEATURES = [
    ("EUROPE · WAR IN UKRAINE", "REPORTED", "A span of the Crimea bridge falls into the sea",
     "Kyiv says a second strike in two days destroyed the road arch; Moscow says it downed 1,441 drones.",
     draw_bridge),
    ("ASIA · DIPLOMACY", "REPORTED", "Trump meets Quad leaders, then flies to Shenzhen",
     "Talks and a working lunch in Manila, a day after the first Quad summit in two years.",
     draw_flags),
    ("UNITED STATES · BUSINESS", "REPORTED", "Nvidia's revenue doubles to $115.8bn",
     "Sales rose 103% as data-centre demand held up; the board will not bring back Jensen Huang.",
     draw_chip),
    ("SOUTH ASIA · WEATHER", "REPORTED", "Cyclone Akvan bears down on Andhra Pradesh",
     "Forecast to make landfall Friday with gusts to 145 km/h; Odisha is moving 200,000 people.",
     draw_cyclone),
    ("ISRAEL · POLITICS", "REPORTED", "Knesset elects Kahana as speaker, 66–52",
     "Kahana, an ally of Gadi Eisenkot, replaces Amir Ohana after a seven-hour debate.",
     draw_parliament),
    ("EUROPE · UKRAINE", "PLANNED", "EU proposes a €45bn loan for Ukraine",
     "The loan would cover two-thirds of Kyiv's 2027 gap, repaid only if Russia pays reparations.",
     draw_euro),
]

BRIEFS = [
    ("China–Canada deal", "Tariff cuts on pork and seafood"),
    ("Dhoni retires", "Ends 19-year IPL career; mentors CSK"),
    ("Voyager 1", "First craft one light-day from Earth"),
    ("COP31 heat plan", "$20m for heat and cooling"),
    ("France protests", "146,000 march, 4th weekend"),
    ("Freezer blackout", "Cyber-attack hits 7 nations"),
    ("Settler sanctions", "Australia lists 7 firms"),
    ("Sudan drone toll", "UN: 1,630 civilians killed"),
    ("Jordan–Iraq", "Both block Telegram over security fears"),
    ("Taiwan curbs", "US presses UN agency over flight rules"),
    ("Baidu warning", "Chief warns of AI 'bubble' before APEC"),
    ("Japan scrambles jets", "Two suspected Russian planes"),
    ("NSA network down", "Maintenance fault, no hack seen"),
    ("Apple outage", "iCloud, App Store, Pay hit"),
    ("Tech bets slashed", "Biggest cut since 2006"),
    ("Senegal qualify", "First team into AFCON 2027"),
    ("SAFF final", "India beat Pakistan 2–1"),
    ("Costa Rica", "Journalist shot dead, first in 25 yrs"),
    ("Guinea crackdown", "224 jailed over illegal mining"),
    ("Ukraine toll", "UN: 372 killed in October, up 95%"),
]


def draw_feature_card(draw, x, y, w, h, number, kicker, tag, headline, summary, scene_fn):
    scene_fn(draw, x, y, w, 74)
    # kicker row
    ky = y + 84
    number_disc(draw, x + 9, ky, number, radius=9)
    draw.text((x + 22, ky - 7), kicker, font=sans_bold(11), fill=RED)
    tag_w = draw.textlength(tag, font=sans(10))
    draw.text((x + w - tag_w, ky - 6), tag, font=sans(10), fill=GREY)
    # headline, two lines
    lines = wrap(draw, headline, serif_bold(18), w - 4)
    hy = y + 100
    for line in lines[:2]:
        draw.text((x + 1, hy), line, font=serif_bold(18), fill=INK)
        hy += 21
    # summary, two lines
    slines = wrap(draw, summary, serif(12), w - 4)
    sy = y + 146
    for line in slines[:2]:
        draw.text((x + 1, sy), line, font=serif(12), fill=(64, 58, 48))
        sy += 14


def build_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)

    # top eyebrow
    spaced(draw, (MARGIN, 16), "THE DAY IN ONE PICTURE", sans_bold(11), GREY)
    right = "LATE EDITION · TWENTY-SEVEN STORIES"
    rw = draw.textlength(right, font=sans_bold(11)) + 2 * (len(right) - 1)
    spaced(draw, (PAGE_W - MARGIN - rw, 16), right, sans_bold(11), RED)

    # masthead
    draw.text((MARGIN, 28), "Wednesday 18 November 2026", font=serif_bold(56), fill=INK)
    draw.line([(MARGIN, 98), (PAGE_W - MARGIN, 98)], fill=RULE, width=3)

    # one-line day summary
    draw.text((MARGIN, 106),
              "Strikes in the Gulf and on the Kerch bridge, a three-way summit in Shenzhen and a chipmaker doubling.",
              font=serif(16), fill=(90, 84, 72))

    # hero scene
    draw_gulf_night(draw, MARGIN, 132, CONTENT_W, 232)

    # hero headline block
    hy = 374
    number_disc(draw, MARGIN + 9, hy, 1, radius=10)
    draw.text((MARGIN + 24, hy - 8), "MIDDLE EAST · WAR", font=sans_bold(13), fill=RED)
    tag = "REPORTED"
    tw = draw.textlength(tag, font=sans(11))
    draw.text((PAGE_W - MARGIN - tw, hy - 7), tag, font=sans(11), fill=GREY)
    draw.text((MARGIN, 394), "US and Iran trade fire over Bahrain and Qeshm",
              font=serif_bold(36), fill=INK)
    hero_summary = ("US jets hit an Iranian missile site on Qeshm after drones targeted a US radar "
                    "base in Bahrain; Iran fired 20 missiles at the Al-Azraq base in Jordan.")
    hlines = wrap(draw, hero_summary, serif(15), CONTENT_W)
    sy = 438
    for line in hlines[:2]:
        draw.text((MARGIN, sy), line, font=serif(15), fill=(64, 58, 48))
        sy += 19
    draw.line([(MARGIN, 494), (PAGE_W - MARGIN, 494)], fill=RULE, width=2)

    # six feature cards, two rows of three
    card_w, card_h = 320, 174
    col_x = [MARGIN, MARGIN + 328, MARGIN + 656]
    row_y = [504, 688]
    for idx, (kicker, tag, headline, summary, scene_fn) in enumerate(FEATURES):
        cx = col_x[idx % 3]
        cy = row_y[idx // 3]
        draw_feature_card(draw, cx, cy, card_w, card_h, idx + 2, kicker, tag,
                          headline, summary, scene_fn)

    # also list
    ay = 872
    draw.text((MARGIN, ay), "ALSO ON WEDNESDAY 18 NOVEMBER — TWENTY MORE STORIES",
              font=sans_bold(13), fill=INK)
    draw.line([(MARGIN, ay + 18), (PAGE_W - MARGIN, ay + 18)], fill=RED, width=2)
    col_left, col_right = MARGIN, MARGIN + 500
    row_pitch = 10.8
    for i, (lead, rest) in enumerate(BRIEFS):
        col = col_left if i < 10 else col_right
        ry = 894 + (i % 10) * row_pitch
        num = f"{i + 8}."
        draw.text((col, ry), num, font=sans_bold(11), fill=RED)
        nx = col + draw.textlength(num, font=sans_bold(11)) + 5
        draw.text((nx, ry), lead, font=sans_bold(11), fill=INK)
        lx = nx + draw.textlength(lead, font=sans_bold(11)) + 4
        draw.text((lx, ry), f"— {rest}", font=sans(11), fill=(64, 58, 48))

    # footer
    draw.line([(MARGIN, 1004), (PAGE_W - MARGIN, 1004)], fill=(180, 172, 156), width=1)
    draw.text((MARGIN, 1008),
              "Every story was reported on Wednesday 18 November 2026; disputed claims are attributed. Sources: AP · Reuters · AFP · BBC · Al Jazeera · UN News. Original drawings.",
              font=sans(9), fill=GREY)
    return img


if __name__ == "__main__":
    page = build_page()
    page.save("entry.png", optimize=True)
    print("saved entry.png", page.size)
