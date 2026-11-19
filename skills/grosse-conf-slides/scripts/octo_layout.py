"""Mise en page des slides OCTO : zones, découpe en colonnes, rangées et grilles, mesure du texte.

On ne pose plus de coordonnées à la main : on part de la zone de contenu de la slide, on la découpe, et chaque helper
reçoit une zone. Les blocs d'une même rangée ont ainsi la même hauteur, les colonnes les mêmes bords, et l'écart est
le même partout. Avec gap=0, les blocs sont emboîtés et partagent leurs bords, comme dans les suggestions de mise en
page de la Com (modèles 41 à 49).

    from octo_layout import CONTENT
    why, droite = CONTENT.cols([3.1, None], gap=0.25)      # 3,1 pouces à gauche, le reste à droite
    g = droite.grid(3, [None, 0.4, None], gap=(0.12, 0))    # 3 rangées : frein | flèche | levier
    d.box(s, *g[0][0], "...")                               # une zone se déballe en x, y, w, h

Toutes les longueurs sont en pouces. Une zone (Frame) est un tuple (x, y, w, h) : elle se passe telle quelle à tous
les helpers de Deck avec *zone.
"""
import re
from collections import namedtuple
from functools import lru_cache
from pathlib import Path

_ASSETS = Path(__file__).resolve().parent.parent / "assets"
# Polices de mesure, par police de la charte : fichiers candidats (le premier trouvé sert), police variable ou non,
# facteur de largeur. Arial se mesure avec Liberation Sans, aux métriques identiques (même chasse, libre) ; Arial Black
# (titres Accenture), qui n'a pas d'équivalent libre, avec Liberation Sans Bold élargie de 20 % (écart mesuré : 13 à 18 %).
MEASURE_FONTS = {
    "Outfit": ([_ASSETS / "fonts" / "Outfit-wght.ttf", Path.home() / "Library" / "Fonts" / "Outfit[wght].ttf"], True, 1.0),
    "Arial": ([_ASSETS / "fonts-accenture" / "LiberationSans-{weight}.ttf"], False, 1.0),
    "Arial Black": ([_ASSETS / "fonts-accenture" / "LiberationSans-{weight}.ttf"], False, 1.2),
}
FONT = "Outfit"  # police de mesure courante : BaseDeck la fixe d'après la charte (use_font)
FONT_FILES = MEASURE_FONTS["Outfit"][0]


def use_font(name):
    """Police de mesure de tout le texte (wrap, text_height, text_width, contrôle de mise en page)."""
    global FONT
    if name not in MEASURE_FONTS:
        raise ValueError(f"police de mesure inconnue : « {name} » ({', '.join(MEASURE_FONTS)})")
    FONT = name


def _sizes(total, spec, gap):
    """Tailles le long d'un axe. spec : un entier (n parts égales) ou une liste dont chaque élément est une taille
    fixe en pouces, None (part égale du reste) ou "2fr" (part pondérée du reste)."""
    if isinstance(spec, int):
        spec = [None] * spec
    weights = [1.0 if s is None else float(s[:-2]) if isinstance(s, str) else 0.0 for s in spec]
    fixed = sum(s for s in spec if isinstance(s, (int, float)) and not isinstance(s, bool))
    free = total - fixed - gap * (len(spec) - 1)
    if free < -1e-6 or (free > 1e-6 and not any(weights)):
        raise ValueError(f"découpe impossible : {total:.2f} pouces pour {spec} avec un écart de {gap}")
    unit = free / sum(weights) if any(weights) else 0
    return [w * unit if w else s for s, w in zip(spec, weights)]


