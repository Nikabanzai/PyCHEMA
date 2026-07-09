# Changelog

## [0.1.0] — 2026-07-09

### Added
- Python package `rocketcae` wrapping NASA `cea` RocketSolver for bipropellant IAC cases
- Curated propellant pairs (LOX/LH2, LOX/RP-1, LOX/CH4, LOX/ethanol, NTO/MMH, NTO/hydrazine)
- CLI: `run`, `sweep`, `optimize`, `rank`, `pareto`, `list-pairs`, `validate`
- O/F and multi-variable optimization (scipy)
- Multi-objective Pareto filter (Isp vs Tc)
- Streamlit GUI (`app/streamlit_app.py`)
- **RP-1311 Example 8** validation against published NASA CEA documentation
- Heritage documentation linking to the 2017 CHEMA graduation project concept
- Apache-2.0 license, CITATION.cff, CONTRIBUTING

### Notes
- Conceptual successor to CHEMA (THK University, 2017); new independent codebase
- Original MATLAB CHEMA sources/media are not included in this repository
