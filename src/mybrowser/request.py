"""Classes and functions related to HTTP requests."""

import socket
from io import TextIOWrapper
from typing import Final, NewType

from mybrowser.url import Url

ResponseContent = NewType("ResponseContent", str)
"""The content of an HTTP response."""


def request(url: Url) -> ResponseContent:
    """Connect to the address of an URL, request the content and return the response."""
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    s.connect((url.hostname, 80))

    request = f"GET {url.path} HTTP/1.0\r\n" + f"Host: {url.hostname}\r\n" + "\r\n"
    s.send(request.encode(encoding="utf8", errors="strict"))

    response: TextIOWrapper = s.makefile("r", encoding="utf8", newline="\r\n")

    s.close()

    return _parse_response(response)


def _parse_response(buffer: TextIOWrapper) -> ResponseContent:
    """Parse an HTTP response by checking status line and header and returning the content.

    Raises:
        EmptyStatusLineError: if an empty status line is encountered
        ValueError: if the status line does not conform to the HTTP response standard
        StatusCodeError:
        TransferEncodingError: if the header contains a transfer encoding
        ContentEncodingError: if the header contains a content encoding and no transfer encoding
    """
    status_line = buffer.readline()
    if len(status_line) == 0:
        raise EmptyStatusLineError

    _version, status, _explanation = status_line.split(" ", 2)
    # We do not verify the HTTP version because servers may be misconfigured and respond in HTTP 1.1
    # even though we talk to them in HTTP 1.0. However, we still raise an ValueError if the status
    # line has an unexpected format or contains bad values.

    try:
        status_code = int(status)
    except ValueError as err:
        raise InvalidStatusError from err

    min_error_value: Final[int] = 400  # defined by HTTP standard
    if status_code >= min_error_value:
        raise StatusCodeError(status_code)

    response_headers: dict[str, str] = {}
    while True:
        line = buffer.readline()
        if line == "\r\n":
            break

        header, value = line.split(":", maxsplit=1)
        response_headers[header.casefold()] = value.strip()

    if "transfer-encoding" in response_headers:
        raise TransferEncodingError
    if "content-encoding" in response_headers:
        raise ContentEncodingError

    return ResponseContent(buffer.read())


class EmptyStatusLineError(Exception):
    """Error raised when an empty status line is encountered in an HTTP response header."""

    MSG: Final[str] = "Empty status lines in HTTP responses are not supported."

    def __init__(self) -> None:
        """Create the exception and error message."""
        super().__init__(self.MSG)


class InvalidStatusError(Exception):
    """Error raised when an invalid status is encountered in the status line of an HTTP response."""

    MSG: Final[str] = "Status in HTTP status line cannot be interpreted as an HTTP status code."

    def __init__(self) -> None:
        """Create the exception and error message."""
        super().__init__(self.MSG)


class StatusCodeError(Exception):
    """Error raised when an error code is encountered in the status line of an HTTP response."""

    MSG: Final[str] = "HTTP status line reports an error: "

    def __init__(self, error_code: int) -> None:
        """Create the exception and error message."""
        super().__init__(self.MSG + str(error_code))


class TransferEncodingError(Exception):
    """Error raised when a transfer encoding is encountered in an HTTP response header."""

    MSG: Final[str] = "Transfer encodings in response headers are not supported."

    def __init__(self) -> None:
        """Create the exception and error message."""
        super().__init__(self.MSG)


class ContentEncodingError(Exception):
    """Error raised when a content encoding is encountered in an HTTP response header."""

    MSG: Final[str] = "Content encodings in response headers are not supported."

    def __init__(self) -> None:
        """Create the exception and error message."""
        super().__init__(self.MSG)