class Frame(namedtuple("Frame", "x y w h")):
    """Zone rectangulaire (pouces). Toutes les méthodes renvoient de nouvelles zones."""

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def cols(self, spec, gap=0.2):
        """Colonnes côte à côte, de même hauteur. gap=0 : colonnes emboîtées (bords partagés)."""
        out, x = [], self.x
        for w in _sizes(self.w, spec, gap):
            out.append(Frame(x, self.y, w, self.h))
            x += w + gap
        return out

    def rows(self, spec, gap=0.2):
        """Rangées empilées, de même largeur."""
        out, y = [], self.y
        for h in _sizes(self.h, spec, gap):
            out.append(Frame(self.x, y, self.w, h))
            y += h + gap
        return out

    def grid(self, rows, cols, gap=0.2):
        """Grille [rangée][colonne] : toutes les cellules d'une rangée ont la même hauteur et toutes celles d'une
        colonne les mêmes bords. gap : un écart, ou (écart entre rangées, écart entre colonnes)."""
        row_gap, col_gap = gap if isinstance(gap, tuple) else (gap, gap)
        return [r.cols(cols, col_gap) for r in self.rows(rows, row_gap)]

    def pad(self, left, top=None, right=None, bottom=None):
        """Zone intérieure : pad(0.2) sur les quatre côtés, pad(0.2, 0.1) horizontal / vertical, ou les quatre."""
        top = left if top is None else top
        right = left if right is None else right
        bottom = top if bottom is None else bottom
        return Frame(self.x + left, self.y + top, self.w - left - right, self.h - top - bottom)

    def top(self, h, gap=0):
        """(bande du haut de hauteur h, reste de la zone sous la bande et l'écart)."""
        return Frame(self.x, self.y, self.w, h), Frame(self.x, self.y + h + gap, self.w, self.h - h - gap)

    def bottom_band(self, h, gap=0):
        """(reste de la zone au-dessus de la bande et de l'écart, bande du bas de hauteur h)."""
        return Frame(self.x, self.y, self.w, self.h - h - gap), Frame(self.x, self.bottom - h, self.w, h)

    def left(self, w, gap=0):
        """(bande de gauche de largeur w, reste à droite)."""
        return Frame(self.x, self.y, w, self.h), Frame(self.x + w + gap, self.y, self.w - w - gap, self.h)

    def right_band(self, w, gap=0):
        """(reste à gauche, bande de droite de largeur w)."""
        return Frame(self.x, self.y, self.w - w - gap, self.h), Frame(self.right - w, self.y, w, self.h)

    def place(self, w=None, h=None, align="tl"):
        """Zone de taille w x h posée dans celle-ci : align = deux lettres, t / m / b puis l / c / r ("mc" : centré)."""
        w, h = self.w if w is None else w, self.h if h is None else h
        x = {"l": self.x, "c": self.cx - w / 2, "r": self.right - w}[align[1]]
        y = {"t": self.y, "m": self.cy - h / 2, "b": self.bottom - h}[align[0]]
        return Frame(x, y, w, h)

    def move(self, dx=0, dy=0):
        """Même zone, décalée de dx vers la droite et de dy vers le bas."""
        return Frame(self.x + dx, self.y + dy, self.w, self.h)

    def union(self, *others):
        """Plus petite zone qui contient celle-ci et les autres (un bloc qui couvre deux cellules d'une grille)."""
        frames = (self, *others)
        x, y = min(f.x for f in frames), min(f.y for f in frames)
        return Frame(x, y, max(f.right for f in frames) - x, max(f.bottom for f in frames) - y)


# Zone de contenu d'une slide de contenu (references/style.md) : sous le sous-titre, au-dessus du numéro de page.
# La pastille du numéro de page occupe le coin bas droit (x > 9,2, y > 5,05) : une zone qui descend jusqu'à 5,2
# s'arrête à droite en 9,2 (CONTENT), ou va jusqu'à 9,5 en s'arrêtant en 5,05 (CONTENT_WIDE).
CONTENT = Frame(0.6, 1.3, 8.6, 3.9)
CONTENT_WIDE = Frame(0.6, 1.3, 8.9, 3.75)
PAGE_NUMBER = Frame(9.2, 5.05, 0.5, 0.35)
SLIDE = Frame(0, 0, 10, 5.625)


# ---------- mesure du texte (police de la charte, comme PowerPoint : use_font) ----------
_MARKUP = re.compile(r"(\*\*.+?\*\*|==.+?==)")
_SCALE = 20  # pixels par point : mesure à 20 fois la taille pour la précision
_BREAK = re.compile(r"(?<= )|(?<=\w-)(?=\w)")  # PowerPoint coupe après une espace ou après le tiret d'un mot composé


@lru_cache(maxsize=None)
def _font(size, bold, name="Outfit"):
    from PIL import ImageFont
    files, variable, _ = MEASURE_FONTS[name]
    for path in files:
        path = Path(str(path).format(weight="Bold" if bold or name == "Arial Black" else "Regular"))
        if path.exists():
            f = ImageFont.truetype(str(path), round(size * _SCALE))
            if variable:
                f.set_variation_by_axes([700 if bold else 400])
            return f
    return None


# Largeur du texte mesuré multipliée par INK. Deck(target="gslides") la porte à GSLIDES_INK : Google Slides ne coupe
# pas les lignes au même endroit que PowerPoint, et un texte calé au plus juste y passe sur une ligne de plus.
# 5 % de marge est une estimation, pas une mesure.
INK = 1.0
GSLIDES_INK = 1.05


def _length(text, size, bold, font=None):
    """Largeur d'un texte sur une ligne, en pouces. font : police du run, si elle est connue et mesurable (« Arial
    Black » dans un deck Arial) ; sinon la police de mesure courante (use_font)."""
    font = font if font in MEASURE_FONTS and font != "Outfit" and FONT != "Outfit" else FONT
    f = _font(size, bold, font)
    widen = MEASURE_FONTS[font][2]
    if f is None:  # police absente : approximation (Outfit : ~0,5 em en regular, ~0,53 em en gras)
        return len(text) * size * (0.53 if bold else 0.5) / 72 * INK * widen
    return f.getlength(text) / _SCALE / 72 * INK * widen


