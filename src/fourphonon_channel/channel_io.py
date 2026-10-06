"""Readers and validation primitives for FourPhonon channel output."""

from __future__ import annotations
from pathlib import Path
import csv
import numpy as np

ATOL = 2.0e-9
RTOL = 2.0e-9
NEAR_ZERO = 1.0e-12
CHANNELS = {"3ph": ("AAA", "AAO", "AOO", "OOO"),
            "4ph": ("AAAA", "AAAO", "AAOO", "AOOO", "OOOO")}
TOPOLOGY = {"3ph": ("plus", "minus"),
            "4ph": ("plusplus", "plusminus", "minusminus")}


def _load(path: Path) -> np.ndarray:
    data = np.loadtxt(path)
    return np.atleast_2d(data)


def read_calculation(path: str | Path) -> dict[str, dict[str, np.ndarray]]:
    path = Path(path)
    result: dict[str, dict[str, np.ndarray]] = {}
    for order in ("3ph", "4ph"):
        prefix = order[0]
        total_file = path / f"BTE.w_{order}"
        total_raw = _load(total_file)
        channels = {name: _load(path / f"BTE.Scatt{prefix}_{name}")
                    for name in CHANNELS[order]}
        topo = {name: _load(path / f"BTE.w_{order}_{name}")[:, 1]
                for name in TOPOLOGY[order]}
        first = channels[CHANNELS[order][0]]
        result[order] = {
            "mode": first[:, 0].astype(int), "q": first[:, 1].astype(int),
            "branch": first[:, 2].astype(int), "frequency": first[:, 3],
            "total": total_raw[:, 1],
            "topology_sum": np.sum(list(topo.values()), axis=0),
            **{name: data[:, 4] for name, data in channels.items()},
        }
        result[order]["ao_sum"] = np.sum([result[order][x] for x in CHANNELS[order]], axis=0)
    return result


def read_reference(path: str | Path) -> dict[str, dict[str, np.ndarray]]:
    path = Path(path)
    if path.is_dir():
        path = path / "channel_reference.csv"
    with path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    result = {}
    for order in ("3ph", "4ph"):
        rr = [x for x in rows if x["scattering_order"] == order]
        d = {key: np.array([float(x[key]) for x in rr]) for key in
             ("mode", "q", "branch", "frequency_rad_per_ps", "total", "topology_sum", *CHANNELS[order])}
        d["mode"] = d["mode"].astype(int); d["q"] = d["q"].astype(int); d["branch"] = d["branch"].astype(int)
        d["frequency"] = d.pop("frequency_rad_per_ps")
        d["ao_sum"] = np.sum([d[x] for x in CHANNELS[order]], axis=0)
        result[order] = d
    return result


def read_any(path: str | Path):
    path = Path(path)
    if path.is_file() or (path / "channel_reference.csv").exists():
        return read_reference(path)
    return read_calculation(path)


def comparison(a: np.ndarray, b: np.ndarray, atol=ATOL, rtol=RTOL, near_zero=NEAR_ZERO):
    residual = a - b
    scale = np.maximum(np.abs(a), np.abs(b))
    stable = scale > near_zero
    relative = np.zeros_like(scale)
    relative[stable] = np.abs(residual[stable]) / scale[stable]
    failed = np.abs(residual) > (atol + rtol * scale)
    return {"max_abs": float(np.max(np.abs(residual))),
            "max_rel": float(np.max(relative[stable])) if np.any(stable) else 0.0,
            "failed": int(np.count_nonzero(failed))}


def validate(data):
    report = {}
    for order in ("3ph", "4ph"):
        d = data[order]
        report[order] = {
            "total_topology": comparison(d["total"], d["topology_sum"]),
            "total_AO": comparison(d["total"], d["ao_sum"]),
            "topology_AO": comparison(d["topology_sum"], d["ao_sum"]),
        }
    return report


def passed(report) -> bool:
    return all(x["failed"] == 0 for order in report.values() for x in order.values())
