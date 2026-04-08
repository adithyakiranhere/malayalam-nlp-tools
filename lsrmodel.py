"""
lsrmodel.py
===========
Thin public wrapper around the compiled lsr_core extension.

This is the ONLY Python file your end users need to see, together with
the compiled lsr_core*.so. It exposes a clean, documented API.

USAGE
-----
    from lsrmodel import Model

    model = Model()                      # one-time load (~0.5 s)

    # Analyse Malayalam input (user-facing):
    for r in model.analyse("ആനകൾ"):
        print(r)

    # Output shape:
    # {
    #   'surface':     'ആനകൾ',          # the Malayalam you passed in
    #   'surface_wx':  'AnakalYZ',       # WX form used internally
    #   'lemma':       'ആന',
    #   'lemma_wx':    'Ana',
    #   'stem':        'ആന',
    #   'stem_wx':     'Ana',
    #   'root':        'ആന',
    #   'root_wx':     'Ana',
    #   'pos':         'N',
    #   'paradigm':    'N_1',
    #   'tags':        ['PL'],
    #   'source':      'rules_exemplar'
    # }

    # Raw WX analysis (if you already have WX input):
    model.analyse_wx("AnakalYZ")

    # Script conversion helpers:
    model.ml_to_wx("ആന")                 # -> 'Ana'
    model.wx_to_ml("Ana")                # -> 'ആന'

    # Model metadata:
    model.info()
    # {'dictionary_entries': 141545, 'paradigms': 71,
    #  'paradigms_with_rules': 42, 'surface_forms': 27520}
"""
from typing import List, Dict

try:
    import lsr_core
    _CORE_SOURCE = 'compiled'
except ImportError:
    try:
        import lsr_core_pyfallback as lsr_core
        _CORE_SOURCE = 'python_fallback'
    except ImportError as e:
        raise ImportError(
            "Neither compiled lsr_core nor lsr_core_pyfallback could be "
            "imported. Run build.sh to produce the .so, or keep "
            "lsr_core_pyfallback.py + _frozen_data.bin alongside this file."
        ) from e


class Model:
    """Malayalam Lemma/Stem/Root analyser."""

    def __init__(self):
        self._core = lsr_core.LSRCore()
        self.backend = _CORE_SOURCE   # 'compiled' or 'python_fallback'

    # ---- analysis ----
    def analyse(self, word: str) -> List[Dict]:
        """Analyse a Malayalam-script word. Returns a list of analyses
        (ambiguous forms may yield more than one)."""
        return self._core.analyse_malayalam(word)

    def analyse_wx(self, word: str) -> List[Dict]:
        """Analyse a WX-notation word directly (skip the ML→WX step)."""
        return self._core.analyse_wx(word)

    # ---- script conversion ----
    def ml_to_wx(self, text: str) -> str:
        return self._core.ml_to_wx(text)

    def wx_to_ml(self, text: str) -> str:
        return self._core.wx_to_ml(text)

    # ---- metadata ----
    def info(self) -> Dict:
        return self._core.info()


# ------------------------------------------------------------------ CLI
def _main():
    import argparse, json, sys
    ap = argparse.ArgumentParser(description="Malayalam LSR analyser")
    ap.add_argument('words', nargs='*', help='Malayalam words to analyse')
    ap.add_argument('--wx', action='store_true',
                    help='Treat input as WX instead of Malayalam')
    ap.add_argument('--json', action='store_true', help='Output JSON')
    ap.add_argument('--info', action='store_true', help='Show model info')
    args = ap.parse_args()

    model = Model()
    if args.info:
        print(json.dumps(model.info(), indent=2))
        return
    if not args.words:
        ap.print_help()
        return

    out = []
    for w in args.words:
        rs = model.analyse_wx(w) if args.wx else model.analyse(w)
        out.extend(rs)

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for r in out:
            tags = '|'.join(r['tags'])
            print(f"{r['surface']}\tlemma={r['lemma']}\tstem={r['stem']}\t"
                  f"root={r['root']}\tpos={r['pos']}\tparadigm={r['paradigm']}\t"
                  f"tags={tags}\tsrc={r['source']}")


if __name__ == '__main__':
    _main()
