# RocketCAE

**Preliminary liquid rocket engine trade studies** using [NASA CEA](https://github.com/nasa/cea) from Python — with a CLI and a simple Streamlit GUI.

RocketCAE is a cleaner, modern take on the **CHEMA** graduation project concept (University of Turkish Aeronautical Association): drive CEA over a design space, optimize a few objectives, and present results without claiming flight-ready “novel rockets.”

> Theoretical chemical-equilibrium performance only. Not a substitute for cycle analysis, cooling, structures, or test.

## Features

| Capability | How |
|------------|-----|
| Single bipropellant evaluation | `rocketcae run` |
| O/F, Pc, Ae/At sweeps | `rocketcae sweep` |
| Maximize Isp (or c*, density-Isp) | `rocketcae optimize` |
| Rank curated propellant pairs | `rocketcae rank` |
| Pareto (max Isp, min Tc) | `rocketcae pareto` |
| GUI | `streamlit run app/streamlit_app.py` |

Depends on the official package: `pip install cea` ([docs](https://nasa.github.io/cea/)).

## Requirements

- Python **3.11+**
- Fortran is **not** required if you install the published `cea` wheel

## Install

```bash
cd RocketCAE
python -m venv .venv

# Windows
.venv\Scripts\activate

python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Quick start

```bash
# List curated fuels
rocketcae list-pairs

# LOX/LH2 (RP-1311 style)
rocketcae run --pair lox_lh2 --of 5.55 --pc 53.3 --eps 25

# LOX/RP-1 (CHEMA heritage)
rocketcae run --pair lox_rp1 --of 2.3 --pc 66.5 --eps 16

# Sweep O/F → CSV in results/
rocketcae sweep --pair lox_ch4 --param of --n 21

# Optimize O/F for max Isp
rocketcae optimize --pair lox_lh2 --vars of --objective isp

# Rank all pairs at fixed Pc / ε
rocketcae rank --pc 50 --eps 40

# GUI
streamlit run app/streamlit_app.py
```

Examples:

```bash
python examples/run_lox_lh2.py
python examples/sweep_lox_rp1.py
```

## Curated propellant pairs

| Key | Pair |
|-----|------|
| `lox_lh2` | LOX / LH2 |
| `lox_rp1` | LOX / RP-1 |
| `lox_ch4` | LOX / LCH4 |
| `lox_ethanol` | LOX / Ethanol |
| `nto_mmh` | NTO / MMH |
| `nto_hydrazine` | NTO / Hydrazine |

Species names follow the NASA CEA database. You can also pass arbitrary CEA names via `--fuel` / `--oxidizer`.

## Project layout

```text
RocketCAE/
  src/rocketcae/     # library: models, CEA runner, sweeps, optimize, ranking, CLI
  app/               # Streamlit GUI
  tests/
  examples/
  docs/heritage.md   # CHEMA thesis mapping
  results/           # generated CSVs (gitignored content)
  Chema/             # LOCAL ONLY — original MATLAB dump (gitignored)
```

## Legacy CHEMA folder

If you have the old MATLAB project under `Chema/`, keep it on disk for reference.
It is **listed in `.gitignore`** (binaries, media, CAD, personal files). See [docs/heritage.md](docs/heritage.md).

## Tests

```bash
pytest -q
```

## Acknowledgements

- **NASA CEA** — Chemical Equilibrium with Applications ([Apache-2.0](https://github.com/nasa/cea))
- **CHEMA** — THK University graduation project (Kul, Seymen, Yıldız, Köroğlu)

## License

Application code is provided under **Apache-2.0** for alignment with NASA CEA.
CEA remains subject to its own license and NOTICE files.
