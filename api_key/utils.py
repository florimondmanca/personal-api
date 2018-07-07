import os
import binascii


def generate_key():
    """Return a random API key."""
    return binascii.hexlify(os.urandom(16)).decode()
