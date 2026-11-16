"""Generate the St. Mary's Painting Works brand assets with Pillow.

Run from the repository root:

    python scripts/make-brand-assets.py

The script is idempotent: rerunning it rewrites the same seven files with the
same bytes. It only writes to public/ and only reads assets/logo.png.

Outputs (all under public/):
    logo-accent.png       96x96 transparent crop of the halo portrait
    favicon.svg           vector navy tile, gold ring, white S
    apple-touch-icon.png  180x180
    icon-192.png          192x192
    icon-512.png          512x512
    og.jpg                1200x630, kept under 200 KB
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
LOGO = ROOT / "assets" / "logo.png"

NAVY = "#0B1F3A"
GOLD = "#F0A010"
WHITE = "#FFFFFF"

# Curly apostrophe (U+2019) and middle dot (U+00B7) via escapes so the source
# stays pure ASCII and the exact glyphs survive any checkout/encoding setup.
SHORT_NAME = "St. Mary\u2019s Painting Works"
OG_SUBTITLE = "Ulsoor, Bangalore \u00b7 Since 1980"

OG_SIZE = (1200, 630)
OG_BUDGET = 200 * 1024

# Fonts are resolved at run time so the script works on Windows, macOS and
# common Linux images without any extra dependency.
BOLD_FONTS = [
    Path("C:/Windows/Fonts/arialbd.ttf"),
    Path("C:/Windows/Fonts/seguisb.ttf"),
    Path("/Library/Fonts/Arial Bold.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
]


def bold_font(size):
    """Return a bold TrueType font at the requested pixel size."""
    for path in BOLD_FONTS:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise SystemExit("No bold system font found; install DejaVu or Arial Bold")


def accent(size):
    """Crop the halo portrait out of the logo and downscale it cleanly.

    The logo is a transparent RGBA emblem. We find the visible ring with an
    alpha threshold, take a centred square around it (with a hair of margin so
    the gold edge is never clipped) and resize with LANCZOS.
    """
    im = Image.open(LOGO).convert("RGBA")
    alpha = im.getchannel("A")
    visible = alpha.point(lambda p: 255 if p > 10 else 0)
    box = visible.getbbox()
    if box is None:
        raise SystemExit(f"{LOGO} has no visible pixels")

    left, top, right, bottom = box
    side = max(right - left, bottom - top)
    cx = (left + right) // 2
    cy = (top + bottom) // 2
    half = round(side / 2 * 1.02)  # 2% transparent breathing room
    crop = (cx - half, cy - half, cx + half, cy + half)

    return im.crop(crop).resize((size, size), Image.LANCZOS)


def icon_mark(size):
    """Render the navy tile + gold ring + white S mark at any pixel size."""
    img = Image.new("RGBA", (size, size), NAVY)
    draw = ImageDraw.Draw(img)

    inset = round(size * 0.18)
    ring = max(1, round(size * 0.06))
    draw.ellipse(
        (inset, inset, size - inset - 1, size - inset - 1),
        outline=GOLD,
        width=ring,
    )

    font = bold_font(round(size * 0.52))
    bbox = draw.textbbox((0, 0), "S", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]),
        "S",
        font=font,
        fill=WHITE,
    )
    return img


def favicon_svg():
    """A simple vector mark that stays legible when shown at 16 px."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        f'  <rect width="64" height="64" fill="{NAVY}"/>\n'
        f'  <circle cx="32" cy="32" r="23" fill="none" stroke="{GOLD}" '
        'stroke-width="5"/>\n'
        f'  <text x="32" y="32" dy=".35em" fill="{WHITE}" '
        'font-family="Arial, Helvetica, sans-serif" font-size="34" '
        'font-weight="bold" text-anchor="middle">S</text>\n'
        '</svg>\n'
    )


def fit_font(text, max_width, start_size):
    """Shrink a bold font until the text fits the available width."""
    size = start_size
    while size > 8:
        font = bold_font(size)
        if font.getbbox(text)[2] - font.getbbox(text)[0] <= max_width:
            return font
        size -= 1
    return bold_font(size)


def og_image():
    """1200x630 Open Graph card: navy, accent logo and the two brand lines."""
    img = Image.new("RGB", OG_SIZE, NAVY)
    draw = ImageDraw.Draw(img)

    logo = accent(180).convert("RGBA")
    img.paste(logo, (110, (OG_SIZE[1] - logo.height) // 2), logo)

    # Text column to the right of the logo.
    left = 110 + logo.width + 56
    right_margin = 90
    width = OG_SIZE[0] - left - right_margin

    title_font = fit_font(SHORT_NAME, width, 64)
    sub_font = fit_font(OG_SUBTITLE, width, 32)
    title_h = title_font.getbbox(SHORT_NAME)[3] - title_font.getbbox(SHORT_NAME)[1]
    sub_h = sub_font.getbbox(OG_SUBTITLE)[3] - sub_font.getbbox(OG_SUBTITLE)[1]
    gap = 24
    block_h = title_h + gap + sub_h
    top = (OG_SIZE[1] - block_h) // 2

    def line(text, font, fill, y):
        bbox = draw.textbbox((0, 0), text, font=font)
        draw.text((left - bbox[0], y - bbox[1]), text, font=font, fill=fill)

    line(SHORT_NAME, title_font, WHITE, top)
    line(OG_SUBTITLE, sub_font, GOLD, top + title_h + gap)

    for quality in range(88, 59, -4):
        img.save(PUBLIC / "og.jpg", "JPEG", quality=quality, optimize=True,
                 progressive=True)
        if (PUBLIC / "og.jpg").stat().st_size <= OG_BUDGET:
            return
    raise SystemExit("og.jpg exceeds 200 KB even at low JPEG quality")


def main():
    PUBLIC.mkdir(parents=True, exist_ok=True)

    acc = accent(96)
    acc.save(PUBLIC / "logo-accent.png")

    (PUBLIC / "favicon.svg").write_text(favicon_svg(), encoding="utf-8")

    for name, size in (
        ("apple-touch-icon.png", 180),
        ("icon-192.png", 192),
        ("icon-512.png", 512),
    ):
        icon_mark(size).save(PUBLIC / name)

    og_image()

    print("logo-accent.png      96x96")
    print("favicon.svg          vector (64x64 viewBox)")
    print("apple-touch-icon.png 180x180")
    print("icon-192.png         192x192")
    print("icon-512.png         512x512")
    og_kb = (PUBLIC / "og.jpg").stat().st_size / 1024
    print(f"og.jpg               {OG_SIZE[0]}x{OG_SIZE[1]} ({og_kb:.1f} KB)")


if __name__ == "__main__":
    main()
