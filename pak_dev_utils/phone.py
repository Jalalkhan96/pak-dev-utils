"""Pakistani mobile number validation and formatting.

Accepted inputs (all for the same 11-digit national number):
``03xx-xxxxxxx``, ``03xxxxxxxxx``, ``+92 3xx xxxxxxx`` and
``00923xxxxxxxxx``. Output formats are the national ``03xx-xxxxxxx``
form and the international ``+92 3xx xxxxxxx`` form.

The third digit is restricted to 0-5, which covers the mobile series
in use (030x-035x); landline-style numbers starting 04x/05x etc. are
rejected because this is a *mobile* formatter.
"""

import re

_NATIONAL = re.compile(r"^03[0-5]\d{8}$")


def normalize_phone_pk(phone):
    """Return the 11-digit national form, or ``""`` if unparseable.

    Strips spaces, dashes and parentheses, converts a +92 / 0092
    country prefix to the leading 0, and returns the digits unchanged
    otherwise so validation can reject them.
    """
    if not isinstance(phone, str):
        return ""
    digits = re.sub(r"[\s\-()]", "", phone.strip())
    if digits.startswith("+92"):
        digits = "0" + digits[3:]
    elif digits.startswith("0092"):
        digits = "0" + digits[4:]
    return digits


def is_valid_phone_pk(phone):
    """Return True only for an 11-digit Pakistani mobile number."""
    if not isinstance(phone, str):
        return False
    return bool(_NATIONAL.match(normalize_phone_pk(phone)))


def format_phone_pk(phone, international=False):
    """Format a valid number as ``03xx-xxxxxxx`` (or ``+92 3xx xxxxxxx``).

    Raises ValueError for an invalid number.
    """
    digits = normalize_phone_pk(phone)
    if not _NATIONAL.match(digits):
        raise ValueError(
            "invalid Pakistani mobile number: expected 03xx-xxxxxxx "
            "(or +92 3xx xxxxxxx)"
        )
    if international:
        return f"+92 {digits[1:4]} {digits[4:]}"
    return f"{digits[:4]}-{digits[4:]}"
