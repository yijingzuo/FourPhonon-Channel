import numpy as np
from fourphonon_channel.channel_io import ATOL, RTOL


def test_3ph_ao_closure(reference):
    d = reference["3ph"]
    np.testing.assert_allclose(d["total"], d["AAA"]+d["AAO"]+d["AOO"]+d["OOO"], atol=ATOL, rtol=RTOL)
