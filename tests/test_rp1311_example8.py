"""Validate against published NASA RP-1311 Example 8."""

from __future__ import annotations

import pytest

pytest.importorskip("cea")

from rocketcae.validation import (
    compare_rp1311_example8,
    format_validation_report,
    validation_passed,
)


def test_rp1311_example8_all_checkpoints():
    rows = compare_rp1311_example8()
    failed = [r for r in rows if not r.pass_]
    if failed:
        report = format_validation_report(rows)
        pytest.fail("RP-1311 Example 8 validation failed:\n" + report)
    assert validation_passed(rows)
    assert len(rows) >= 10


def test_rp1311_chamber_temperature_close():
    rows = compare_rp1311_example8()
    t_row = next(r for r in rows if r.station == "chamber" and r.quantity == "T_K")
    assert abs(t_row.computed - 3383.845) < 5.0


def test_rp1311_isp_at_eps25():
    rows = compare_rp1311_example8()
    isp = next(
        r for r in rows if r.station == "Ae/At=25" and r.quantity == "Isp_m_s"
    )
    # Published 4124.410 m/s
    assert abs(isp.computed - 4124.410) / 4124.410 < 0.005
