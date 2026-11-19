"""Inspiration pour une notion à faire comprendre : comment d'autres l'ont dessinée. Une planche de résultats Bing
Images par requête, capturée par Chrome sans interface, à lire pour repérer les formes qui reviennent (un curseur, deux
histogrammes comparés, un nuage de points groupés…), puis à redessiner avec les helpers dans la charte OCTO.

    uv run --with pillow python scripts/inspiration.py <dossier> "temperature|LLM temperature explained diagram" …

    → <dossier>/inspiration_<clé>.png (une planche de 1 400 x 2 600 pixels par requête)

Les images vues ici ne vont jamais dans le deck : leurs droits sont inconnus et leur style n'est pas celui d'OCTO.
Google Images renvoie une page « trafic inhabituel » (captcha) aux navigateurs pilotés : ne pas la contourner, Bing
montre la même mosaïque. Voir references/images.md §7.
"""
import sys
import urllib.parse
from pathlib import Path

from maquette import find_chrome, run_chrome

BING = "https://www.bing.com/images/search?setlang=fr&q="
WIDTH, HEIGHT, KEEP = 1400, 3200, 2600  # fenêtre capturée, hauteur gardée (le bas se charge mal)


def capture(chrome, query, out):
    """Capture de la mosaïque de résultats d'une requête, rognée à ses premières rangées."""
    shot = out.with_suffix(".full.png")
    run_chrome(chrome, f"--window-size={WIDTH},{HEIGHT}", "--lang=fr-FR", f"--screenshot={shot}",
               BING + urllib.parse.quote_plus(query))
    if not shot.exists():
        return False
    try:
        from PIL import Image
        Image.open(shot).crop((0, 0, WIDTH, KEEP)).save(out)
        shot.unlink()
    except ImportError:
        shot.rename(out)
    return True


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    chrome = find_chrome()
    if not chrome:
        sys.exit("Chrome ou Chromium introuvable : passer par le MCP Chrome DevTools (bing.com/images), ou par la "
                 "recherche web de la session")
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    for arg in sys.argv[2:]:
        key, query = arg.split("|", 1) if "|" in arg else (arg.split()[0], arg)
        out = out_dir / f"inspiration_{key}.png"
        print(f"{out} : {query}" if capture(chrome, query, out) else f"échec de la capture : {query}")


if __name__ == "__main__":
    main()
