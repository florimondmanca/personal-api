"""Disable Internet access during tests."""

import socket


def _guard(*args, **kwargs):
    raise Exception("A test tried to access the Internet!")


socket.socket = _guard
