import pytest

from app.core.security import (
    hash_password,
    validate_password_strength,
    verify_password,
)


@pytest.mark.parametrize(
    ("password", "expected_message"),
    [
        (
            "Short1!",
            "Password must be at least 12 characters",
        ),
        (
            "lowercase123!",
            "Password must contain an uppercase letter",
        ),
        (
            "UPPERCASE123!",
            "Password must contain a lowercase letter",
        ),
        (
            "NoNumbersHere!",
            "Password must contain a number",
        ),
        (
            "NoSpecial123A",
            "Password must contain a special character",
        ),
    ],
)
def test_weak_passwords_are_rejected(
    password,
    expected_message,
):
    with pytest.raises(
        ValueError,
        match=expected_message,
    ):
        validate_password_strength(password)


def test_strong_password_is_accepted():
    password = "MAJE-Strong-2026!"

    validate_password_strength(password)


def test_hash_password_enforces_policy():
    with pytest.raises(
        ValueError,
        match="Password must be at least 12 characters",
    ):
        hash_password("Weak1!")


def test_strong_password_hash_can_be_verified():
    password = "MAJE-Strong-2026!"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(
        password,
        hashed_password,
    )
    assert not verify_password(
        "Wrong-Password-2026!",
        hashed_password,
    )
