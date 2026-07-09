# Heritage: CHEMA (THK graduation project)

RocketCAE is a **modern Python re-implementation of the concept** behind **CHEMA**
(University of Turkish Aeronautical Association graduation project):

> *Preliminary Design, Basic Simulation and Optimization of Liquid Rocket Engines*
> Muhammed Ali Kul, Yağız Seymen, Melih Emre Yıldız, Süleyman Murat Köroğlu
> Advisors: Assist. Prof. Sudantha Balage, Assist. Prof. Durmuş Sinan Körpe

## What CHEMA was

- MATLAB GUI (`ChemaV7.m` / GUIDE) calling legacy **CEA300.exe**
- Sample input (RP-1 / LOX), optimization hooks, plots, CAD-related exports
- Goal: explore many LRE design points and optimize under specifications

## What lives on disk vs Git

The local folder `Chema/` (if present) is the original project dump: MATLAB sources,
media, CAD, WAV help audio, binaries, CVs, etc. (~tens of MB).

It is **gitignored** so the public RocketCAE repo stays lean. Keep `Chema/` on your
machine for reference; do not commit binaries or personal media.

Useful reference snippets from the original workflow:

```text
problem  rkt fac equilibrium shock
case=1 p,psia=965 pc/p=1 o/f=2.57776544 sup-ae/at=16 ...
reactants
fuel =RP-1 wt=100.
oxid =O2(L) wt=100.
```

RocketCAE maps this to the curated pair `lox_rp1` and the Python `cea` API.

## Mapping CHEMA → RocketCAE

| CHEMA | RocketCAE |
|-------|-----------|
| MATLAB + CEA300.exe | Python + `pip install cea` (NASA) |
| GUIDE GUI | Streamlit GUI |
| Manual `.inp` | `EngineInputs` + CLI |
| Optimization tab | `optimize` / Pareto modules |
| “Novel designs” marketing | Explicitly **thermo trades only** |

## Disclaimer (same spirit as CHEMA)

Theoretical results may differ immensely from reality. No liability for use of
outputs for hardware decisions.
