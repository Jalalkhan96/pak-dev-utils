"""Pakistani IBAN (ISO 13616) validation.

A Pakistani IBAN is 24 characters: ``PK`` + 2 check digits + a
4-character bank identifier + a 16-digit account number, e.g.
``PK36SCBL0000001123456702`` (the well-known ISO example).
Validation is the standard mod-97 check: move the first 4 characters
to the end, convert letters A=10..Z=35, and require remainder 1.
"""

import re

_IBAN = re.compile(r"^PK\d{2}[A-Z0-9]{4}\d{16}$")


def _mod97(iban):
    rearranged = iban[4:] + iban[:4]
    numeric = "".join(
        str(int(ch, 36)) if ch.isalpha() else ch for ch in rearranged
    )
    return int(numeric) % 97


def normalize_iban_pk(iban):
    """Return the IBAN upper-cased with spaces removed, or ``""``."""
    if not isinstance(iban, str):
        return ""
    return iban.strip().replace(" ", "").upper()


def is_valid_iban_pk(iban):
    """Return True only for a 24-char PK IBAN passing the mod-97 check."""
    if not isinstance(iban, str):
        return False
    text = normalize_iban_pk(iban)
    if not _IBAN.match(text):
        return False
    return _mod97(text) == 1


def format_iban_pk(iban):
    """Format a valid PK IBAN in groups of 4 characters.

    Raises ValueError for an invalid IBAN.
    """
    text = normalize_iban_pk(iban)
    if not is_valid_iban_pk(iban):
        raise ValueError("invalid Pakistani IBAN (expected PK + 22 chars, mod-97 = 1)")
    return " ".join(text[i : i + 4] for i in range(0, len(text), 4))
