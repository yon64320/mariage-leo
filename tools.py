#!/usr/bin/env python3
"""
Outils pour gérer les images du livre HTML.

Usage :
  python tools.py externalize   # Extrait toutes les images base64 vers dossier photos/
  python tools.py b64 IMAGE.jpg # Affiche le base64 d'une image (à coller dans le HTML)
  python tools.py optimize IMAGE.jpg # Redimensionne et optimise (max 1000px, qualité 82%)
"""

import base64
import os
import re
import sys
from pathlib import Path

HTML_FILE = "discours-mariage.html"


def cmd_externalize():
    """Extract all base64 images from the HTML into a photos/ folder."""
    if not Path(HTML_FILE).exists():
        print(f"❌ {HTML_FILE} not found in current directory")
        return

    photos_dir = Path("photos")
    photos_dir.mkdir(exist_ok=True)

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Find all base64 images
    pattern = r'data:image/(jpeg|png|jpg);base64,([A-Za-z0-9+/=]+)'
    matches = list(re.finditer(pattern, html))
    print(f"Found {len(matches)} base64 images")

    seen_hashes = {}
    counter = 0

    # Process from end to start so positions don't shift
    for match in reversed(matches):
        ext, b64data = match.group(1), match.group(2)
        # Hash the data to detect duplicates
        h = hash(b64data)

        if h in seen_hashes:
            filename = seen_hashes[h]
        else:
            counter += 1
            filename = f"img-{counter:02d}.{'jpg' if ext == 'jpeg' else ext}"
            filepath = photos_dir / filename
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(b64data))
            seen_hashes[h] = filename
            print(f"  ✓ Saved {filename} ({len(b64data) // 1024} KB)")

        # Replace in HTML
        html = html[:match.start()] + f"photos/{filename}" + html[match.end():]

    # Backup original
    backup = HTML_FILE.replace(".html", ".base64-backup.html")
    if not Path(backup).exists():
        Path(HTML_FILE).rename(backup)
        print(f"📦 Original saved as {backup}")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Done. {counter} unique images in photos/")
    print(f"   New HTML size: {len(html) // 1024} KB")


def cmd_b64(image_path):
    """Print base64 data URL for an image."""
    if not Path(image_path).exists():
        print(f"❌ {image_path} not found")
        return

    ext = Path(image_path).suffix.lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"

    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    result = f"data:image/{ext};base64,{data}"
    print(result)
    print(f"\n# Length: {len(result)} chars (~{len(result) // 1024} KB)", file=sys.stderr)


def cmd_optimize(image_path):
    """Resize an image to max 1000px and re-encode at quality 82%."""
    try:
        from PIL import Image
    except ImportError:
        print("❌ Need Pillow: pip install Pillow")
        return

    if not Path(image_path).exists():
        print(f"❌ {image_path} not found")
        return

    img = Image.open(image_path)
    print(f"Original: {img.size}, mode: {img.mode}")

    img.thumbnail((1000, 1000), Image.LANCZOS)
    img = img.convert("RGB")

    out = Path(image_path).stem + "_small.jpg"
    img.save(out, "JPEG", quality=82, optimize=True)

    size = Path(out).stat().st_size
    print(f"Saved {out}: {img.size}, {size // 1024} KB")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "externalize":
        cmd_externalize()
    elif cmd == "b64" and len(sys.argv) >= 3:
        cmd_b64(sys.argv[2])
    elif cmd == "optimize" and len(sys.argv) >= 3:
        cmd_optimize(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
