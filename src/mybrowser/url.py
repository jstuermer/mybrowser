"""Url class implementation."""

from dataclasses import dataclass
from typing import Final, Literal
from urllib.parse import ParseResult, urlparse


class SchemeError(Exception):
    """Error raised when an unsupported scheme is encountered in a parsed url."""

    BASE_MSG: Final[str] = "Unsupported url scheme encountered"
    """Base error message uniquely identifying this error."""

    def __init__(self, scheme: str) -> None:
        """Create the exception and error message."""
        super().__init__(self.BASE_MSG + ": " + scheme)


class HostnameError(Exception):
    """Error raised when an unsupported hostname is encountered in a parsed url."""

    BASE_MSG: Final[str] = "Unsupported hostname encountered"
    """Base error message uniquely identifying this error."""

    def __init__(self, hostname: str | None) -> None:
        """Create the exception and error message."""
        super().__init__(self.BASE_MSG + ": " + str(hostname))


class NetlocError(Exception):
    """Error raised when an unsupported netloc is encountered in a parsed url."""

    BASE_MSG: Final[str] = "Unsupported netloc encountered"
    """Base error message uniquely identifying this error."""

    def __init__(self, netloc: str) -> None:
        """Create the exception and error message."""
        super().__init__(self.BASE_MSG + ": " + netloc)


@dataclass(frozen=True)
class Url:
    """Url type returned by `parse_url`."""

    scheme: Literal["http"]
    hostname: str
    netloc: str
    path: str


def parse_url(path: str) -> Url:
    """Parse a path into a `Url` using `urllib.parse.urlparse` and verify its validity.

    Raises:
        SchemeError: if the `scheme` is not HTTP
        HostnameError: if the parsed `hostname` is not a valid string
        NetlocError: if the parsed `netloc` is not a valid location
    """
    result: ParseResult = urlparse(path)

    supported_scheme: Literal["http"] = "http"
    if result.scheme != supported_scheme:
        raise SchemeError(result.scheme)
    if result.hostname is None:
        raise HostnameError(result.hostname)
    if "." not in result.netloc:
        raise NetlocError(result.netloc)

    return Url(
        scheme=supported_scheme, hostname=result.hostname, netloc=result.netloc, path=result.path
    )
