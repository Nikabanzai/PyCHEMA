"""
RocketCAE Streamlit GUI — preliminary liquid rocket trades via NASA CEA.

Run:
    streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running without install
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import streamlit as st

from rocketcae.cea_runner import run_rocket
from rocketcae.models import EngineInputs
from rocketcae.optimize import multi_objective_of_sweep, optimize_of, pareto_front_2d
from rocketcae.propellants import get_pair, list_propellant_pairs
from rocketcae.ranking import rank_propellant_pairs
from rocketcae.sweeps import sweep_of, sweep_to_dataframe

st.set_page_config(page_title="RocketCAE", page_icon="🚀", layout="wide")

st.title("RocketCAE")
st.caption(
    "Preliminary liquid rocket performance explorer using NASA CEA. "
    "Theoretical equilibrium results only — not flight hardware design."
)

with st.expander("Disclaimer", expanded=False):
    st.write(
        """
        Results come from chemical equilibrium thermodynamics (NASA CEA). They do **not**
        include turbomachinery, cooling, structures, combustion efficiency, or vehicle design.
        Use for conceptual trade studies only. Heritage: THK University CHEMA graduation project;
        modernized in Python with the official `cea` package (Apache-2.0).
        """
    )

pairs = list_propellant_pairs()
pair_labels = {p.label: p.key for p in pairs}

tab_run, tab_sweep, tab_opt, tab_rank, tab_pareto = st.tabs(
    ["Single run", "O/F sweep", "Optimize O/F", "Rank pairs", "Pareto (Isp–Tc)"]
)

with tab_run:
    c1, c2, c3 = st.columns(3)
    label = c1.selectbox("Propellant pair", list(pair_labels.keys()), index=1)
    pair = get_pair(pair_labels[label])
    of = c2.slider("O/F (mass)", float(pair.of_min), float(pair.of_max), float(pair.of_default), 0.01)
    pc = c3.number_input("Chamber pressure Pc [bar]", 1.0, 300.0, 50.0, 1.0)
    eps = st.number_input("Nozzle area ratio Ae/At", 2.0, 200.0, 40.0, 1.0)
    if st.button("Run CEA", type="primary"):
        with st.spinner("Solving equilibrium…"):
            r = run_rocket(
                EngineInputs(
                    fuel=pair.fuel.name,
                    oxidizer=pair.oxidizer.name,
                    of_ratio=of,
                    pc_bar=pc,
                    area_ratio=eps,
                    fuel_temp_k=pair.fuel.temp_k,
                    oxidizer_temp_k=pair.oxidizer.temp_k,
                )
            )
        if not r.success:
            st.error(r.message)
        else:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Isp", f"{r.isp_s:.1f} s")
            m2.metric("Isp vac", f"{r.isp_vac_s:.1f} s")
            m3.metric("c*", f"{r.cstar_m_s:.0f} m/s")
            m4.metric("Tc", f"{r.tc_k:.0f} K")
            st.json(r.to_dict())

with tab_sweep:
    label = st.selectbox("Pair (sweep)", list(pair_labels.keys()), index=1, key="sw_pair")
    pair = get_pair(pair_labels[label])
    c1, c2, c3 = st.columns(3)
    pc = c1.number_input("Pc [bar]", 1.0, 300.0, 50.0, key="sw_pc")
    eps = c2.number_input("Ae/At", 2.0, 200.0, 40.0, key="sw_eps")
    n = c3.slider("Points", 5, 41, 21)
    if st.button("Run sweep"):
        base = EngineInputs(
            fuel=pair.fuel.name,
            oxidizer=pair.oxidizer.name,
            of_ratio=pair.of_default,
            pc_bar=pc,
            area_ratio=eps,
            fuel_temp_k=pair.fuel.temp_k,
            oxidizer_temp_k=pair.oxidizer.temp_k,
        )
        with st.spinner("Sweeping O/F…"):
            sweep = sweep_of(base, pair.of_min, pair.of_max, n=n)
            df = sweep_to_dataframe(sweep)
        st.dataframe(df, use_container_width=True)
        ok = df[df["success"]]
        if not ok.empty:
            st.line_chart(ok.set_index("of_ratio")[["isp_s", "isp_vac_s"]])
            st.line_chart(ok.set_index("of_ratio")[["tc_k"]])

with tab_opt:
    label = st.selectbox("Pair (optimize)", list(pair_labels.keys()), index=1, key="opt_pair")
    pair = get_pair(pair_labels[label])
    c1, c2 = st.columns(2)
    pc = c1.number_input("Pc [bar]", 1.0, 300.0, 50.0, key="opt_pc")
    eps = c2.number_input("Ae/At", 2.0, 200.0, 40.0, key="opt_eps")
    objective = st.selectbox("Objective", ["isp", "isp_vac", "cstar", "density_isp"])
    if st.button("Optimize O/F"):
        base = EngineInputs(
            fuel=pair.fuel.name,
            oxidizer=pair.oxidizer.name,
            of_ratio=pair.of_default,
            pc_bar=pc,
            area_ratio=eps,
            fuel_temp_k=pair.fuel.temp_k,
            oxidizer_temp_k=pair.oxidizer.temp_k,
        )
        with st.spinner("Optimizing…"):
            res = optimize_of(base, pair.of_min, pair.of_max, objective=objective)
        if not res.success:
            st.error(res.message)
        else:
            st.success(f"Best {res.objective} = {res.best_value:.4g} at O/F = {res.best_inputs.of_ratio:.4f}")
            st.json(res.best_result.to_dict())

with tab_rank:
    c1, c2 = st.columns(2)
    pc = c1.number_input("Pc [bar]", 1.0, 300.0, 50.0, key="rk_pc")
    eps = c2.number_input("Ae/At", 2.0, 200.0, 40.0, key="rk_eps")
    if st.button("Rank all pairs"):
        with st.spinner("Ranking…"):
            df = rank_propellant_pairs(pc_bar=pc, area_ratio=eps)
        st.dataframe(df, use_container_width=True)

with tab_pareto:
    label = st.selectbox("Pair (pareto)", list(pair_labels.keys()), index=1, key="pa_pair")
    pair = get_pair(pair_labels[label])
    c1, c2, c3 = st.columns(3)
    pc = c1.number_input("Pc [bar]", 1.0, 300.0, 50.0, key="pa_pc")
    eps = c2.number_input("Ae/At", 2.0, 200.0, 40.0, key="pa_eps")
    n = c3.slider("Points", 10, 41, 21, key="pa_n")
    if st.button("Compute Pareto"):
        base = EngineInputs(
            fuel=pair.fuel.name,
            oxidizer=pair.oxidizer.name,
            of_ratio=pair.of_default,
            pc_bar=pc,
            area_ratio=eps,
            fuel_temp_k=pair.fuel.temp_k,
            oxidizer_temp_k=pair.oxidizer.temp_k,
        )
        with st.spinner("Multi-objective sweep…"):
            pts = multi_objective_of_sweep(base, pair.of_min, pair.of_max, n=n)
            points = [(o1, -o2, r) for _, o1, o2, r in pts]
            front = pareto_front_2d(points, maximize=(True, False))
        if not pts:
            st.warning("No successful points.")
        else:
            all_df = pd.DataFrame(
                {
                    "of_ratio": [r.inputs.of_ratio for *_, r in pts],
                    "isp_s": [o1 for _, o1, _, _ in pts],
                    "tc_k": [-o2 for _, _, o2, _ in pts],
                }
            )
            front_df = pd.DataFrame(
                {
                    "of_ratio": [r.inputs.of_ratio for _, _, r in front],
                    "isp_s": [a for a, _, _ in front],
                    "tc_k": [b for _, b, _ in front],
                }
            )
            st.subheader("All sweep points")
            st.scatter_chart(all_df, x="tc_k", y="isp_s")
            st.subheader("Pareto front (max Isp, min Tc)")
            st.dataframe(front_df, use_container_width=True)

st.divider()
st.markdown(
    "CEA: [nasa/cea](https://github.com/nasa/cea) · Docs: [nasa.github.io/cea](https://nasa.github.io/cea/) · "
    "RocketCAE: Python modernization of the CHEMA thesis concept."
)
