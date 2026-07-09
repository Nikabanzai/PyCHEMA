# Heritage: CHEMA (2017) → RocketCAE (2026)

## Open-source positioning

RocketCAE is published as a **public educational/engineering tool**: a **conceptual continuation** of the CHEMA graduation project idea, implemented as a **new Python codebase**. It is **not** a release of the original MATLAB sources.

Please credit:

1. **NASA CEA** for the equilibrium solver  
2. **CHEMA authors and advisors** for the 2017 project concept  
3. **RocketCAE** for the modern packaging, validation harness, and UI  

## CHEMA (2017)

**Title:** Preliminary Design, Basic Simulation and Optimization of Liquid Rocket Engines  

**Students:** Muhammed Ali Kul, Yağız Seymen, Melih Emre Yıldız, Süleyman Murat Köroğlu  

**University:** University of Turkish Aeronautical Association (THK)  

**Advisors:** Assist. Prof. Sudantha Balage, Assist. Prof. Durmuş Sinan Körpe  

**Stack:** MATLAB GUIDE GUI (`ChemaV7`) calling legacy CEA (e.g. CEA300.exe), sample RP-1/LOX inputs, optimization hooks, plots.

### Sample legacy input (conceptual)

```text
problem  rkt fac equilibrium shock
case=1 p,psia=965 ... o/f=2.57776544 sup-ae/at=16 ...
reactants
fuel =RP-1 wt=100.
oxid =O2(L) wt=100.
```

Mapped in RocketCAE to curated pair **`lox_rp1`**.

## What is not in this repository

The local `Chema/` folder (if present on a developer machine) may contain the original dump: MATLAB, CAD, media, binaries, personal files. It is **gitignored** and must not be committed.

## Mapping

| CHEMA | RocketCAE |
|-------|-----------|
| MATLAB + CEA300.exe | Python + `pip install cea` |
| GUIDE GUI | Streamlit |
| Manual `.inp` | `EngineInputs` + CLI |
| Optimization tab | `optimize` / Pareto |
| Limited validation story | RP-1311 Example 8 automated checks |

## Disclaimer

Theoretical results may differ immensely from reality. No liability for hardware decisions based on these tools.
