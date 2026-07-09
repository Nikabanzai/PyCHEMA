# RocketCAE

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CEA](https://img.shields.io/badge/engine-NASA%20CEA-informational)](https://github.com/nasa/cea)

**Preliminary liquid rocket engine trade studies** using [NASA CEA](https://github.com/nasa/cea) — Python library, CLI, and Streamlit GUI.

> **Not flight hardware design.** Outputs are theoretical chemical-equilibrium performance only (Isp, c\*, Tc, …). They do **not** include turbopumps, cooling, structures, injectors, or vehicle Δv.

## Heritage (CHEMA → RocketCAE)

RocketCAE is a **modern Python continuation of the CHEMA *concept*** from a 2017 graduation project at the University of Turkish Aeronautical Association:

> *Preliminary Design, Basic Simulation and Optimization of Liquid Rocket Engines*  
> M. A. Kul, Y. Seymen, M. E. Yıldız, S. M. Köroğlu  
> Advisors: Assist. Prof. S. Balage, Assist. Prof. D. S. Körpe

CHEMA used MATLAB + legacy CEA executables. **RocketCAE is a new codebase** (not a port of the MATLAB GUI) that keeps the same educational goal — explore many bipropellant design points and lightly optimize — on top of the official modern [`cea`](https://github.com/nasa/cea) package.

Original MATLAB dumps, media, and binaries are **not** published here (local-only / gitignored). See [docs/heritage.md](docs/heritage.md).

## Features

| Capability | Command / entry |
|------------|-----------------|
| Single bipropellant evaluation | `rocketcae run` |
| O/F, Pc, Ae/At sweeps | `rocketcae sweep` |
| Maximize Isp / c\* / density-Isp | `rocketcae optimize` |
| Rank curated propellant pairs | `rocketcae rank` |
| Pareto (max Isp, min Tc) | `rocketcae pareto` |
| **RP-1311 Examples 8 & 13 validation** | `rocketcae validate` |
| GUI | `streamlit run app/streamlit_app.py` |

## Validation (NASA RP-1311 Examples 8 & 13)

RocketCAE checks live CEA results against published NASA cases:

| Case | Focus |
|------|--------|
| **Example 8** | H₂(L)/O₂(L) IAC rocket performance |
| **Example 13** | N₂H₄+Be / H₂O₂ with `insert=BeO(L)` and condensed products |

```bash
python -m rocketcae.cli validate              # both
python -m rocketcae.cli validate --case ex13
python examples/rp1311_example8.py
python examples/rp1311_example13.py
pytest tests/test_rp1311_example8.py -q
```

Details: [docs/validation.md](docs/validation.md).

## Requirements

- Python **3.11+**
- `pip install cea` (Fortran **not** required for the published wheel)

## Install

```bash
git clone https://github.com/Nikabanzai/RocketCAE.git
cd RocketCAE
python -m venv .venv

# Windows
.venv\Scripts\activate

python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Quick start

```bash
rocketcae list-pairs

# LOX/LH2 near Example 8 conditions
rocketcae run --pair lox_lh2 --of 5.55 --pc 53.3 --eps 25

# LOX/RP-1 (CHEMA-style sample)
rocketcae run --pair lox_rp1 --of 2.3 --pc 66.5 --eps 16

rocketcae sweep --pair lox_ch4 --param of --n 21
rocketcae optimize --pair lox_lh2 --vars of --objective isp
rocketcae rank --pc 50 --eps 40
rocketcae validate

streamlit run app/streamlit_app.py
```

If console scripts are not on `PATH`:

```bash
python -m rocketcae.cli validate
```

## Curated propellant pairs

| Key | Pair |
|-----|------|
| `lox_lh2` | LOX / LH2 |
| `lox_rp1` | LOX / RP-1 |
| `lox_ch4` | LOX / LCH4 |
| `lox_ethanol` | LOX / Ethanol |
| `nto_mmh` | NTO / MMH (`CH6N2(L)` in CEA) |
| `nto_hydrazine` | NTO / Hydrazine |

Arbitrary CEA species: `--fuel` / `--oxidizer`.

## Project layout

```text
RocketCAE/
  src/rocketcae/     # library + CLI + validation
  app/               # Streamlit GUI
  tests/
  examples/          # including rp1311_example8.py
  docs/              # heritage, validation
  results/           # generated CSVs (content gitignored)
```

## Citing

If you use RocketCAE, please cite NASA CEA / RP-1311 for the thermodynamics engine, and optionally this software (see [CITATION.cff](CITATION.cff)).

```bibtex
@software{RocketCAE2026,
  author = {Kul, Muhammed Ali},
  title  = {RocketCAE: Preliminary liquid rocket trades via NASA CEA},
  year   = {2026},
  url    = {https://github.com/Nikabanzai/RocketCAE},
  note   = {Conceptual successor to the 2017 CHEMA graduation project (THK University)}
}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs welcome for propellant data, validation cases, and docs.

## Acknowledgements

- **NASA CEA** — Chemical Equilibrium with Applications ([Apache-2.0](https://github.com/nasa/cea))
- **CHEMA (2017)** — Kul, Seymen, Yıldız, Köroğlu; THK University; advisors Balage & Körpe  
  *Concept predecessor only; RocketCAE is independently implemented.*

## Disclaimer

Same spirit as CHEMA: theoretical results may differ greatly from reality. No liability for decisions based on these outputs.

## License

Application code: **Apache-2.0** (see [LICENSE](LICENSE)).  
CEA is a separate dependency with its own license and NOTICE.

## References

1. McBride, B.J., Gordon, S., *Computer Program for Calculation of Complex Chemical Equilibrium Compositions and Applications II. Users Manual and Program Description*, NASA RP-1311, 1996. [NTRS 19960044559](https://ntrs.nasa.gov/citations/19960044559)  
2. NASA CEA documentation — [Example 8 (RP-1311)](https://nasa.github.io/cea/examples/rocket/example8.html)  
3. [nasa/cea](https://github.com/nasa/cea) on GitHub  

