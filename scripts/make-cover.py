# Brighten Anthony's face in assets/cover.png and export the web hero JPEG.
# Run: python scripts/make-cover.py
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "cover.png"
DEST = ROOT / "public" / "gallery" / "cover-anthony.jpg"
SIZE = (720, 1280)


def main():
    im = Image.open(SRC).convert("RGB")
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    # Left man; soft ellipse over his face, feathered heavily.
    draw.ellipse((292, 325, 452, 510), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(38))
    bright = ImageEnhance.Brightness(im).enhance(1.2)
    out = Image.composite(bright, im, mask).resize(SIZE, Image.LANCZOS)
    out.save(DEST, "JPEG", quality=56, optimize=True, progressive=True)
    print(f"{DEST.name} {out.size[0]}x{out.size[1]} {DEST.stat().st_size} bytes")


if __name__ == "__main__":
    main()
