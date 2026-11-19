"""Images d'un deck existant (une formation OCTO, un deck client fourni), pour en reprendre des illustrations :
captures, schémas, unes de presse, photos. Chaque image n'est extraite qu'une fois, avec la slide où elle apparaît ;
des planches de vignettes permettent de choisir à l'œil.

    uv run --with python-pptx --with pillow python scripts/extract_images.py deck.pptx <dossier>

    → <dossier>/img/s<slide>_<n>_<empreinte>.<ext>, <dossier>/index.json, <dossier>/planche_NN.png

On reprend le contenu, jamais le style (references/charte.md). Avant d'en mettre une dans un deck : vérifier ses droits
(une photo de presse ou de banque d'images d'un deck interne n'est pas forcément réutilisable), la recadrer avec
Deck.photo() ou la poser avec Deck.photo_fit(), et la créditer. Voir references/images.md.
"""
import hashlib
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu


def _pictures(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _pictures(sh.shapes)
        elif hasattr(sh, "image"):
            yield sh


def extract(pptx, out):
    img_dir = out / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    seen, index = {}, []
    for n, slide in enumerate(Presentation(str(pptx)).slides, 1):
        for k, sh in enumerate(_pictures(slide.shapes)):
            try:
                img = sh.image
            except (ValueError, KeyError):
                continue  # image liée, pas incluse dans le fichier
            digest = hashlib.md5(img.blob).hexdigest()[:10]
            if digest not in seen:
                seen[digest] = f"s{n:03d}_{k}_{digest}.{img.ext}"
                (img_dir / seen[digest]).write_bytes(img.blob)
            index.append({"slide": n, "fichier": seen[digest], "pixels": list(img.size),
                          "pouces": [round(Emu(sh.width).inches, 2), round(Emu(sh.height).inches, 2)]})
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
    return [img_dir / f for f in seen.values()]


def sheets(files, out, per_sheet=36, size=230, cols=6):
    from PIL import Image, ImageDraw
    Image.MAX_IMAGE_PIXELS = None
    for s in range(0, len(files), per_sheet):
        chunk = files[s:s + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        canvas = Image.new("RGB", (cols * (size + 10), rows * (size + 30)), "white")
        draw = ImageDraw.Draw(canvas)
        for i, f in enumerate(chunk):
            x, y = (i % cols) * (size + 10), (i // cols) * (size + 30)
            try:
                im = Image.open(f)
                im.thumbnail((size, size))
                bg = Image.new("RGB", im.size, (230, 230, 230))
                im = im.convert("RGBA")
                bg.paste(im, mask=im.split()[-1])
                canvas.paste(bg, (x, y))
            except OSError as e:  # format non lu par Pillow (emf, wmf, svg)
                draw.text((x, y + 10), f"{f.suffix} : {e}"[:40], fill="red")
            draw.text((x, y + size + 4), f.stem[:28], fill="black")
        canvas.save(out / f"planche_{s // per_sheet + 1:02d}.png")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    out = Path(sys.argv[2])
    files = extract(Path(sys.argv[1]), out)
    print(f"{len(files)} image(s) unique(s) dans {out / 'img'}")
    try:
        sheets(files, out)
        print(f"planches : {out}/planche_*.png")
    except ImportError:
        print("Pillow absent : pas de planche (ajouter --with pillow)")
