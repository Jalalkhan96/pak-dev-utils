"""Tests for pak-dev-utils: CNIC, Pakistani mobile, PK IBAN."""

import pytest

from pak_dev_utils import (
    format_cnic,
    format_iban_pk,
    format_phone_pk,
    is_valid_cnic,
    is_valid_iban_pk,
    is_valid_phone_pk,
    normalize_cnic,
    normalize_phone_pk,
)


# --- CNIC -----------------------------------------------------------------
def test_cnic_valid_forms():
    assert is_valid_cnic("35202-1234567-1")
    assert is_valid_cnic("3520212345671")
    assert is_valid_cnic(" 35202-1234567-1 ")


def test_cnic_invalid():
    assert not is_valid_cnic("35202-123456-1")  # 12 digits
    assert not is_valid_cnic("35202123456712")  # 14 digits
    assert not is_valid_cnic("35202-1234567-A")  # non-digit
    assert not is_valid_cnic("3520-21234567-1")  # misplaced dash
    assert not is_valid_cnic("00000-0000000-0")  # all zeros
    assert not is_valid_cnic("00000-1234567-1")  # zero first block
    assert not is_valid_cnic(None)
    assert not is_valid_cnic(3520212345671)


def test_cnic_format():
    assert format_cnic("3520212345671") == "35202-1234567-1"
    assert format_cnic("35202-1234567-1") == "35202-1234567-1"
    assert normalize_cnic("35202-1234567-1") == "3520212345671"
    with pytest.raises(ValueError):
        format_cnic("35202-123456-1")


# --- Pakistani mobile ------------------------------------------------------
def test_phone_valid_forms():
    assert is_valid_phone_pk("0323-9352963")
    assert is_valid_phone_pk("03239352963")
    assert is_valid_phone_pk("+92 323 9352963")
    assert is_valid_phone_pk("00923239352963")
    assert is_valid_phone_pk("0300-1234567")
    assert is_valid_phone_pk("0355-1234567")  # 035x series


def test_phone_invalid():
    assert not is_valid_phone_pk("0323-935296")  # 10 digits
    assert not is_valid_phone_pk("0323-93529633")  # 12 digits
    assert not is_valid_phone_pk("042-1234567")  # landline-style, not mobile
    assert not is_valid_phone_pk("0363-1234567")  # 036x not a mobile series
    assert not is_valid_phone_pk("+1 323 9352963")  # wrong country code
    assert not is_valid_phone_pk("")
    assert not is_valid_phone_pk(None)


def test_phone_format():
    assert format_phone_pk("03239352963") == "0323-9352963"
    assert format_phone_pk("+92 323 9352963") == "0323-9352963"
    assert format_phone_pk("03239352963", international=True) == "+92 323 9352963"
    assert normalize_phone_pk("+92 323 9352963") == "03239352963"
    with pytest.raises(ValueError):
        format_phone_pk("042-1234567")


# --- PK IBAN ---------------------------------------------------------------
# PK36SCBL0000001123456702 is the ISO 13616 example IBAN for Pakistan.
def test_iban_valid():
    assert is_valid_iban_pk("PK36SCBL0000001123456702")
    assert is_valid_iban_pk("pk36 scbl 0000 0011 2345 6702")
    assert is_valid_iban_pk("PK36SCBL0000001123456702".lower().upper())


def test_iban_invalid():
    assert not is_valid_iban_pk("PK37SCBL0000001123456702")  # bad check digits
    assert not is_valid_iban_pk("PK36SCBL000000112345670")  # 23 chars
    assert not is_valid_iban_pk("GB29NWBK60161331926819")  # not PK
    assert not is_valid_iban_pk("PK36SCBL00000011234567AB")  # letters in account
    assert not is_valid_iban_pk("")
    assert not is_valid_iban_pk(None)


def test_iban_format():
    assert format_iban_pk("PK36SCBL0000001123456702") == (
        "PK36 SCBL 0000 0011 2345 6702"
    )
    with pytest.raises(ValueError):
        format_iban_pk("PK37SCBL0000001123456702")
