# Malayalam LSR Analyser

A fast Lemma / Stem / Root analyser for Malayalam, built on a
paradigm-dictionary approach. Input Malayalam words in script; get
lemma, stem, root, POS, paradigm, and morphological tags.

## Requirements

- **Linux x86_64** (the shipped `.so` is built for this platform)
- **Python 3.10** (the `.so` is ABI-locked to this version)
- No pip installs. No data files. No configuration.

If you're on a different OS, Python version, or CPU architecture, you
will need to rebuild from source.

## Install

```bash
git clone <this-repo>
cd malayalam-nlp-tools
python3 inference.py
```

That's it. The model is self-contained in `lsr_core*.so`.

## Usage

### Python API

```python
from lsrmodel import Model

model = Model()                    # loads once (~0.3s)

for r in model.analyse("ആനകൾ"):
    print(r['lemma'])              # ആന
    print(r['root'])               # ആന
    print(r['pos'])                # N
    print(r['paradigm'])           # N_1
    print(r['tags'])               # ['PL']
```

Each analysis is a dict with these keys:

| Key | Description |
|---|---|
| `surface` | Input word (Malayalam script) |
| `surface_wx` | Input word in WX notation (internal) |
| `lemma` / `lemma_wx` | Lemma in Malayalam / WX |
| `stem` / `stem_wx` | Stem in Malayalam / WX |
| `root` / `root_wx` | Root in Malayalam / WX |
| `pos` | Part of speech (N, V, adj, adv, PN, UNK) |
| `paradigm` | Paradigm ID (e.g. `N_1`, `V_2`) |
| `tags` | Morphological tags (`['PL']`, `['PRES']`, `['ACC']`, etc.) |
| `source` | How the analysis was found: `dict_direct`, `rules_exemplar`, `rules_generated`, or `unknown` |

A single word may return multiple analyses if ambiguous.

### WX input (if you already have WX)

```python
model.analyse_wx("AnakalYZ")
```

### Script conversion only

```python
model.ml_to_wx("ആന")    # 'Ana'
model.wx_to_ml("Ana")   # 'ആന'
```

### Command-line

```bash
python3 lsrmodel.py ആന ആനകൾ മരങ്ങൾ
python3 lsrmodel.py --wx AnakalYZ alYakkunnu
python3 lsrmodel.py --json ആന
python3 lsrmodel.py --info
```

## Examples

| Input | Lemma | Root | POS | Paradigm | Tags |
|---|---|---|---|---|---|
| ആന | ആന | ആന | N | N_1 | BASE |
| ആനകൾ | ആന | ആന | N | N_1 | PL |
| മരം | മരം | മര | N | N_9 | BASE |
| മരങ്ങൾ | മരം | മര | N | N_9 | PL |

## Performance

- ~20,000–40,000 Malayalam analyses/second on a modern CPU
- Load time: ~0.3 seconds (one-time)
- Memory: ~150 MB resident

## Model stats

- 141,545 dictionary entries
- 71 paradigms (42 with full rule coverage)
- 27,520 unique inflected surface forms learned
- Covers N, V, adj, adv, PN
