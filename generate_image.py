"""Generate entry.png (1024x1024) for make.fun ai-excited-01 round 9.

Concept: the IMPOSSIBLE sun. A colossal sun cracking open like a cosmic
doorway, revealing a gigantic glowing eye / second universe inside. A small
robot on a dark cliff leans back against the force, one arm shielding its
face, the other reaching toward the light. Particles stream into the sun,
clouds bend inward, the cliff fractures into floating fragments.
Palette: gold / amber / rose / violet. Enormous scale contrast.
Everything is drawn fresh with PIL; no input image is read.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W = H = 1024
random.seed(20261116)
CX, CY, R = 640, 360, 320  # sun centre + radius


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def radial_disc(size, cx, cy, radius, stops):
    """Layer with a radial-gradient disc. stops: [(t, rgb), ...] sorted."""
    layer = Image.new("RGB", size, (0, 0, 0))
    d = ImageDraw.Draw(layer)
    for r in range(radius, 0, -1):
        t = 1.0 - r / radius
        col = stops[-1][1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                tt = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
                col = lerp(stops[i][1], stops[i + 1][1], tt)
                break
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return layer


# ---------------------------------------------------------------- sky
sky = Image.new("RGB", (W, H))
sd = ImageDraw.Draw(sky)
sky_stops = [
    (0.00, (22, 9, 44)),
    (0.30, (56, 18, 66)),
    (0.55, (104, 38, 62)),
    (0.78, (146, 64, 54)),
    (1.00, (34, 14, 32)),
]
for y in range(H):
    t = y / (H - 1)
    col = sky_stops[-1][1]
    for i in range(len(sky_stops) - 1):
        if sky_stops[i][0] <= t <= sky_stops[i + 1][0]:
            tt = (t - sky_stops[i][0]) / (sky_stops[i + 1][0] - sky_stops[i][0])
            col = lerp(sky_stops[i][1], sky_stops[i + 1][1], tt)
            break
    sd.line([(0, y), (W, y)], fill=col)

# stars (denser away from the sun)
stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
std = ImageDraw.Draw(stars)
for _ in range(260):
    x = random.uniform(0, W)
    y = random.uniform(0, H * 0.62)
    d = math.hypot(x - CX, y - CY)
    if d < R + 40:
        continue
    r = random.uniform(0.6, 1.9)
    a = random.randint(90, 230)
    warm = random.random() < 0.4
    col = (255, 220, 160, a) if warm else (235, 225, 255, a)
    std.ellipse([x - r, y - r, x + r, y + r], fill=col)
img = Image.alpha_composite(sky.convert("RGBA"), stars)

# ---------------------------------------------------------------- sun glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([CX - R - 30, CY - R - 30, CX + R + 30, CY + R + 30],
           fill=(255, 150, 60, 150))
glow = glow.filter(ImageFilter.GaussianBlur(70))
img = Image.alpha_composite(img, glow)

# sun disc
sun_stops = [
    (0.00, (255, 246, 205)),
    (0.30, (255, 202, 88)),
    (0.60, (244, 148, 58)),
    (0.85, (220, 86, 52)),
    (1.00, (168, 46, 74)),
]
sun = radial_disc((W, H), CX, CY, R, sun_stops)
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.ellipse([CX - R, CY - R, CX + R, CY + R], fill=255)
img.paste(sun, (0, 0), mask)

# light beams fanning out of the sun
beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beams)
for ang_deg, spread, length, alpha in [
    (-160, 7, 620, 34), (-115, 5, 700, 30), (-65, 6, 640, 34),
    (-25, 5, 560, 28), (155, 6, 600, 26), (115, 5, 520, 24),
]:
    a = math.radians(ang_deg)
    tip = (CX + length * math.cos(a), CY + length * math.sin(a))
    perp = math.radians(ang_deg + 90)
    wdt = spread
    base1 = (CX + wdt * math.cos(perp), CY + wdt * math.sin(perp))
    base2 = (CX - wdt * math.cos(perp), CY - wdt * math.sin(perp))
    bd.polygon([base1, base2, tip], fill=(255, 196, 100, alpha))
beams = beams.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, beams)

# ---------------------------------------------------------------- the opening: the eye
# bright lens (the doorway) inside the sun
lens = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(lens)
# outer glow of the doorway
ld.ellipse([CX - 118, CY - 235, CX + 118, CY + 235], fill=(255, 240, 190, 90))
lens = lens.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, lens)

# lens body: vertical almond of blinding light
lens2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
l2d = ImageDraw.Draw(lens2)
for k in range(100, 0, -1):
    t = k / 100.0
    rx, ry = 96 * t, 208 * t
    col = lerp((255, 250, 225), (255, 196, 90), 1 - t)
    l2d.ellipse([CX - rx, CY - ry, CX + rx, CY + ry],
                fill=col + (255,))
# crisp bright rim of the doorway
l2d.ellipse([CX - 96, CY - 208, CX + 96, CY + 208],
            outline=(255, 244, 200, 255), width=4)
img = Image.alpha_composite(img, lens2)

# tiny stars of the "second universe" inside the doorway
inner = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ind = ImageDraw.Draw(inner)
for _ in range(46):
    ang = random.uniform(0, 2 * math.pi)
    rr = random.uniform(0, 1)
    x = CX + 88 * rr * math.cos(ang)
    y = CY + 200 * rr * math.sin(ang)
    if math.hypot((x - CX) / 88.0, (y - CY) / 200.0) > 1:
        continue
    if math.hypot(x - CX, y - CY) < 86:  # keep iris clean
        continue
    r = random.uniform(0.7, 1.8)
    ind.ellipse([x - r, y - r, x + r, y + r],
                fill=(255, 255, 240, random.randint(140, 255)))
img = Image.alpha_composite(img, inner)

# the giant eye: iris + pupil
iris = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ird = ImageDraw.Draw(iris)
iris_stops = [
    (0.00, (255, 214, 120)),
    (0.45, (238, 150, 52)),
    (0.80, (176, 84, 62)),
    (1.00, (128, 62, 150)),
]
for r in range(82, 0, -1):
    t = 1.0 - r / 82
    col = iris_stops[-1][1]
    for i in range(len(iris_stops) - 1):
        if iris_stops[i][0] <= t <= iris_stops[i + 1][0]:
            tt = (t - iris_stops[i][0]) / (iris_stops[i + 1][0] - iris_stops[i][0])
            col = lerp(iris_stops[i][1], iris_stops[i + 1][1], tt)
            break
    ird.ellipse([CX - r, CY - r, CX + r, CY + r], fill=col + (255,))
# iris striations
for _ in range(70):
    a = random.uniform(0, 2 * math.pi)
    r0 = random.uniform(30, 78)
    r1 = r0 + random.uniform(6, 18)
    x0, y0 = CX + r0 * math.cos(a), CY + r0 * math.sin(a)
    x1, y1 = CX + r1 * math.cos(a), CY + r1 * math.sin(a)
    ird.line([x0, y0, x1, y1], fill=(120, 50, 30, 110), width=2)
ird.ellipse([CX - 82, CY - 82, CX + 82, CY + 82],
            outline=(90, 40, 110, 255), width=3)
# pupil
ird.ellipse([CX - 34, CY - 34, CX + 34, CY + 34], fill=(18, 7, 24, 255))
ird.ellipse([CX - 34, CY - 34, CX + 34, CY + 34], outline=(255, 200, 110, 220), width=2)
# glint
ird.ellipse([CX - 22, CY - 24, CX - 8, CY - 10], fill=(255, 255, 255, 235))
img = Image.alpha_composite(img, iris)

# ---------------------------------------------------------------- cracks across the sun
cracks = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cracks)
crack_angles = [-78, -52, -30, -8, 14, 38, 62, 88, 112, 138, -105, -135, 165]
for ang_deg in crack_angles:
    a = math.radians(ang_deg)
    # start just outside the lens, end near the sun rim
    r_start = 100 if abs(ang_deg) < 90 else 110
    pts = []
    steps = 7
    for s in range(steps + 1):
        rr = r_start + (R - 12 - r_start) * s / steps
        jitter = random.uniform(-16, 16) if 0 < s < steps else 0
        aa = a + math.radians(jitter * 0.35)
        pts.append((CX + rr * math.cos(aa), CY + rr * math.sin(aa)))
    cd.line(pts, fill=(38, 12, 26, 235), width=9, joint="curve")
    cd.line(pts, fill=(255, 196, 110, 200), width=2, joint="curve")
# peeling shell shards beside the doorway
for poly in [
    [(CX - 100, CY - 190), (CX - 150, CY - 260), (CX - 60, CY - 285), (CX - 88, CY - 205)],
    [(CX + 102, CY + 150), (CX + 168, CY + 230), (CX + 80, CY + 262), (CX + 92, CY + 168)],
    [(CX - 108, CY + 120), (CX - 190, CY + 190), (CX - 110, CY + 215), (CX - 96, CY + 138)],
]:
    cd.polygon(poly, fill=(46, 16, 30, 255), outline=(255, 190, 100, 230))
cracks = cracks.filter(ImageFilter.GaussianBlur(0.6))
img = Image.alpha_composite(img, cracks)

# ---------------------------------------------------------------- clouds bending inward
clouds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cld = ImageDraw.Draw(clouds)
for radius, start, end, col, wdt in [
    (392, 150, 285, (216, 110, 128, 66), 26),
    (430, 200, 330, (168, 92, 168, 60), 34),
    (470, 120, 250, (226, 130, 120, 52), 22),
    (505, 190, 320, (150, 84, 150, 55), 30),
    (545, 140, 300, (210, 120, 140, 44), 26),
    (380, -30, 60, (220, 130, 140, 58), 20),
]:
    cld.arc([CX - radius, CY - radius, CX + radius, CY + radius],
            start=start, end=end, fill=col, width=wdt)
# a couple of low horizontal streaks, also arcing toward the sun
for y0, x0, x1, col in [
    (120, 30, 380, (200, 110, 140, 46)),
    (180, 0, 300, (170, 96, 160, 42)),
    (700, 40, 420, (190, 100, 120, 40)),
]:
    cld.ellipse([x0, y0, x1, y0 + 26], fill=col)
clouds = clouds.filter(ImageFilter.GaussianBlur(9))
img = Image.alpha_composite(img, clouds)

# ---------------------------------------------------------------- particles streaming into the sun
parts = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(parts)
for _ in range(170):
    ang = random.uniform(0, 2 * math.pi)
    rr = random.uniform(R + 30, 560)
    x = CX + rr * math.cos(ang)
    y = CY + rr * math.sin(ang)
    if not (0 <= x < W and 0 <= y < H):
        continue
    # streak pointing at the sun centre
    ln = random.uniform(10, 34)
    dx, dy = (CX - x) / rr, (CY - y) / rr
    a = random.randint(120, 235)
    warm = random.random() < 0.75
    col = (255, 200, 110, a) if warm else (240, 200, 255, a)
    pd.line([x, y, x + dx * ln, y + dy * ln], fill=col, width=2)
    if random.random() < 0.3:
        r = random.uniform(1.2, 2.6)
        pd.ellipse([x - r, y - r, x + r, y + r], fill=col)
parts = parts.filter(ImageFilter.GaussianBlur(0.8))
img = Image.alpha_composite(img, parts)

# ---------------------------------------------------------------- cliff + floating fragments
cliff_top = [(0, 872), (90, 848), (180, 862), (260, 838), (350, 852),
             (430, 830), (520, 846), (610, 828), (700, 852), (790, 836),
             (880, 858), (960, 842), (1024, 860)]
cliff = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cfd = ImageDraw.Draw(cliff)
cfd.polygon(cliff_top + [(1024, H), (0, H)], fill=(13, 7, 22, 255))
# rim light along the cliff top (gold on the sun side, violet elsewhere)
cfd.line(cliff_top, fill=(150, 88, 120, 255), width=2, joint="curve")
cfd.line(cliff_top[5:], fill=(255, 170, 90, 200), width=2, joint="curve")
# glowing fractures inside the cliff
for x0, y0 in [(300, 852), (560, 840), (820, 850)]:
    pts = [(x0, y0)]
    y = y0
    xx = x0
    for _ in range(4):
        xx += random.uniform(-14, 14)
        y += random.uniform(18, 34)
        pts.append((xx, y))
    cfd.line(pts, fill=(255, 130, 60, 200), width=2, joint="curve")
img = Image.alpha_composite(img, cliff)

# floating fragments of the fracturing cliff
frags = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(frags)
for _ in range(12):
    fx = random.uniform(120, 960)
    fy = random.uniform(540, 800)
    s = random.uniform(7, 26)
    rot = random.uniform(0, 2 * math.pi)
    pts = []
    for k in range(5):
        aa = rot + k * 2 * math.pi / 5 + random.uniform(-0.3, 0.3)
        rr = s * random.uniform(0.6, 1.15)
        pts.append((fx + rr * math.cos(aa), fy + rr * math.sin(aa)))
    fd.polygon(pts, fill=(16, 9, 26, 255))
    # sun-facing edge catches the light: brighten the edge nearest the sun
    best = None
    for i in range(len(pts)):
        p1, p2 = pts[i], pts[(i + 1) % len(pts)]
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        d = math.hypot(mx - CX, my - CY)
        if best is None or d < best[0]:
            best = (d, p1, p2)
    fd.line([best[1], best[2]], fill=(255, 180, 100, 235), width=2)
    fd.line(pts + [pts[0]], fill=(120, 80, 110, 160), width=1, joint="curve")
img = Image.alpha_composite(img, frags)

# ---------------------------------------------------------------- the robot
robot = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
rd = ImageDraw.Draw(robot)
metal = (62, 62, 80, 255)
dark = (38, 38, 52, 255)
gold = (255, 190, 100, 255)
# legs
rd.line([96, 148, 88, 186], fill=metal, width=11)
rd.line([112, 148, 120, 186], fill=metal, width=11)
rd.ellipse([78, 182, 98, 192], fill=dark)
rd.ellipse([110, 182, 130, 192], fill=dark)
# body
rd.rounded_rectangle([78, 96, 122, 152], radius=12, fill=metal, outline=gold, width=2)
rd.ellipse([100, 118, 114, 132], fill=(255, 200, 90, 255))  # chest light
rd.line([122, 108, 122, 140], fill=gold, width=2)
# head
rd.rounded_rectangle([82, 58, 118, 96], radius=10, fill=metal, outline=gold, width=2)
rd.line([100, 58, 100, 46], fill=metal, width=4)
rd.ellipse([96, 40, 104, 48], fill=(255, 200, 90, 255))  # antenna tip
# visor: one glowing eye slit
rd.rounded_rectangle([88, 70, 112, 82], radius=6, fill=(255, 205, 95, 255))
# left arm: bent up, shielding the face
rd.line([80, 106, 64, 88], fill=metal, width=9)
rd.line([64, 88, 76, 68], fill=metal, width=9)
rd.ellipse([70, 60, 82, 72], fill=dark, outline=gold, width=1)
# right arm: reaching up toward the sun
rd.line([120, 106, 148, 82], fill=metal, width=9)
rd.line([148, 82, 168, 58], fill=metal, width=9)
rd.ellipse([162, 50, 176, 64], fill=gold)
# visor/chest glow
glow_r = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
grd = ImageDraw.Draw(glow_r)
grd.ellipse([84, 64, 116, 88], fill=(255, 190, 80, 110))
grd.ellipse([96, 114, 118, 136], fill=(255, 190, 80, 90))
glow_r = glow_r.filter(ImageFilter.GaussianBlur(6))
robot = Image.alpha_composite(glow_r, robot)

# lean back ~16 degrees away from the sun, plant feet on the cliff top
robot = robot.rotate(16, resample=Image.BICUBIC, expand=True)
# shadow on the cliff
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shd = ImageDraw.Draw(shadow)
shd.ellipse([330, 838, 500, 862], fill=(0, 0, 0, 130))
shadow = shadow.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img, shadow)
img.alpha_composite(robot, (330, 640))

# ---------------------------------------------------------------- vignette
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
vd.ellipse([-220, -220, W + 220, H + 220], fill=(0, 0, 0, 0))
vig_mask = Image.new("L", (W, H), 0)
vmd = ImageDraw.Draw(vig_mask)
vmd.ellipse([-140, -140, W + 140, H + 140], fill=255)
vig_mask = vig_mask.filter(ImageFilter.GaussianBlur(120))
black = Image.new("RGBA", (W, H), (8, 4, 14, 255))
img = Image.composite(img, black, vig_mask)

img.convert("RGB").save("entry.png", optimize=True)
print("saved entry.png")
