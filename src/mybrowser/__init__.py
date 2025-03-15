"""Entry point of the browser."""

from mybrowser.request import request
from mybrowser.url import Url, parse_url


def main() -> None:
    """Start the browser."""
    print("Connecting to example.org")
    url: Url = parse_url(path="http://example.org")
    request(url)
