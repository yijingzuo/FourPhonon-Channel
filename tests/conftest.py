from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fourphonon_channel.channel_io import read_reference  # noqa: E402


@pytest.fixture(scope="session")
def reference():
    return read_reference(Path(__file__).parent / "reference")
