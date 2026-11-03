"""pak-dev-utils: small validators/formatters for Pakistani identifiers.

No network access, no secrets, no external dependencies.
"""

from .cnic import format_cnic, is_valid_cnic, normalize_cnic
from .iban import format_iban_pk, is_valid_iban_pk
from .phone import format_phone_pk, is_valid_phone_pk, normalize_phone_pk

__all__ = [
    "format_cnic",
    "is_valid_cnic",
    "normalize_cnic",
    "format_iban_pk",
    "is_valid_iban_pk",
    "format_phone_pk",
    "is_valid_phone_pk",
    "normalize_phone_pk",
]

__version__ = "0.1.0"
