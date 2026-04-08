# small script to try out the LSR model
# usage: python3 inference.py [words...]

import sys
from lsrmodel import Model

model = Model()  # load once, reuse


def show(word):
    print(f"\nInput: {word}")
    results = model.analyse(word)

    if not results:
        print("  (no analysis)")
        return

    for i, r in enumerate(results, 1):
        print(f"  [{i}] lemma={r['lemma']}  stem={r['stem']}  root={r['root']}")
        print(f"      pos={r['pos']}  paradigm={r['paradigm']}  tags={r['tags']}")
        print(f"      source={r['source']}")


if __name__ == '__main__':
    words = sys.argv[1:]
    if not words:
        words = ['ആന', 'ആനകൾ', 'മരം', 'മരങ്ങൾ']

    print("Model info:", model.info())
    for w in words:
        show(w)
