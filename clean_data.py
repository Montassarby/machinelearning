"""Étape 1 : audit + nettoyage des fichiers bruts -> fichiers CSV propres.

Usage : python clean_data.py --train train.csv --test test.csv --out data_clean
"""
import argparse, os, collections
from src.cleaning import clean_lines


def read(path):
    with open(path, encoding="utf-8-sig") as fh:      # échoue si l'encodage n'est pas UTF-8
        return fh.read().splitlines()


def audit(name, lines, has_label):
    heads = [l.split(",")[0 if has_label else 0] for l in lines]
    print(f"[{name}] lignes={len(lines)}  vides={sum(not l.strip() for l in lines)}  "
          f"doublons={len(lines) - len(set(lines))}")
    if has_label:
        c = collections.Counter(h for h in heads)
        print(f"[{name}] utilisateurs={len(c)}  min={min(c.values())}  max={max(c.values())}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True); ap.add_argument("--test", required=True)
    ap.add_argument("--out", default="data_clean")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for name, path, lab in [("train", a.train, True), ("test", a.test, False)]:
        raw = read(path)
        audit(name, raw, lab)
        clean, small, rep = clean_lines(raw, lab)
        out = os.path.join(a.out, f"{name}_clean.csv")
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(clean) + "\n")
        print(f"[{name}] corrections: {rep}  | lignes modifiées: {sum(x != y for x, y in zip(raw, clean))}")
        print(f"[{name}] sessions quasi vides (<4 actions): {sum(small)} -> indices {[i for i, s in enumerate(small) if s]}")
        print(f"[{name}] écrit : {out}\n")


if __name__ == "__main__":
    main()