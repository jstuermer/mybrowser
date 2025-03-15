"""Request implementations."""

import socket

from mybrowser.url import Url


def request(url: Url) -> None:
    """Connect to the specified url."""
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    s.connect((url.hostname, 80))
