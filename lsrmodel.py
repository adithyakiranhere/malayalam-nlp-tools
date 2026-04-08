# lsrmodel.py -- public wrapper around lsr_core
#
# Loads the compiled .so if available, otherwise falls back to the pure
# python version. Keep this file + lsr_core*.so together and you're good.
#
# quick usage:
#   from lsrmodel import Model
#   m = Model()
#   m.analyse("ആനകൾ")

from typing import List, Dict

_CORE_SOURCE = None

try:
    import lsr_core
    _CORE_SOURCE = 'compiled'
except ImportError:
    # fallback for when the .so isn't built yet
    try:
        import lsr_core_pyfallback as lsr_core
        _CORE_SOURCE = 'python_fallback'
    except ImportError as e:
        raise ImportError(
            "Couldn't import lsr_core or lsr_core_pyfallback. "
            "Run build.sh first, or make sure the fallback files are "
            "next to this script."
        ) from e


class Model:
    """Malayalam lemma/stem/root analyser."""

    def __init__(self):
        self._core = lsr_core.LSRCore()
        self.backend = _CORE_SOURCE

    def analyse(self, word: str) -> List[Dict]:
        # ambiguous forms can return more than one result
        return self._core.analyse_malayalam(word)

    def analyse_wx(self, word: str) -> List[Dict]:
        return self._core.analyse_wx(word)

    def ml_to_wx(self, text: str) -> str:
        return self._core.ml_to_wx(text)

    def wx_to_ml(self, text: str) -> str:
        return self._core.wx_to_ml(text)

    def info(self) -> Dict:
        return self._core.info()


def _main():
    import argparse, json

    ap = argparse.ArgumentParser(description="Malayalam LSR analyser")
    ap.add_argument('words', nargs='*')
    ap.add_argument('--wx', action='store_true', help='input is WX, not Malayalam')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--info', action='store_true')
    args = ap.parse_args()

    model = Model()

    if args.info:
        print(json.dumps(model.info(), indent=2))
        return

    if not args.words:
        ap.print_help()
        return

    results = []
    for w in args.words:
        if args.wx:
            results.extend(model.analyse_wx(w))
        else:
            results.extend(model.analyse(w))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    for r in results:
        tags = '|'.join(r['tags'])
        print(
            f"{r['surface']}\tlemma={r['lemma']}\tstem={r['stem']}\t"
            f"root={r['root']}\tpos={r['pos']}\tparadigm={r['paradigm']}\t"
            f"tags={tags}\tsrc={r['source']}"
        )


if __name__ == '__main__':
    _main()