def _words(line, bold=False):
    """Mots d'une ligne balisée, avec leur graisse : [(mot, gras), ...] ; l'espace suit chaque mot."""
    out = []
    for part in _MARKUP.split(line):
        if not part:
            continue
        is_bold = bold or part.startswith(("**", "=="))
        inner = part.strip("*=") if part.startswith(("**", "==")) else part
        for word in _BREAK.split(inner):
            if word:
                out.append((word, is_bold))
    return out


NBSP = " "


FRENCH = True  # typographie française (typo) ; BaseDeck la coupe pour un deck dans une autre langue


def typo(text):
    """Typographie française de la charte, appliquée à tout texte posé par les helpers : espace insécable avant
    « : ; ! ? % » et à l'intérieur des guillemets français. Seules les espaces déjà tapées sont remplacées (« 10:30 »,
    « https:// » restent intacts). Idempotente. Sans effet si FRENCH est faux (deck en anglais)."""
    if not text or not FRENCH:
        return text
    text = re.sub(r" ([:;!?%»])", NBSP + r"\1", text)
    text = re.sub(r"«[  ]*", "«" + NBSP, text)
    return re.sub(r"[  ]*»", NBSP + "»", text)


def lines_of(text):
    """Lignes d'un texte balisé, typographie appliquée (typo). Un **gras** ou un ==mot-clé== qui couvre un retour à
    la ligne est refermé en fin de ligne et rouvert sur la suivante : "**R&D &\nco-innovation**" donne deux lignes en
    gras."""
    out, carry = [], ""
    for line in typo(text).split("\n"):
        bullet = line[:2] if line.startswith(("- ", "> ")) else ""
        body = carry + line[len(bullet):]
        still_open = [m for m in ("**", "==") if body.count(m) % 2]
        out.append(bullet + body + "".join(reversed(still_open)))
        carry = "".join(still_open)
    return out


def wrap(text, w, size, bold=False):
    """Lignes affichées d'un texte balisé dans une largeur utile w (pouces), retour à la ligne aux espaces comme
    PowerPoint. Une puce ("- ", "> ") réduit la largeur de son retrait."""
    lines = []
    for para in lines_of(text):
        width = w
        if para.startswith(("- ", "> ")):
            width -= 0.18 if para[0] == "-" else 0.24
            para = para[2:]
        current, used = "", 0.0
        for word, is_bold in _words(para, bold):
            advance = _length(word, size, is_bold)
            ink = _length(word.rstrip(), size, is_bold)
            if current and used + ink > width:
                lines.append(current.rstrip())
                current, used = "", 0.0
            current += word
            used += advance
        lines.append(current.rstrip())
    return lines


def wrap_runs(runs, w):
    """Retour à la ligne d'un paragraphe aux tailles mélangées (un chiffre clé en 32 pt suivi de son libellé en
    13 pt) : runs = [(texte, gras, taille en pt)]. Renvoie la plus grande taille de chaque ligne affichée."""
    return [size for _, size in _wrap_runs(runs, w)]


def _wrap_runs(runs, w):
    """Comme wrap_runs, avec le texte : [(texte de la ligne, plus grande taille), ...]. Un run peut porter sa
    police en 4e élément (texte, gras, taille, police)."""
    lines, text_, current, used = [], "", 0.0, 0.0
    for text, bold, size, *font in runs:
        font = font[0] if font else None
        for word in _BREAK.split(text):
            if not word:
                continue
            ink = _length(word.rstrip(), size, bold, font)
            if used and used + ink > w:
                lines.append((text_.rstrip(), current))
                text_, current, used = "", 0.0, 0.0
            text_ += word
            current = max(current, size)
            used += _length(word, size, bold, font)
    return lines + [(text_.rstrip(), current or max((r[2] for r in runs), default=0))]


def text_height(text, w, size, bold=False, line_spacing=None, margins=(0.08, 0.04), space_before=0):
    """Hauteur (pouces) qu'occupe un texte balisé dans une boîte de largeur w, marges internes comprises
    (par défaut celles de Deck.text). line_spacing : interligne multiple (défaut de Deck : 1,5 dès 10 pt, sinon 1,2).
    space_before : espace avant chaque paragraphe, en points."""
    line_spacing = line_spacing or (1.5 if size >= 10 else 1.2)
    mx, my = margins
    n = len(wrap(text, w - 2 * mx, size, bold))
    paragraphs = text.count("\n") + 1
    return n * size * LINE_HEIGHT * line_spacing / 72 + (paragraphs - 1) * space_before / 72 + 2 * my


def text_width(text, size, bold=False):
    """Largeur (pouces) de la plus longue ligne d'un texte balisé, sans retour à la ligne automatique."""
    return max(sum(_length(word, size, b) for word, b in _words(line, bold)) for line in lines_of(text))


# Hauteur d'une ligne en interligne simple, en fraction de la taille de police : PowerPoint prend 1,2 em pour
# Outfit (étalonné sur un rendu PowerPoint, evals/etalonnage_texte.py).
LINE_HEIGHT = 1.2
