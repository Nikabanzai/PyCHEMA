"""Validation cases against published NASA RP-1311 / CEA documentation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

# Published RP-1311 Example 8 reference (IAC, H2(L)/O2(L), of=5.55157, Pc=53.3172 bar)
# Source: NASA CEA docs — Example 8 from RP-1311
# https://nasa.github.io/cea/examples/rocket/example8.html
# McBride & Gordon, NASA RP-1311, 1996.

RP1311_EX8_INPUT = {
    "reac_names": ["H2(L)", "O2(L)"],
    "T_reactant": np.array([20.27, 90.17]),
    "fuel_weights": np.array([1.0, 0.0]),
    "oxidant_weights": np.array([0.0, 1.0]),
    "of_ratio": 5.55157,
    "pc_bar": 53.3172,
    "pi_p": [10.0, 100.0, 1000.0],
    "subar": [1.58],
    "supar": [25.0, 50.0, 75.0],
    "iac": True,
}

# Selected performance checkpoints from documented terminal output
RP1311_EX8_REFERENCE = {
    "chamber_T_K": 3383.845,
    "chamber_P_bar": 53.317,
    "cstar_m_s": 2332.34,
    # keyed by Ae/At
    "stations": {
        1.0: {"Isp_m_s": 1537.917, "Isp_vac_m_s": 2878.925, "Cf": 0.6594, "T_K": 3185.673},
        25.0: {"Isp_m_s": 4124.410, "Isp_vac_m_s": 4348.510, "Cf": 1.7684, "T_K": 1468.163},
        50.0: {"Isp_m_s": 4309.122, "Isp_vac_m_s": 4487.303, "Cf": 1.8476, "T_K": 1219.613},
        75.0: {"Isp_m_s": 4399.121, "Isp_vac_m_s": 4554.913, "Cf": 1.8861, "T_K": 1088.640},
    },
}


@dataclass
class CheckpointCompare:
    station: str
    quantity: str
    reference: float
    computed: float
    rel_error: float
    abs_error: float
    pass_: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "station": self.station,
            "quantity": self.quantity,
            "reference": self.reference,
            "computed": self.computed,
            "rel_error": self.rel_error,
            "abs_error": self.abs_error,
            "pass": self.pass_,
        }


def _require_cea():
    try:
        import cea
        return cea
    except ImportError as exc:
        raise ImportError("pip install cea is required for validation") from exc


def run_rp1311_example8():
    """Execute Example 8 with the modern CEA Python API (str species names)."""
    cea = _require_cea()
    cfg = RP1311_EX8_INPUT

    reac = cea.Mixture(cfg["reac_names"])
    prod = cea.Mixture(cfg["reac_names"], products_from_reactants=True)
    solver = cea.RocketSolver(prod, reactants=reac)
    solution = cea.RocketSolution(solver)

    weights = reac.of_ratio_to_weights(
        cfg["oxidant_weights"], cfg["fuel_weights"], cfg["of_ratio"]
    )
    hc = reac.calc_property(cea.ENTHALPY, weights, cfg["T_reactant"]) / cea.R
    solver.solve(
        solution,
        weights,
        cfg["pc_bar"],
        cfg["pi_p"],
        subar=cfg["subar"],
        supar=cfg["supar"],
        hc=hc,
        iac=cfg["iac"],
    )
    return solution


def _nearest_index(ae: np.ndarray, target: float) -> int:
    return int(np.argmin(np.abs(ae - target)))


def compare_rp1311_example8(
    rtol: float = 5e-3,
    atol_map: dict[str, float] | None = None,
) -> list[CheckpointCompare]:
    """Compare live CEA solution to published Example 8 checkpoints.

    Default relative tolerance 0.5% (modern CEA reimplementation may differ
    slightly from 1996 printout; still a strong validation gate).
    """
    atol_map = atol_map or {
        "T_K": 5.0,
        "Isp_m_s": 5.0,
        "Isp_vac_m_s": 5.0,
        "Cf": 0.005,
        "cstar_m_s": 2.0,
        "P_bar": 0.05,
    }

    sol = run_rp1311_example8()
    ae = np.asarray(sol.ae_at, dtype=float)
    Isp = np.asarray(sol.Isp, dtype=float)
    Isp_vac = np.asarray(sol.Isp_vacuum, dtype=float)
    Cf = np.asarray(sol.coefficient_of_thrust, dtype=float)
    T = np.asarray(sol.T, dtype=float)
    P = np.asarray(sol.P, dtype=float)
    cstar = np.asarray(sol.c_star, dtype=float)

    ref = RP1311_EX8_REFERENCE
    rows: list[CheckpointCompare] = []

    def add(station: str, quantity: str, reference: float, computed: float) -> None:
        abs_err = abs(computed - reference)
        rel = abs_err / max(abs(reference), 1e-30)
        atol = atol_map.get(quantity, 1.0)
        ok = rel <= rtol or abs_err <= atol
        rows.append(
            CheckpointCompare(station, quantity, reference, computed, rel, abs_err, ok)
        )

    add("chamber", "T_K", ref["chamber_T_K"], float(T[0]))
    add("chamber", "P_bar", ref["chamber_P_bar"], float(P[0]))
    add("throat", "cstar_m_s", ref["cstar_m_s"], float(cstar[_nearest_index(ae, 1.0)]))

    for eps, vals in ref["stations"].items():
        i = _nearest_index(ae, eps)
        st = f"Ae/At={eps:g}"
        add(st, "Isp_m_s", vals["Isp_m_s"], float(Isp[i]))
        add(st, "Isp_vac_m_s", vals["Isp_vac_m_s"], float(Isp_vac[i]))
        add(st, "Cf", vals["Cf"], float(Cf[i]))
        add(st, "T_K", vals["T_K"], float(T[i]))

    return rows


def validation_passed(rows: list[CheckpointCompare] | None = None) -> bool:
    rows = rows if rows is not None else compare_rp1311_example8()
    return all(r.pass_ for r in rows)


def format_validation_report(rows: list[CheckpointCompare] | None = None) -> str:
    rows = rows if rows is not None else compare_rp1311_example8()
    lines = [
        "RP-1311 Example 8 validation (H2(L)/O2(L), IAC)",
        f"{'station':<14} {'qty':<12} {'ref':>12} {'cea':>12} {'rel%':>10} {'ok':>4}",
        "-" * 68,
    ]
    for r in rows:
        lines.append(
            f"{r.station:<14} {r.quantity:<12} {r.reference:12.4f} {r.computed:12.4f} "
            f"{100 * r.rel_error:9.3f}% {'PASS' if r.pass_ else 'FAIL':>4}"
        )
    n_ok = sum(1 for r in rows if r.pass_)
    lines.append("-" * 68)
    lines.append(f"{n_ok}/{len(rows)} checkpoints passed")
    return "\n".join(lines)
