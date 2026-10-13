import argparse
import os
from collections import Counter

from sklearn.model_selection import train_test_split


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True)
    ap.add_argument("--out", default="data_split")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()

    with open(a.train, encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()
    y = [l.split(",")[0] for l in lines]          # étiquette = trigramme (1er champ)

    # stratify=y : chaque utilisateur est réparti 80/20 entre entraînement et validation
    l_tr, l_va, y_tr, y_va = train_test_split(
        lines, y, test_size=0.2, stratify=y, random_state=a.seed)

    c_tr, c_va = Counter(y_tr), Counter(y_va)
    print(f"entraînement : {len(l_tr)} sessions ({len(l_tr)/len(lines):.1%}), {len(c_tr)} utilisateurs")
    print(f"validation   : {len(l_va)} sessions ({len(l_va)/len(lines):.1%}), {len(c_va)} utilisateurs")
    print("utilisateurs absents de la validation :", len(set(y) - set(c_va)))
    print("utilisateurs absents de l'entraînement :", len(set(y) - set(c_tr)))
    print("sessions par utilisateur en validation : min", min(c_va.values()), "max", max(c_va.values()))

    os.makedirs(a.out, exist_ok=True)
    for name, data in [("train_80.csv", l_tr), ("val_20.csv", l_va)]:
        with open(os.path.join(a.out, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(data) + "\n")
    print("fichiers écrits dans", a.out)


if __name__ == "__main__":
    main()