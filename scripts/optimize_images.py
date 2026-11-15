"""Generate small, properly sized WebP variants from existing site artwork.

Run from repo root: python scripts/optimize_images.py
No external image hosts or new original artwork are needed.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
OUT = ASSETS / 'optimized'
# (source image, output stem, target widths, image quality, mode)
SPECS = [
    ('area81-bg.png', 'area81-cover', (480, 960), 78, 'cover'),
    ('guildmaster-bg.png', 'guildmaster-cover', (480, 800), 76, 'cover'),
    ('biomebites-bg.png', 'biomebites-cover', (480, 800), 76, 'cover'),
    ('area81-logo.png', 'area81-icon', (160,), 82, 'contain'),
]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, name, sizes, quality, mode in SPECS:
        src = ASSETS / filename
        if not src.is_file():
            raise FileNotFoundError(f'Missing source: {src}')
        with Image.open(src) as original:
            original = ImageOps.exif_transpose(original)
            for w in sizes:
                if mode == 'cover':
                    # Fill wide game-card crop without distortion; preserve center art.
                    h = round(w * 9 / 16)
                    img = ImageOps.fit(original.convert('RGB'), (w,h), method=Image.Resampling.LANCZOS, centering=(.5,.5))
                else:
                    img = original.convert('RGBA' if 'A' in original.getbands() else 'RGB')
                    img.thumbnail((w,w), Image.Resampling.LANCZOS)
                    canvas = Image.new('RGBA', (w,w), (0,0,0,0))
                    canvas.alpha_composite(img.convert('RGBA'), ((w-img.width)//2, (w-img.height)//2))
                    img = canvas
                out = OUT / f'{name}-{w}.webp'
                img.save(out, 'WEBP', quality=quality, method=6)
                print(f'{filename}: {src.stat().st_size/1024:.0f} KiB -> {out.name}: {out.stat().st_size/1024:.0f} KiB')

if __name__ == '__main__':
    main()