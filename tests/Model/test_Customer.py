import pytest
from datetime import date
from pydantic_core import ValidationError
from src.Model.customer import Customer


def test_customer_constructor_ok():
    customer = Customer(
        id_user=1,
        username="john_doe",
        password="secret",
        sign_up_date=date(2025, 1, 1),
        phone_number="0606060606"
    )
    assert customer.id_user == 1
    assert customer.username == "john_doe"
    assert customer.password == "secret"
    assert customer.sign_up_date == date(2025, 1, 1)
    assert customer.phone_number == "0606060606"


def test_customer_invalid_id_raises_validationerror():
    with pytest.raises(ValidationError):
        Customer(
            id_user="one",
            username="john_doe",
            password="secret",
            sign_up_date=date(2025, 1, 1),
            phone_number="0606060606"
        )
