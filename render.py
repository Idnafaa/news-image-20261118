"""Draw the 18 November 2026 world-news poster (1024x1024 PNG).

A broadsheet-style front page rendered with PIL and the DejaVu fonts:
a crimson masthead naming the day, a full-width lead story with a
hand-drawn sea panel, two rows of two stories each, and an "also on
this day" strip. Every line of text comes from news first reported
on Wednesday 18 November 2026. The drawing is deterministic: no
randomness, no clock, no network. Run: python3 render.py
"""
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (248, 244, 233)
INK = (30, 30, 30)
CRIMSON = (150, 25, 30)
GOLD = (233, 186, 84)
CREAM = (255, 250, 240)
NAVY = (23, 42, 74)
SEA = (28, 68, 110)
ORANGE = (238, 120, 30)
TEAL = (16, 104, 102)
BLUE = (33, 90, 138)
GREEN = (36, 108, 70)
SLATE = (88, 84, 76)
BODY = (62, 59, 52)
RUST = (176, 62, 28)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(FONTS + name, size)


def bold(size):
    return load("DejaVuSans-Bold.ttf", size)


def plain(size):
    return load("DejaVuSans.ttf", size)


def serif_bold(size):
    return load("DejaVuSerif-Bold.ttf", size)


def fit_words(draw, text, face, width):
    """Split text into lines that fit inside width pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def block(draw, x, y, text, face, colour, width, gap):
    """Draw a wrapped paragraph; return the y below its last line."""
    for line in fit_words(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += gap
    return y


def spaced(draw, x, y, text, face, colour, extra=5):
    """Draw a line with extra space between its letters."""
    for char in text:
        draw.text((x, y), char, font=face, fill=colour)
        x += draw.textlength(char, font=face) + extra
    return x


def rule(draw, x0, x1, y, colour=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=colour, width=width)


# --- pictograms, each drawn from plain shapes ---------------------------

def draw_tanker(d, box):
    """A tanker on a dark sea, with a burst above its funnel."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=SEA)
    # sky burst
    cx, cy = (x0 + x1) // 2, y0 + 52
    star = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 30 if i % 2 == 0 else 13
        star.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(star, fill=ORANGE)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=GOLD)
    d.text((x0 + 14, y0 + 12), "GULF OF OMAN", font=bold(15),
           fill=(170, 200, 225))
    # hull
    hx0, hy0 = x0 + 26, y0 + 150
    hx1, hy1 = x1 - 26, y0 + 196
    d.polygon([(hx0, hy0), (hx1, hy0), (hx1 - 26, hy1), (hx0 + 14, hy1)],
              fill=(16, 24, 38))
    d.rectangle([hx0 + 60, hy0 - 34, hx0 + 118, hy0], fill=(16, 24, 38))
    d.rectangle([hx0 + 132, hy0 - 22, hx0 + 158, hy0], fill=RUST)
    d.line([(hx0 + 30, hy0 - 34), (hx0 + 30, hy0 - 58)], fill=(16, 24, 38),
           width=4)
    # waves
    for wy in (y1 - 34, y1 - 18):
        for wx in range(x0 + 10, x1 - 10, 46):
            d.arc([wx, wy - 8, wx + 44, wy + 10], 180, 360,
                  fill=(120, 170, 210), width=3)


def draw_parliament(d, box, colour):
    """A classical facade: pediment, columns, steps."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    d.polygon([(x0 + 4, y0 + 26), (cx, y0 + 2), (x1 - 4, y0 + 26)],
              fill=colour)
    d.rectangle([x0 + 4, y0 + 26, x1 - 4, y0 + 32], fill=colour)
    for i in range(4):
        px = x0 + 12 + i * ((x1 - x0 - 24) // 3)
        d.rectangle([px, y0 + 36, px + 9, y1 - 12], fill=colour)
    d.rectangle([x0 + 2, y1 - 12, x1 - 2, y1 - 8], fill=colour)
    d.rectangle([x0 + 6, y1 - 6, x1 - 6, y1 - 2], fill=colour)


def draw_bridge(d, box, colour):
    """A suspension bridge: deck, two towers, hanging cables."""
    x0, y0, x1, y1 = box
    mid = (x0 + x1) / 2
    d.line([(x0 + 2, y1 - 14), (x1 - 2, y1 - 14)], fill=colour, width=5)
    for tx in (x0 + 16, x1 - 24):
        d.rectangle([tx, y0 + 8, tx + 8, y1 - 14], fill=colour)
    d.line([(x0 + 20, y0 + 8), (mid, y1 - 14)], fill=colour, width=3)
    d.line([(x1 - 20, y0 + 8), (mid, y1 - 14)], fill=colour, width=3)
    for frac in (0.25, 0.5, 0.75):
        px = x0 + (x1 - x0) * frac
        top = y0 + 8 + (y1 - 14 - y0 - 8) * abs(frac - 0.5) * 2
        d.line([(px, top), (px, y1 - 14)], fill=colour, width=2)
    d.line([(x0 + 6, y1 - 26), (mid, y1 - 34), (x1 - 6, y1 - 26)],
           fill=colour, width=2)


def draw_snowflake(d, box, colour):
    """Six arms, each with two small branches."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for k in range(6):
        ang = math.pi * k / 3
        dx, dy = math.cos(ang), math.sin(ang)
        ex, ey = cx + 26 * dx, cy + 26 * dy
        d.line([(cx, cy), (ex, ey)], fill=colour, width=4)
        for t in (0.55, 0.8):
            bx, by = cx + 26 * t * dx, cy + 26 * t * dy
            for s in (1, -1):
                px, py = dx * 0.5 + s * dy * 0.5, dy * 0.5 - s * dx * 0.5
                d.line([(bx, by), (bx + 9 * px, by + 9 * py)],
                       fill=colour, width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=colour)


