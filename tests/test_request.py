"""Unit tests for HTTP requests."""

import io
from collections.abc import Buffer
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from mybrowser.request import (
    ContentEncodingError,
    EmptyStatusLineError,
    InvalidStatusError,
    StatusCodeError,
    TransferEncodingError,
    _parse_response,
)


@pytest.mark.parametrize(
    argnames=("response_buffer", "expected_behaviour"),
    argvalues=[
        (
            b"",
            pytest.raises(EmptyStatusLineError, match=EmptyStatusLineError.MSG),
        ),
        (
            b"invalid",
            pytest.raises(ValueError, match="not enough values to unpack"),
        ),
        (
            b"invalid status line",
            pytest.raises(InvalidStatusError, match=InvalidStatusError.MSG),
        ),
        (
            b"HTTP/1.0 400 ERROR",
            pytest.raises(StatusCodeError, match=StatusCodeError.MSG),
        ),
        (
            b"HTTP/1.0 399 REDIRECTED",
            pytest.raises(ValueError, match="not enough values to unpack"),
        ),
        (
            b"HTTP/1.0 399 REDIRECTED\r\n",
            pytest.raises(ValueError, match="not enough values to unpack"),
        ),
        (
            b"HTTP/1.0 399 REDIRECTED\r\n\r\n",
            does_not_raise(),
        ),
        (
            b"HTTP/1.0 399 REDIRECTED\r\n" + b"Date: 2025-03-18",
            pytest.raises(ValueError, match="not enough values to unpack"),
        ),
        (
            b"HTTP/1.0 399 REDIRECTED\r\n" + b"Date: 2025-03-18\r\n\r\n",
            does_not_raise(),
        ),
        (
            b"HTTP/1.0 399 REDIRECTED\r\n" + b"Transfer-Encoding: something\r\n\r\n",
            pytest.raises(TransferEncodingError, match=TransferEncodingError.MSG),
        ),
        (
            b"HTTP/1.0 399 REDIRECTED\r\n" + b"Content-Encoding: something\r\n\r\n",
            pytest.raises(ContentEncodingError, match=ContentEncodingError.MSG),
        ),
    ],
    ids=(
        "empty-status-line",
        "invalid-status-line",
        "invalid-status-in-status-line",
        "valid-status-line-with-error-code",
        "valid-status-line-without-line-break",
        "valid-status-line-with-line-break-but-without-empty-line",
        "valid-status-line-with-line-break-and-empty-line",
        "valid-status-line-with-valid-header-but-without-line-break",
        "valid-status-line-with-valid-header-and-line-break",
        "invalid-response-with-transfer-encoding",
        "invalid-response-with-content-encoding",
    ),
)
def test_parse_response_raises_for_invalid_header(
    response_buffer: Buffer, expected_behaviour: AbstractContextManager
) -> None:
    """Test that creating an url validates data."""
    # ARRANGE
    buffer = io.TextIOWrapper(io.BytesIO(response_buffer), encoding="utf-8", newline="\r\n")

    # ASSERT
    with expected_behaviour:
        # ACT
        _parse_response(buffer)
