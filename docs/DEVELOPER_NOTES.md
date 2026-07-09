# Developer notes — pause / resume

Snapshot of project state as of **2026-07-09** (PyCHEMA **v0.2.0**).  
Public resting point after rebrand, Zenodo DOI, and core feature set.

## Status: good place to pause

Work through v0.2.0 is enough for people to find, install, cite, and use PyCHEMA.
No urgent feature work required before the next development wave.

| Item | Value |
|------|--------|
| Repository | https://github.com/Nikabanzai/PyCHEMA |
| Package / CLI | `pychema` |
| Version | 0.2.0 |
| Zenodo DOI | [10.5281/zenodo.21278092](https://doi.org/10.5281/zenodo.21278092) |
| CHEMA 2017 DOI | [10.13140/RG.2.2.31672.55043](https://doi.org/10.13140/RG.2.2.31672.55043) |
| Thermochemistry | Official NASA **`cea`** (not PyPI **RocketCEA**) |
| License (app) | Apache-2.0 |

Local working copy may still live under a path named `RocketCAE`; the project identity is **PyCHEMA**.

---

## When you come back — quick start

```bash
# Clone (new machine) or pull (existing clone)
git clone https://github.com/Nikabanzai/PyCHEMA.git
cd PyCHEMA
# — or —
git pull origin master

python -m pip install -e ".[dev]"
python -m pychema.cli validate --case full
```

Optional:

```bash
python -m streamlit run app/streamlit_app.py
python -m pychema.cli design --pair lox_rp1 --thrust 50000 --pc 50 --eps 25
python -m pytest -q
```

---

## Ideas backlog (not urgent)

Parked for a future session; none block v0.2.0:

1. **Multi-fuel UI** — 2–3 fuel/oxidizer species mixes (CHEMA had multi-slot reactants)
2. **FAC Ex.9 numerical validation** — finite-area combustor checkpoints vs RP-1311 Example 9 (beyond smoke)
3. **Frozen path** — equilibrium vs frozen nozzle / `nfz` style options (CHEMA + Ex.12)
4. **Dashboard PNG** — matplotlib multi-panel engine dashboard export (cmflannery/rocket-style)

Other low-priority notes (see also `docs/chema_gap_analysis.md`, `docs/related_work.md`):

- Stronger multi-objective / thrust maximization campaigns  
- Optional cycle bookkeeping (GG/SC) — only if needed  
- Keep scope educational/preliminary; no trajectory/targeting features  

---

## Related docs

| Doc | Purpose |
|-----|---------|
| [ANNOUNCEMENTS.md](ANNOUNCEMENTS.md) | Zenodo / ResearchGate / LinkedIn / email copy |
| [ZENODO_UPLOAD.md](ZENODO_UPLOAD.md) | How the DOI archive was finished |
| [heritage.md](heritage.md) | CHEMA 2017 → PyCHEMA |
| [chema_gap_analysis.md](chema_gap_analysis.md) | What CHEMA had vs what we restored |
| [engineering_helpers.md](engineering_helpers.md) | Mission sizing / design brief |
| [validation.md](validation.md) / [rp1311_samples.md](rp1311_samples.md) | CEA validation |

---

## Naming reminder

| Name | Meaning |
|------|---------|
| **PyCHEMA** | This project |
| **CHEMA** | 2017 graduation project / paper |
| **cea** | NASA official Python package |
| **RocketCEA** | Unrelated PyPI FORTRAN wrapper — do not confuse |
| **RocketCAE** | Former working title of PyCHEMA only |
