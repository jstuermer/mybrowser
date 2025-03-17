"""Unit tests of URL ."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from mybrowser.url import HostnameError, NetlocError, SchemeError, parse_url


@pytest.mark.parametrize(
    argnames=("path", "expected_behaviour"),
    argvalues=[
        ("foo", pytest.raises(SchemeError, match=SchemeError.MSG)),
        ("http://", pytest.raises(HostnameError, match=HostnameError.MSG)),
        ("http://foo", pytest.raises(NetlocError, match=NetlocError.MSG)),
        ("http://foo.com", does_not_raise()),
        ("http://foo.com/index.html", does_not_raise()),
    ],
    ids=(
        "invalid-scheme",
        "missing-hostname",
        "invalid-netloc",
        "valid-url",
        "valid-url-with-path",
    ),
)
def test_parse_url_raises_for_invalid_input(
    path: str, expected_behaviour: AbstractContextManager
) -> None:
    """Test that creating an url validates data."""
    # ASSERT
    with expected_behaviour:
        # ACT
        parse_url(path)
