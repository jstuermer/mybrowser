"""Entry point of the browser."""

from request import request
from url import Url


def main() -> None:
    """Start the browser."""
    print("Connecting to example.org")
    url = Url("http://example.org")
    request(url)
