import numpy as np
from fourphonon_channel.channel_io import ATOL, RTOL


def test_4ph_ao_closure(reference):
    d = reference["4ph"]
    np.testing.assert_allclose(d["total"], d["AAAA"]+d["AAAO"]+d["AAOO"]+d["AOOO"]+d["OOOO"], atol=ATOL, rtol=RTOL)
