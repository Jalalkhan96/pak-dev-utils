"""Pakistani CNIC (Computerised National Identity Card) validation.

A CNIC is 13 digits, conventionally written as ``xxxxx-xxxxxxx-x``
(5 digits, 7 digits, 1 check digit). There is no published checksum
algorithm for CNICs, so this module validates *format only* — it does
not claim a number is genuinely issued. It never invents a checksum.
"""

import re

_DIGITS_ONLY = re.compile(r"^\d{13}$")
_FORMATTED = re.compile(r"^(\d{5})-(\d{7})-(\d{1})$")


def normalize_cnic(cnic):
    """Return the 13 digits of *cnic*, or ``""`` if it is not a string.

    Dashes and surrounding whitespace are stripped; anything else is
    left in place so :func:`is_valid_cnic` rejects it.
    """
    if not isinstance(cnic, str):
        return ""
    return cnic.strip().replace("-", "").replace(" ", "")


def is_valid_cnic(cnic):
    """Return True only for a well-formed 13-digit CNIC.

    Accepts the dashed form (``35202-1234567-1``) and the bare form
    (``3520212345671``). Rejects wrong lengths, non-digits, misplaced
    dashes, and all-zero blocks (a number of all zeros is not a CNIC).
    """
    if not isinstance(cnic, str):
        return False
    text = cnic.strip()
    if _FORMATTED.match(text):
        digits = text.replace("-", "")
    elif _DIGITS_ONLY.match(text):
        digits = text
    else:
        return False
    if digits == "0" * 13:
        return False
    # The three blocks must not be individually all zeros either.
    if digits[:5] == "0" * 5 or digits[5:12] == "0" * 7:
        return False
    return True


def format_cnic(cnic):
    """Format a valid CNIC as ``xxxxx-xxxxxxx-x``.

    Raises ValueError for an invalid CNIC instead of formatting garbage.
    """
    digits = normalize_cnic(cnic)
    if not is_valid_cnic(cnic):
        raise ValueError("invalid CNIC: expected 13 digits (xxxxx-xxxxxxx-x)")
    return f"{digits[:5]}-{digits[5:12]}-{digits[12]}"
