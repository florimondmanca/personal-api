"""Production settings."""

from .common import *
from aws.conf import *

ALLOWED_HOSTS = ["api.florimondmanca.com", ".florimond.dev"]

CORS_ORIGIN_REGEX_WHITELIST = [
    # florimondmanca.com and any subdomains
    r"^(https?://)?(\w+\.)?florimondmanca\.com$"
]
