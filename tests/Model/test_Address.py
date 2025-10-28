import pytest
from pydantic_core import ValidationError

from src.Model.address import Address


def test_address_constructor_ok():
    address = Address(
        city="Rennes",
        postal_code="35000",
        street_name="Rue de la Galette",
        street_number=12
    )

    assert address.city == "Rennes"
    assert address.postal_code == "35000"
    assert address.street_name == "Rue de la Galette"
    assert address.street_number == 12


def test_address_invalid_street_number_raises_validationerror():
    # street_number invalide (chaîne au lieu d’un int)
    with pytest.raises(ValidationError):
        Address(
            city="Rennes",
            postal_code="35000",
            street_name="Rue de la Galette",
            street_number="douze"
        )
