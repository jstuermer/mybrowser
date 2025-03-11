"""Url class implementation."""

from typing import Final
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


class Url:
    """Url type that adheres to some constraints."""

    def __init__(self, path: str) -> None:
        """Create an url from the given path."""
        self.parsed: ParseResult = urlparse(path)

        if self.parsed.scheme != "http":
            raise SchemeError(self.parsed.scheme)
        if self.parsed.hostname is None:
            raise HostnameError(self.parsed.hostname)
        if "." not in self.parsed.netloc:
            raise NetlocError(self.parsed.netloc)