def draw_globe(d, box, colour):
    """A globe: outline, equator, one meridian, one latitude arc."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=colour, width=5)
    d.ellipse([cx - 11, y0 + 4, cx + 11, y1 - 4], outline=colour, width=3)
    d.line([(x0 + 4, cy), (x1 - 4, cy)], fill=colour, width=3)
    d.arc([x0 + 8, y0 + 14, x1 - 8, y1 - 14], 200, 340, fill=colour,
          width=3)


# --- the page --------------------------------------------------------------

def story(d, x, y, width, kicker, colour, icon, headline, body,
          head_size=25):
    """One story block: kicker, icon, headline, body. Returns bottom y."""
    d.text((x, y), kicker, font=bold(17), fill=colour)
    if icon is not None:
        icon(d, (x + width - 58, y - 6, x + width, y + 52), colour)
    y += 26
    y = block(d, x, y, headline, bold(head_size), INK, width - 68, 31)
    y += 4
    y = block(d, x, y, body, plain(17), BODY, width - 6, 23)
    return y


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, SIZE - 1, SIZE - 1], outline=INK, width=4)

    # Masthead.
    d.rectangle([4, 4, SIZE - 5, 148], fill=CRIMSON)
    spaced(d, 38, 22, "THE WORLD IN ONE DAY", bold(24), GOLD, 5)
    d.text((36, 54), "WEDNESDAY, 18 NOVEMBER 2026",
           font=serif_bold(48), fill=CREAM)
    rule(d, 38, SIZE - 38, 118, GOLD, 2)
    d.text((38, 126), "The Gulf burns again — and the stories that made the day",
           font=plain(18), fill=(232, 200, 200))

    # Lead story, with the sea panel on the right.
    y = 166
    d.text((36, y), "THE GULF, OVERNIGHT", font=bold(21), fill=CRIMSON)
    y += 32
    y = block(d, 36, y,
              "US sinks five Iranian tankers — Tehran fires missiles "
              "at a Jordan base",
              bold(34), INK, 660, 41)
    y += 6
    y = block(d, 36, y,
              "Washington said it destroyed five oil tankers tied to "
              "Iran's Revolutionary Guard — four in the Gulf of Oman "
              "and one near Kharg Island — after the Guard twice fired "
              "ballistic missiles at a US warship. Iran answered with "
              "20 missiles at the Al-Azraq base in Jordan; 18 were "
              "shot down.",
              plain(19), BODY, 660, 26)
    draw_tanker(d, (724, 168, 988, 448))

    rule(d, 36, SIZE - 36, 466)

    # Second row: Israel and Ukraine.
    col_w = 464
    story(d, 36, 482, col_w, "ISRAEL", NAVY, draw_parliament,
          "Herzog hands Eisenkot the mandate",
          "Israel's president asked Gadi Eisenkot to form the next "
          "government, after 67 lawmakers backed him against 46 for "
          "Netanyahu. He has 28 days to win 61 seats.")
    story(d, 524, 482, col_w, "UKRAINE", BLUE, draw_bridge,
          "Kerch Bridge hit a second night as the summit nears",
          "Ukrainian drones struck the bridge to Crimea for a second "
          "night running, shutting the crossing, while Russia hit "
          "bridges near Kyiv. The strikes come a day before Trump, "
          "Putin and Xi meet in Shenzhen.")

    rule(d, 36, SIZE - 36, 674)

    # Third row: Gaza and the climate talks.
    story(d, 36, 690, col_w, "GAZA", TEAL, draw_snowflake,
          "UN warns of cold deaths in Gaza as winter sets in",
          "More than 1.7 million remain displaced and 1.4 million "
          "face acute hunger, the UN said, as four Western allies "
          "urged Israel to open crossings for aid.")
    story(d, 524, 690, col_w, "CLIMATE", GREEN, draw_globe,
          "COP31 enters its decisive phase in Antalya",
          "Negotiators are working through a draft deal with 144 "
          "disputed items, including a faster fossil-fuel phase-out "
          "and $120bn a year in climate finance.")

    # Also on this day.
    y = 858
    rule(d, 36, SIZE - 36, y)
    y += 12
    d.text((36, y), "ALSO ON 18 NOVEMBER", font=bold(19), fill=CRIMSON)
    y += 28
    items = [
        ("France — ", "Fourth weekend of cost-of-living protests; "
         "146,000 march as unions strike."),
        ("Europe — ", "Cyber-attack knocks out supermarket freezers "
         "in seven countries."),
        ("Health — ", "US measles cases reach a 40-year high as "
         "vaccination rates fall."),
        ("Asia — ", "Quad leaders meet in Manila; Trump heads on to "
         "China for Thursday's summit."),
    ]
    for lead, rest in items:
        d.text((36, y), lead, font=bold(16), fill=INK)
        off = d.textlength(lead, font=bold(16))
        d.text((36 + off, y), rest, font=plain(16), fill=BODY)
        y += 22

    # Footer.
    rule(d, 36, SIZE - 36, 992, SLATE, 1)
    d.text((36, 998), "Sources: Al Jazeera · Reuters · NPR · The Guardian · UN News",
           font=plain(14), fill=SLATE)
    stamp = "18 NOVEMBER 2026"
    d.text((SIZE - 36 - d.textlength(stamp, font=bold(14)), 996),
           stamp, font=bold(14), fill=SLATE)
    return img


if __name__ == "__main__":
    poster = build()
    poster.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", poster.size)
