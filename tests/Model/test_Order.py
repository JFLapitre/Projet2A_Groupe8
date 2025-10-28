from datetime import date

import pytest
from pydantic_core import ValidationError

from src.Model.address import Address
from src.Model.customer import Customer
from src.Model.order import Order


def test_order_constructor_ok():
    # Crée un client et une adresse valides
    customer = Customer(
        id_user=1,
        username="john_doe",
        password="secure",
        sign_up_date=date(2025, 1, 1),
        phone_number="0606060606"
    )

    address = Address(
        city="Rennes",
        postal_code="35000",
        street_name="Rue de la Galette",
        street_number=12
    )

    order = Order(
        id_order=1,
        customer=customer,
        address=address,
        bundles=[],
        status="pending"
    )

    assert order.id_order == 1
    assert order.customer.username == "john_doe"
    assert order.address.city == "Rennes"
    assert order.status == "pending"
    assert isinstance(order.bundles, list)


def test_order_invalid_customer_type_raises_validationerror():
    address = Address(
        city="Rennes",
        postal_code="35000",
        street_name="Rue de la Galette",
        street_number=12
    )

    # customer invalide (int au lieu d’un objet Customer)
    with pytest.raises(ValidationError):
        Order(
            id_order=1,
            customer=123,
            address=address,
            bundles=[],
            status="pending"
        )
