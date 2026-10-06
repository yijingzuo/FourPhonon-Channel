import numpy as np
from fourphonon_channel.channel_io import ATOL, RTOL, passed, validate


def test_three_way_validation(reference):
    report = validate(reference)
    assert passed(report)
    for order in ("3ph", "4ph"):
        d = reference[order]
        np.testing.assert_allclose(d["total"], d["topology_sum"], atol=ATOL, rtol=RTOL)
        np.testing.assert_allclose(d["topology_sum"], d["ao_sum"], atol=ATOL, rtol=RTOL)


def test_acoustic_target_structural_zeros(reference):
    m3 = reference["3ph"]["branch"] <= 3
    m4 = reference["4ph"]["branch"] <= 3
    assert np.count_nonzero(reference["3ph"]["OOO"][m3]) == 0
    assert np.count_nonzero(reference["4ph"]["OOOO"][m4]) == 0
    # AOOO is intentionally not asserted: it is not a universal structural zero.
