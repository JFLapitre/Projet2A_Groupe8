from datetime import date

import pytest
from pydantic_core import ValidationError

from src.Model.driver import Driver


def test_driver_constructor_ok():
    driver = Driver(
        id_user=1,
        username="driver_1",
        password="strong_pwd",
        sign_up_date=date(2025, 1, 1),
        name="Jean Dupont",
        phone_number="0601020304",
        vehicle_type="bike",
        availability=True
    )

    assert driver.id_user == 1
    assert driver.username == "driver_1"
    assert driver.password == "strong_pwd"
    assert driver.name == "Jean Dupont"
    assert driver.phone_number == "0601020304"
    assert driver.vehicle_type == "bike"
    assert driver.availability is True
    assert isinstance(driver.sign_up_date, date)


def test_driver_invalid_id_raises_validationerror():
    # id_user invalide (chaîne au lieu d'un entier)
    with pytest.raises(ValidationError):
        Driver(
            id_user="one",
            username="driver_1",
            password="strong_pwd",
            sign_up_date=date(2025, 1, 1),
            name="Jean Dupont",
            phone_number="0601020304",
            vehicle_type="bike",
            availability=True
        )
