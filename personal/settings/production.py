"""Production settings."""

from .common import *
from aws.conf import *

ALLOWED_HOSTS = ["api.florimondmanca.com", ".florimond.dev"]

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^(https?://)?(\w+\.)?florimondmanca\.com$",
    r"^(https?://)?(\w+\.)?florimond\.dev$",
]
