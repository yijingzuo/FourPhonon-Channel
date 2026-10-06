"""Dependency-light release test runner (pytest is optional)."""

from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fourphonon_channel.channel_io import ATOL, RTOL, passed, read_reference, validate


def close(a, b):
    np.testing.assert_allclose(a, b, atol=ATOL, rtol=RTOL)


def main():
    ref = read_reference(Path(__file__).parent / "reference")
    d3, d4 = ref["3ph"], ref["4ph"]
    checks = [
        ("3ph A/O closure", lambda: close(d3["total"], d3["AAA"] + d3["AAO"] + d3["AOO"] + d3["OOO"])),
        ("4ph A/O closure", lambda: close(d4["total"], d4["AAAA"] + d4["AAAO"] + d4["AAOO"] + d4["AOOO"] + d4["OOOO"])),
        ("3ph three-way", lambda: (close(d3["total"], d3["topology_sum"]), close(d3["topology_sum"], d3["ao_sum"]))),
        ("4ph three-way", lambda: (close(d4["total"], d4["topology_sum"]), close(d4["topology_sum"], d4["ao_sum"]))),
        ("acoustic structural zeros", lambda: (
            np.testing.assert_array_equal(d3["OOO"][d3["branch"] <= 3], 0),
            np.testing.assert_array_equal(d4["OOOO"][d4["branch"] <= 3], 0),
        )),
    ]
    for name, check in checks:
        check()
        print(f"PASS: {name}")
    assert passed(validate(ref))
    print(f"{len(checks)}/{len(checks)} release checks passed")


if __name__ == "__main__":
    main()
