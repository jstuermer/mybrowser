"""Unit tests for the url class."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from url import HostnameError, NetlocError, SchemeError, Url


@pytest.mark.parametrize(
    argnames=("path", "expected_context"),
    argvalues=[
        ("foo", pytest.raises(SchemeError, match=SchemeError.BASE_MSG)),
        ("http://", pytest.raises(HostnameError, match=HostnameError.BASE_MSG)),
        ("http://foo", pytest.raises(NetlocError, match=NetlocError.BASE_MSG)),
        ("http://foo.com", does_not_raise()),
        ("http://foo.com/index.html", does_not_raise()),
    ],
    ids=("invalid-scheme", "missing-hostname", "missing", "valid-url", "valid-url-2"),
)
def test_url_creation_raises_for_invalid_input(
    path: str, expected_context: AbstractContextManager
) -> None:
    """Test that creating an url validates data."""
    # ASSERT
    with expected_context:
        # ACT
        Url(path)
