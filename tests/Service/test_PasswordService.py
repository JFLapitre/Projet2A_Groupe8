import pytest

from src.Service.password_service import PasswordService


@pytest.fixture
def service():
    """
    Provides a PasswordService instance for each test.
    """
    return PasswordService()


def test_hash_password_with_known_salt(service: PasswordService):
    """
    Tests hashing a known password and salt produces a known hash.
    """
    password = "soleil1234"
    salt = "jambon"
    # This hash is specific to your *new* implementation logic.
    expected_hash = "7877d4860ef88458096f549b618667d860540db5d59b1d153557d5cdbe1221e7"

    hashed_password = service.hash_password(password, salt)

    assert hashed_password == expected_hash


def test_hash_password_requires_salt(service: PasswordService):
    """
    Tests that hash_password raises ValueError if no salt is provided.
    """
    password = "onepassword"

    with pytest.raises(ValueError) as e:
        service.hash_password(password, salt=None)

    assert "Salt must be provided" in str(e.value)


def test_different_salts_produce_different_hashes(service: PasswordService):
    """
    Tests that the same password with different salts produces different hashes.
    """
    password = "mysecretpassword"
    salt1 = "salt_A"
    salt2 = "salt_B"

    hash1 = service.hash_password(password, salt1)
    hash2 = service.hash_password(password, salt2)

    assert hash1 != hash2


def test_hash_is_consistent(service: PasswordService):
    """
    Tests that hashing the same password and salt multiple times yields the same hash.
    """
    password = "consistent123"
    salt = "fixed_salt"

    hash1 = service.hash_password(password, salt)
    hash2 = service.hash_password(password, salt)

    assert hash1 == hash2


def test_strength_valid_length(service: PasswordService):
    """
    Tests that a password meeting the length requirement passes.
    """
    try:
        service.check_password_strength("ValidPassword123")
        service.check_password_strength("123456789")
    except Exception as e:
        pytest.fail(f"check_password_strength raised an unexpected exception: {e}")


def test_strength_exact_length(service: PasswordService):
    """
    Tests that a password of exactly 8 characters passes.
    """
    try:
        service.check_password_strength("12345678")
    except Exception as e:
        pytest.fail(f"check_password_strength raised an unexpected exception: {e}")


def test_strength_too_short(service: PasswordService):
    """
    Tests that a password shorter than 8 characters raises an Exception.
    """
    with pytest.raises(Exception) as e:
        service.check_password_strength("1234567")

    # Check the specific error message
    assert "Password length must be at least 8 characters" in str(e.value)


def test_strength_empty_string(service: PasswordService):
    """
    Tests that an empty string (length 0) raises an Exception.
    """
    with pytest.raises(Exception) as e:
        service.check_password_strength("")  # 0 chars

    assert "Password length must be at least 8 characters" in str(e.value)
