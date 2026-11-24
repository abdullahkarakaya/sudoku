"""PWA simgelerini üretir: icons/*.png (bir kez çalıştırmak yeterli)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "icons"
OUT.mkdir(exist_ok=True)
BG, FG, LINE = (31, 78, 121), (246, 245, 242), (120, 160, 200)
FONT = "C:/Windows/Fonts/segoeuib.ttf"


def icon(size, maskable):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0) if not maskable else BG + (255,))
    d = ImageDraw.Draw(img)
    if not maskable:
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 5, fill=BG + (255,))
    m = size * (0.2 if maskable else 0.14)
    s = (size - 2 * m) / 3
    w = max(1, size // 64)
    for k in range(4):
        d.line([(m + k * s, m), (m + k * s, size - m)], fill=LINE, width=w)
        d.line([(m, m + k * s), (size - m, m + k * s)], fill=LINE, width=w)
    font = ImageFont.truetype(FONT, int(s * 0.72))
    for (r, c), t in {(0, 0): "5", (1, 1): "3", (2, 2): "9", (0, 2): "7", (2, 0): "1"}.items():
        cx, cy = m + c * s + s / 2, m + r * s + s / 2
        d.text((cx, cy), t, font=font, fill=FG, anchor="mm")
    return img


for s in (192, 512):
    icon(s, False).save(OUT / f"icon-{s}.png")
    icon(s, True).save(OUT / f"maskable-{s}.png")
icon(180, True).convert("RGB").save(OUT / "apple-touch-icon.png")
icon(64, False).save(OUT / "favicon.png")
print(sorted(p.name for p in OUT.iterdir()))
