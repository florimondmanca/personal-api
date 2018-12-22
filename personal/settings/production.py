"""Production settings."""

from .common import *
from aws.conf import *

ALLOWED_HOSTS = ["api.florimondmanca.com"]

CORS_ORIGIN_REGEX_WHITELIST = [
    # florimondmanca.com and any subdomains
    r"^(https?://)?(\w+\.)?florimondmanca\.com$"
]
