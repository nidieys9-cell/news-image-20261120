#!/usr/bin/env python3
"""news-image-20261120 — draw the day's front page by hand, in code.

One 1024x1024 PNG that sums up Friday 20 November 2026: one top story
plus six stories from six different fields. Every fact in here was
checked against same-day reporting; the sources are listed in README.md.

Run:  python3 draw.py        -> writes entry.png next to this file.
The picture is fully deterministic: same code, same bytes, every run.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PAPER = (247, 242, 231)      # warm newsprint
INK = (24, 28, 38)           # near-black
NAVY = (18, 38, 76)          # masthead
RED = (178, 34, 34)          # headline accent
CARD = (255, 255, 255)
MUTED = (92, 96, 104)
LINE = (214, 206, 188)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 58)
F_SUB = font(SANS_B, 20)
F_KICK = font(SANS_B, 19)
F_HEAD = font(SERIF_B, 36)
F_SUM = font(SANS, 21)
F_CAT = font(SANS_B, 17)
F_CARD_T = font(SANS_B, 24)
F_CARD_B = font(SANS, 18)
F_FOOT = font(SANS, 16)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
# Small hand-drawn style glyphs, one per story, drawn with plain shapes.

def icon_storm(d, x, y, c):
    for r in (34, 24, 14):
        d.arc([x - r, y - r, x + r, y + r], start=200, end=120, fill=c, width=4)


def icon_talk(d, x, y, c):
    d.rounded_rectangle([x - 34, y - 26, x + 2, y + 8], radius=10,
                        outline=c, width=4)
    d.rounded_rectangle([x - 2, y - 6, x + 34, y + 28], radius=10,
                        outline=c, width=4)
    d.line([x - 22, y - 12, x - 8, y - 12], fill=c, width=3)
    d.line([x + 8, y + 8, x + 22, y + 8], fill=c, width=3)


def icon_scales(d, x, y, c):
    d.line([x, y - 30, x, y + 28], fill=c, width=4)
    d.line([x - 30, y - 22, x + 30, y - 22], fill=c, width=4)
    d.polygon([(x - 42, y + 6), (x - 18, y + 6), (x - 30, y - 18)], outline=c)
    d.polygon([(x + 18, y + 6), (x + 42, y + 6), (x + 30, y - 18)], outline=c)
    d.line([x - 26, y + 28, x + 26, y + 28], fill=c, width=4)


def icon_rocket(d, x, y, c):
    d.polygon([(x, y - 34), (x + 16, y + 6), (x - 16, y + 6)], fill=c)
    d.ellipse([x - 5, y - 8, x + 5, y + 2], fill=PAPER)
    d.line([x - 12, y + 14, x - 20, y + 30], fill=c, width=4)
    d.line([x + 12, y + 14, x + 20, y + 30], fill=c, width=4)
    d.ellipse([x - 38, y - 32, x - 34, y - 28], fill=c)
    d.ellipse([x + 30, y - 8, x + 34, y - 4], fill=c)


def icon_pad(d, x, y, c):
    d.rounded_rectangle([x - 36, y - 18, x + 36, y + 20], radius=16,
                        outline=c, width=4)
    d.line([x - 24, y, x - 12, y], fill=c, width=3)
    d.line([x - 18, y - 6, x - 18, y + 6], fill=c, width=3)
    d.ellipse([x + 12, y - 8, x + 20, y], fill=c)
    d.ellipse([x + 22, y + 2, x + 30, y + 10], fill=c)


def icon_chart(d, x, y, c):
    d.line([x - 34, y + 26, x + 34, y + 26], fill=c, width=4)
    for bx, bh in ((-26, 18), (-8, 30), (10, 22), (26, 40)):
        d.rectangle([x + bx - 6, y + 26 - bh, x + bx + 6, y + 26], fill=c)


ICONS = {
    "storm": icon_storm,
    "talk": icon_talk,
    "scales": icon_scales,
    "rocket": icon_rocket,
    "pad": icon_pad,
    "chart": icon_chart,
}

# ---------------------------------------------------------------- stories

HEADLINE = {
    "kicker": "TOP STORY  ·  WASHINGTON",
    "title": "Trump puts any Iran war decision off to 2027",
    "body": ("The US president says there is \u201cno rush\u201d and he will "
             "\u201csee what happens\u201d after 1 January \u2014 pushing a "
             "decision on Iran into next year.  — Reuters, 20 Nov"),
}

CARDS = [
    {
        "cat": "WEATHER", "color": (31, 120, 180), "icon": "storm",
        "title": "Cyclone Akvan hits India\u2019s east coast",
        "body": ("Akvan makes landfall near Gopalpur, Odisha, at noon. Over "
                 "300,000 people evacuated; 423 rescue teams deployed. "
                 "— ANI, 20 Nov"),
    },
    {
        "cat": "DIPLOMACY", "color": (46, 125, 87), "icon": "talk",
        "title": "Europe ready to talk with Russia on Ukraine",
        "body": ("At a Berlin summit, leaders say they will negotiate an "
                 "end to the war — with Kyiv and Europe at the table. "
                 "— BBC, 20 Nov"),
    },
    {
        "cat": "JUSTICE", "color": (122, 63, 120), "icon": "scales",
        "title": "UN court: Myanmar committed genocide",
        "body": ("The ICJ rules 9\u20136 that the 2017 crackdown on the "
                 "Rohingya was genocide — a first for a state. "
                 "— BBC / Reuters"),
    },
    {
        "cat": "SPACE", "color": (196, 110, 24), "icon": "rocket",
        "title": "Voyager 1 is now a light-day away",
        "body": ("NASA confirms the 49-year-old probe has passed 16 billion "
                 "miles out; a signal now takes a day to reach it. "
                 "— NASA / Reuters"),
    },
    {
        "cat": "CULTURE", "color": (178, 34, 34), "icon": "pad",
        "title": "GTA VI out-earns a Hollywood epic",
        "body": ("An estimated $1.84bn in a day passes the entire $1.80bn "
                 "global box office of Nolan\u2019s The Odyssey. "
                 "— Sensor Tower / Reuters"),
    },
    {
        "cat": "BUSINESS", "color": (24, 96, 110), "icon": "chart",
        "title": "Anthropic joins the market at $1.5tn",
        "body": ("The AI lab behind Claude starts trading on Nasdaq as ANT "
                 "after a record $81bn IPO. Deal closes 20 Nov. "
                 "— Wall Street Journal"),
    },
]

# ---------------------------------------------------------------- drawing

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((36, 18), "THE WORLD TODAY", font=F_TITLE, fill=(255, 255, 255))
d.text((36, 84), "FRIDAY  ·  20 NOVEMBER 2026  ·  ONE DAY, SEVEN STORIES",
       font=F_SUB, fill=(196, 205, 224))

# Headline card
d.rounded_rectangle([28, 134, W - 28, 340], radius=10, fill=CARD,
                    outline=LINE, width=2)
d.rectangle([28, 134, 40, 340], fill=RED)
d.text((60, 152), HEADLINE["kicker"], font=F_KICK, fill=RED)
y = 182
y = draw_lines(d, wrap(d, HEADLINE["title"], F_HEAD, 900), F_HEAD,
               60, y, INK, 44)
draw_lines(d, wrap(d, HEADLINE["body"], F_SUM, 900), F_SUM, 60, y + 6,
           (52, 56, 66), 28)

# Story grid: 2 columns x 3 rows
GX, GY, CW, CH, GAP = 28, 352, 476, 192, 12
for i, card in enumerate(CARDS):
    col, row = i % 2, i // 2
    x0 = GX + col * (CW + GAP)
    y0 = GY + row * (CH + GAP)
    c = card["color"]
    d.rounded_rectangle([x0, y0, x0 + CW, y0 + CH], radius=10, fill=CARD,
                        outline=LINE, width=2)
    d.rounded_rectangle([x0, y0, x0 + CW, y0 + 8], radius=4, fill=c)
    d.text((x0 + 18, y0 + 20), card["cat"], font=F_CAT, fill=c)
    ICONS[card["icon"]](d, x0 + CW - 52, y0 + 52, c)
    ty = y0 + 48
    ty = draw_lines(d, wrap(d, card["title"], F_CARD_T, 330), F_CARD_T,
                    x0 + 18, ty, INK, 29)
    draw_lines(d, wrap(d, card["body"], F_CARD_B, CW - 36), F_CARD_B,
               x0 + 18, ty + 6, (52, 56, 66), 23)

# Footer
d.line([28, 960, W - 28, 960], fill=LINE, width=2)
d.text((28, 970),
       "Sources: Reuters · BBC · NASA · ANI · Sensor Tower · Wall Street Journal",
       font=F_FOOT, fill=MUTED)
d.text((28, 992),
       "All seven stories were reported on 20 November 2026; dates of the underlying events are in README.md.",
       font=F_FOOT, fill=MUTED)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
