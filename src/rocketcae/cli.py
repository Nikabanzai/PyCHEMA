"""Command-line interface for RocketCAE."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rocketcae.cea_runner import run_from_pair, run_rocket
from rocketcae.models import EngineInputs
from rocketcae.optimize import multi_objective_of_sweep, optimize_of, optimize_of_pc, pareto_front_2d
from rocketcae.propellants import get_pair, list_propellant_pairs
from rocketcae.ranking import rank_propellant_pairs
from rocketcae.sweeps import sweep_area_ratio, sweep_of, sweep_pc, sweep_to_dataframe


def _print_result(r) -> None:
    if not r.success:
        print(f"FAILED: {r.message}", file=sys.stderr)
        return
    print(f"Fuel/Ox     : {r.inputs.fuel} / {r.inputs.oxidizer}")
    print(f"O/F         : {r.inputs.of_ratio:.4f}")
    print(f"Pc          : {r.pc_bar:.3f} bar")
    print(f"Ae/At       : {r.area_ratio:.3f}")
    print(f"Tc          : {r.tc_k:.1f} K")
    print(f"c*          : {r.cstar_m_s:.1f} m/s")
    print(f"Isp         : {r.isp_m_s:.1f} m/s  ({r.isp_s:.2f} s)")
    print(f"Isp vac     : {r.isp_vac_m_s:.1f} m/s  ({r.isp_vac_s:.2f} s)")
    print(f"Cf          : {r.cf:.4f}")
    if r.density_isp_s is not None:
        print(f"Density-Isp : {r.density_isp_s:.3f} (proxy)")


def cmd_list_pairs(_: argparse.Namespace) -> int:
    for p in list_propellant_pairs():
        print(f"{p.key:16s}  {p.label:20s}  O/F default={p.of_default}  [{p.of_min}-{p.of_max}]  {p.notes}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if args.pair:
        r = run_from_pair(args.pair, of_ratio=args.of, pc_bar=args.pc, area_ratio=args.eps)
    else:
        if not args.fuel or not args.oxidizer:
            print("Provide --pair or both --fuel and --oxidizer", file=sys.stderr)
            return 2
        inputs = EngineInputs(
            fuel=args.fuel,
            oxidizer=args.oxidizer,
            of_ratio=args.of or 2.0,
            pc_bar=args.pc,
            area_ratio=args.eps,
        )
        r = run_rocket(inputs)
    _print_result(r)
    if args.json:
        print(json.dumps(r.to_dict(), indent=2))
    return 0 if r.success else 1


def cmd_sweep(args: argparse.Namespace) -> int:
    pair = get_pair(args.pair)
    base = EngineInputs(
        fuel=pair.fuel.name,
        oxidizer=pair.oxidizer.name,
        of_ratio=args.of or pair.of_default,
        pc_bar=args.pc,
        area_ratio=args.eps,
        fuel_temp_k=pair.fuel.temp_k,
        oxidizer_temp_k=pair.oxidizer.temp_k,
    )
    if args.param == "of":
        lo = args.min if args.min is not None else pair.of_min
        hi = args.max if args.max is not None else pair.of_max
        sweep = sweep_of(base, lo, hi, n=args.n)
    elif args.param == "pc":
        lo = args.min if args.min is not None else 10.0
        hi = args.max if args.max is not None else 100.0
        sweep = sweep_pc(base, lo, hi, n=args.n)
    else:
        lo = args.min if args.min is not None else 10.0
        hi = args.max if args.max is not None else 80.0
        sweep = sweep_area_ratio(base, lo, hi, n=args.n)

    df = sweep_to_dataframe(sweep)
    out = Path(args.out) if args.out else Path("results") / f"sweep_{args.param}_{args.pair}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(df.to_string(index=False))
    print(f"\nWrote {out}")
    return 0


def cmd_optimize(args: argparse.Namespace) -> int:
    pair = get_pair(args.pair)
    base = EngineInputs(
        fuel=pair.fuel.name,
        oxidizer=pair.oxidizer.name,
        of_ratio=pair.of_default,
        pc_bar=args.pc,
        area_ratio=args.eps,
        fuel_temp_k=pair.fuel.temp_k,
        oxidizer_temp_k=pair.oxidizer.temp_k,
    )
    if args.vars == "of":
        res = optimize_of(base, pair.of_min, pair.of_max, objective=args.objective)
    else:
        res = optimize_of_pc(
            base,
            (pair.of_min, pair.of_max),
            (args.pc_min, args.pc_max),
            objective=args.objective,
            maxiter=args.maxiter,
        )
    print(f"Objective : {res.objective}")
    print(f"Success   : {res.success}  ({res.message})")
    print(f"Best value: {res.best_value}")
    if res.best_result:
        _print_result(res.best_result)
    return 0 if res.success else 1


def cmd_rank(args: argparse.Namespace) -> int:
    df = rank_propellant_pairs(pc_bar=args.pc, area_ratio=args.eps)
    print(df.to_string(index=False))
    out = Path(args.out) if args.out else Path("results") / "rank_pairs.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"\nWrote {out}")
    return 0


def cmd_pareto(args: argparse.Namespace) -> int:
    pair = get_pair(args.pair)
    base = EngineInputs(
        fuel=pair.fuel.name,
        oxidizer=pair.oxidizer.name,
        of_ratio=pair.of_default,
        pc_bar=args.pc,
        area_ratio=args.eps,
        fuel_temp_k=pair.fuel.temp_k,
        oxidizer_temp_k=pair.oxidizer.temp_k,
    )
    pts = multi_objective_of_sweep(base, pair.of_min, pair.of_max, n=args.n, obj1="isp", obj2="neg_tc")
    # Convert to (isp, -neg_tc=tc) for display maximization of isp and minimization of tc
    points = [(o1, -o2, r) for _, o1, o2, r in pts]  # isp, tc, result
    front = pareto_front_2d(points, maximize=(True, False))  # max isp, min tc
    print("Pareto front (max Isp, min Tc):")
    for isp, tc, r in front:
        print(f"  O/F={r.inputs.of_ratio:6.3f}  Isp={isp:7.2f} s  Tc={tc:8.1f} K")
    return 0



def cmd_validate(args: argparse.Namespace) -> int:
    from rocketcae.validation import format_validation_report, validation_passed
    case = getattr(args, "case", "all")
    report = format_validation_report(cases=case)
    print(report)
    return 0 if validation_passed(cases=case) else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rocketcae",
        description="RocketCAE — preliminary LRE trades via NASA CEA",
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("list-pairs", help="List curated propellant pairs")
    s.set_defaults(func=cmd_list_pairs)

    s = sub.add_parser("run", help="Single CEA rocket evaluation")
    s.add_argument("--pair", help="Curated pair key (e.g. lox_rp1)")
    s.add_argument("--fuel", help="CEA fuel species name")
    s.add_argument("--oxidizer", help="CEA oxidizer species name")
    s.add_argument("--of", type=float, default=None, help="Oxidizer/fuel mass ratio")
    s.add_argument("--pc", type=float, default=50.0, help="Chamber pressure [bar]")
    s.add_argument("--eps", type=float, default=40.0, help="Nozzle area ratio Ae/At")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("sweep", help="Parameter sweep")
    s.add_argument("--pair", required=True)
    s.add_argument("--param", choices=["of", "pc", "eps"], default="of")
    s.add_argument("--min", type=float, default=None)
    s.add_argument("--max", type=float, default=None)
    s.add_argument("--n", type=int, default=15)
    s.add_argument("--of", type=float, default=None)
    s.add_argument("--pc", type=float, default=50.0)
    s.add_argument("--eps", type=float, default=40.0)
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_sweep)

    s = sub.add_parser("optimize", help="Maximize Isp (or other) over O/F or O/F+Pc")
    s.add_argument("--pair", required=True)
    s.add_argument("--vars", choices=["of", "of_pc"], default="of")
    s.add_argument("--objective", choices=["isp", "isp_vac", "cstar", "density_isp"], default="isp")
    s.add_argument("--pc", type=float, default=50.0)
    s.add_argument("--eps", type=float, default=40.0)
    s.add_argument("--pc-min", type=float, default=20.0)
    s.add_argument("--pc-max", type=float, default=100.0)
    s.add_argument("--maxiter", type=int, default=12)
    s.set_defaults(func=cmd_optimize)

    s = sub.add_parser("rank", help="Rank all curated propellant pairs")
    s.add_argument("--pc", type=float, default=50.0)
    s.add_argument("--eps", type=float, default=40.0)
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_rank)

    s = sub.add_parser("pareto", help="O/F Pareto front: max Isp vs min Tc")
    s.add_argument("--pair", required=True)
    s.add_argument("--pc", type=float, default=50.0)
    s.add_argument("--eps", type=float, default=40.0)
    s.add_argument("--n", type=int, default=21)
    s.set_defaults(func=cmd_pareto)

    
    s = sub.add_parser("validate", help="Run RP-1311 Example 8/13 validation vs NASA published output")
    s.add_argument(
        "--case",
        choices=["ex8", "ex13", "all"],
        default="all",
        help="Which RP-1311 example(s) to validate (default: all)",
    )
    s.set_defaults(func=cmd_validate)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    code = args.func(args)
    raise SystemExit(code)


if __name__ == "__main__":
    main()

