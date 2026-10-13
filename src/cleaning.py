import re
from collections import Counter

# marqueur de temps collé à une action (virgule manquante), ex. "...Controller)t5"
# les vrais marqueurs sont des multiples de 5 ; le suffixe "1" (en modification) n'en est pas un
RE_GLUED_TIME = re.compile(r"^(.{4,}?)(t(?:[1-9]\d*)?[05])$")
RE_PURE_TIME = re.compile(r"^t\d+$")
MIN_ACTIONS = 4  # en dessous, la session est marquée "quasi vide"


def _fix_token(tok, stats):
    """Corrige un jeton ; renvoie une liste (1 ou 2 jetons)."""
    tok = tok.replace("\u2019", "'").strip()   # apostrophe typographique -> droite
    if not RE_PURE_TIME.match(tok):
        m = RE_GLUED_TIME.match(tok)
        if m and not m.group(1)[-1].isdigit():
            stats["temps_colle"] += 1
            return [m.group(1), m.group(2)]
    return [tok]


def clean_line(line, has_label, stats=None):
    """Nettoie une ligne brute. Renvoie (ligne_propre, session_quasi_vide)."""
    stats = stats if stats is not None else Counter()
    raw = line.split(",")
    head_n = 2 if has_label else 1          # util (si présent) + navigateur
    head = [h.strip() for h in raw[:head_n]]
    out = []
    for tok in raw[head_n:]:
        if not tok.strip():
            stats["jeton_vide"] += 1
            continue
        out.extend(_fix_token(tok, stats))
    n_actions = sum(1 for t in out if not RE_PURE_TIME.match(t))
    if n_actions < MIN_ACTIONS:
        stats["session_quasi_vide"] += 1
    stats["apostrophes_norm"] += line.count("\u2019")
    return ",".join(head + out), n_actions < MIN_ACTIONS


def clean_lines(lines, has_label):
    """Nettoie toutes les lignes. Renvoie (lignes_propres, flags_quasi_vide, rapport)."""
    stats = Counter()
    res = [clean_line(l, has_label, stats) for l in lines]
    return [r[0] for r in res], [r[1] for r in res], dict(stats)