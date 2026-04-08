"""
inference.py
============
Minimal example of how to use the Malayalam LSR model.

Requirements: Python 3.10 on Linux x86_64 (matches the shipped .so).
No pip installs needed.

Run:
    python3 inference.py
    python3 inference.py ആന ആനകൾ മരങ്ങൾ
"""
import sys
from lsrmodel import Model

# Load once (takes ~0.3 seconds; reuse the same `model` for every query).
model = Model()


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
    words = sys.argv[1:] or ['ആന', 'ആനകൾ', 'മരം', 'മരങ്ങൾ']
    print(f"Model info: {model.info()}")
    for w in words:
        show(w)
