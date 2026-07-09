# Validation against NASA RP-1311 Example 8

## Case definition

From the [CEA Python docs — Example 8](https://nasa.github.io/cea/examples/rocket/example8.html) and NASA RP-1311 [[1]](#references):

| Parameter | Value |
|-----------|--------|
| Mode | Rocket, infinite-area combustor (IAC) |
| Fuel | H2(L) @ 20.27 K |
| Oxidizer | O2(L) @ 90.17 K |
| O/F (mass) | 5.55157 |
| Pc | 53.3172 bar |
| Subsonic Ae/At | 1.58 |
| Supersonic Ae/At | 25, 50, 75 |
| Pressure ratios | 10, 100, 1000 |

**Note:** Older docs show `b"H2(L)"` byte strings; current `cea` 3.x accepts plain `str` species names (used by RocketCAE).

## Published performance checkpoints (excerpt)

| Station | T [K] | Isp [m/s] | Isp_vac [m/s] | Cf | c* [m/s] |
|---------|-------|-----------|---------------|-----|----------|
| Chamber | 3383.845 | — | — | — | 2332.34 |
| Ae/At = 1 | 3185.673 | 1537.917 | 2878.925 | 0.6594 | 2332.34 |
| Ae/At = 25 | 1468.163 | 4124.410 | 4348.510 | 1.7684 | 2332.34 |
| Ae/At = 50 | 1219.613 | 4309.122 | 4487.303 | 1.8476 | 2332.34 |
| Ae/At = 75 | 1088.640 | 4399.121 | 4554.913 | 1.8861 | 2332.34 |

## How RocketCAE checks

```bash
python -m rocketcae.cli validate
python examples/rp1311_example8.py
pytest tests/test_rp1311_example8.py -q
```

Implementation: `src/rocketcae/validation.py`.

Default pass criteria (per checkpoint): relative error ≤ **0.5%** **or** absolute tolerance (e.g. 5 m/s on Isp, 5 K on T). Modern CEA 3.x may differ slightly from the 1996 printed table while remaining an excellent engineering match.

## References

1. McBride, B.J., Gordon, S., NASA RP-1311, 1996. https://ntrs.nasa.gov/citations/19960044559  
2. https://nasa.github.io/cea/examples/rocket/example8.html  
