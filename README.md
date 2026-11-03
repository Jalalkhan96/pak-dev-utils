# pak-dev-utils

Small, dependency-free Python validators and formatters for Pakistani
identifiers — written for developers who need quick, honest format checks
(no network calls, no secrets, no invented checksums).

## What it validates

| Identifier | Format | Check |
| --- | --- | --- |
| CNIC | `xxxxx-xxxxxxx-x` (13 digits) | Format only — there is no published CNIC checksum, so this module does **not** claim a number is genuinely issued. |
| Pakistani mobile | `03xx-xxxxxxx` / `+92 3xx xxxxxxx` | 11-digit mobile series `030x`–`035x`; landline-style numbers are rejected. |
| PK IBAN | `PK` + 2 check digits + 4-char bank code + 16 digits (24 chars) | Full ISO 13616 mod-97 check. |

## Usage

```python
from pak_dev_utils import (
    format_cnic, is_valid_cnic,
    format_phone_pk, is_valid_phone_pk,
    format_iban_pk, is_valid_iban_pk,
)

is_valid_cnic("35202-1234567-1")          # True
format_cnic("3520212345671")              # "35202-1234567-1"

is_valid_phone_pk("+92 323 9352963")     # True
format_phone_pk("03239352963")            # "0323-9352963"
format_phone_pk("03239352963", international=True)  # "+92 323 9352963"

is_valid_iban_pk("PK36SCBL0000001123456702")  # True
format_iban_pk("PK36SCBL0000001123456702")    # "PK36 SCBL 0000 0011 2345 6702"
```

Invalid input raises `ValueError` from the `format_*` functions instead of
formatting garbage; the `is_valid_*` functions return `False` (never raise)
for bad input, including `None` and non-strings.

## Tests

```bash
python3 -m pytest tests/ -q
```
