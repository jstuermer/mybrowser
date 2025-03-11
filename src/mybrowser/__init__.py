"""Entry point of the browser."""

from mybrowser.request import request
from mybrowser.url import Url


def main() -> None:
    """Start the browser."""
    print("Connecting to example.org")
    url = Url("http://example.org")
    request(url)
