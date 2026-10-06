"""Command-line interface."""

from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np
from .channel_io import CHANNELS, passed, read_any, validate


def cmd_validate(args):
    report = validate(read_any(args.path))
    for order, comparisons in report.items():
        for name, x in comparisons.items():
            print(f"{order} {name}: max_abs={x['max_abs']:.8e} max_rel={x['max_rel']:.8e} failed={x['failed']}")
    print("THREE-WAY SCATTERING-RATE VALIDATION:", "PASS" if passed(report) else "FAIL")
    return 0 if passed(report) else 1


def cmd_summarize(args):
    data = read_any(args.path)
    for order in ("3ph", "4ph"):
        d = data[order]; mask = d["branch"] <= 3 if args.acoustic_targets else np.ones(len(d["branch"]), bool)
        for channel in CHANNELS[order]: print(f"{order},{channel},{d[channel][mask].sum():.15g}")
    return 0


def cmd_compare(args):
    a, b = read_any(args.path0), read_any(args.path5)
    rows = []
    for order in ("3ph", "4ph"):
        for channel in CHANNELS[order]:
            m0=a[order]["branch"]<=3; m5=b[order]["branch"]<=3
            s0=a[order][channel][m0].sum(); s5=b[order][channel][m5].sum()
            pct=(s5/s0-1)*100 if s0 else (0.0 if s5==0 else np.inf)
            rows.append((order,channel,s0,s5,pct))
    with Path(args.output).open("w",newline="") as f:
        w=csv.writer(f); w.writerow(("order","channel","sum_path0","sum_path5","percent_change")); w.writerows(rows)
    return 0


def cmd_plot(args):
    from .plotting import plot_channels
    plot_channels(read_any(args.path), args.output)
    return 0


def main(argv=None):
    p=argparse.ArgumentParser(prog="fourphonon-channel")
    s=p.add_subparsers(dest="command",required=True)
    v=s.add_parser("validate"); v.add_argument("path"); v.set_defaults(func=cmd_validate)
    u=s.add_parser("summarize"); u.add_argument("path"); u.add_argument("--acoustic-targets",action="store_true"); u.set_defaults(func=cmd_summarize)
    c=s.add_parser("compare"); c.add_argument("path0"); c.add_argument("path5"); c.add_argument("--output",required=True); c.set_defaults(func=cmd_compare)
    q=s.add_parser("plot"); q.add_argument("path"); q.add_argument("--output",required=True); q.set_defaults(func=cmd_plot)
    a=p.parse_args(argv); return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main())
