#!/usr/bin/env python3
"""make_og.py — og.png 1200x630 share card for Two Shores Café.
Petrol tide + cream serif + dulce amber; alfajor stack + twin waves. Hard fit assertions."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public", "og.png")

W, H = 1200, 630
TIDE = (10, 44, 55)      # #0a2c37
PETROL = (16, 64, 77)    # #10404d
CREAM = (250, 244, 230)  # #faf4e6
PLATA = (201, 215, 219)  # #c9d7db
AMBER = (209, 138, 58)   # #d18a3a

def SERIF(size):
    cands = [
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Times.ttc",
        "/Library/Fonts/Georgia Bold.ttf",
    ]
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                pass
    return ImageFont.load_default()

def SANS(size, bold=False):
    cands = ([
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ] if bold else [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ])
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                pass
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), TIDE)
d = ImageDraw.Draw(img)

# vertical gradient-ish: petrol panel bottom-left rising
for y in range(H):
    t = y / H
    r = int(TIDE[0] + (PETROL[0] - TIDE[0]) * t * 0.8)
    g = int(TIDE[1] + (PETROL[1] - TIDE[1]) * t * 0.8)
    b = int(TIDE[2] + (PETROL[2] - TIDE[2]) * t * 0.8)
    d.line([(0, y), (W, y)], fill=(r, g, b))

def wave(y0, amp, color, width, x0=0, x1=W, n=3, period=400):
    pts = []
    x = x0
    while x <= x1:
        import math
        y = y0 + amp * math.sin(2 * math.pi * (x - x0) / period)
        pts.append((x, y))
        x += 8
    d.line(pts, fill=color, width=width)

# twin waves near bottom (the two-shores motif)
wave(540, 22, PLATA, 5)
wave(568, 22, AMBER, 5)

x = 72
# eyebrow
f_eye = SANS(26, bold=True)
eye = "URUGUAYAN · ARGENTINIAN COFFEE SHOP & BAKERY"
d.text((x, 78), eye, font=f_eye, fill=AMBER)
lens = d.textlength(eye, font=f_eye)
assert x + lens <= 1128, f"eyebrow too wide: {x + lens}"

# wordmark
f_big = SERIF(96)
wm = "Two Shores Café"
d.text((x, 128), wm, font=f_big, fill=CREAM)
lens = d.textlength(wm, font=f_big)
assert x + lens <= 812, f"wordmark too wide: {x + lens} — shrink font or move art"

# subline
f_sub = SERIF(40)
sub = "Montevideo's counter, rebuilt on"
sub2 = "N Tamiami Trail in Sarasota."
d.text((x, 262), sub, font=f_sub, fill=PLATA)
d.text((x, 312), sub2, font=f_sub, fill=PLATA)
lens = max(d.textlength(sub, font=f_sub), d.textlength(sub2, font=f_sub))
assert x + lens <= 812, f"subline too wide: {x + lens}"

# hours line
f_hrs = SANS(27, bold=True)
hrs = "Mon–Sat 7–5 · Sun 7–3 · (941) 298-9252"
d.text((x, 420), hrs, font=f_hrs, fill=CREAM)
lens = d.textlength(hrs, font=f_hrs)
assert x + lens <= 812, f"hours line too wide: {x + lens}"

f_addr = SANS(24)
addr = "7321 N Tamiami Trail · Sarasota, FL 34243"
d.text((x, 460), addr, font=f_addr, fill=PLATA)
lens = d.textlength(addr, font=f_addr)
assert x + lens <= 812, f"address line too wide: {x + lens}"

# alfajor stack art (right side) — cookie/dulce/cookie + chocolate coat cap
cx, cy = 985, 265
R = 118
def disc(y, color, r=R):
    d.ellipse([cx - r, y - r, cx + r, y + r], fill=color, outline=(8, 30, 38), width=3)
disc(cy + 78, PLATA)           # bottom cookie
rect_y = cy + 12
d.rounded_rectangle([cx - R + 6, rect_y, cx + R - 6, rect_y + 62], radius=28, fill=AMBER)  # dulce filling
disc(cy - 52, PLATA)           # top cookie
d.chord([cx - R, cy - R - 52 + 12, cx + R, cy + 30 - 52], 180, 360, fill=(62, 38, 26))  # choc dome
# dusting dots
import random
random.seed(7)
for _ in range(26):
    px = cx - R + 24 + random.random() * (2 * R - 48)
    py = cy - 52 - 30 + random.random() * 46
    d.ellipse([px, py, px + 5, py + 5], fill=(88, 56, 38))

# crumb dots near bottom right
for i, (px, py) in enumerate([(1096, 470), (1122, 496), (1075, 502)]):
    d.ellipse([px, py, px + 7, py + 7], fill=AMBER)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
