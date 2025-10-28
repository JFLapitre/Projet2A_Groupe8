from datetime import date

import pytest
from pydantic_core import ValidationError

from src.Model.address import Address
from src.Model.customer import Customer
from src.Model.delivery import Delivery
from src.Model.driver import Driver
from src.Model.order import Order


def test_delivery_constructor_ok():
    customer = Customer(
        id_user=1,
        username="john_doe",
        password="secure",
        sign_up_date=date(2025, 1, 1),
        phone_number="0606060606"
    )

    driver = Driver(
        id_user=2,
        username="driver_1",
        password="strong_pwd",
        sign_up_date=date(2025, 1, 2),
        name="Jean Dupont",
        phone_number="0610101010",
        vehicle_type="bike",
        availability=True
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

    delivery = Delivery(
        id_delivery=1,
        driver=driver,
        orders=[order],
        status="in_progress",
        delivery_time=date(2025, 1, 2)
    )

    assert delivery.id_delivery == 1
    assert delivery.driver.name == "Jean Dupont"
    assert delivery.orders[0].customer.username == "john_doe"
    assert delivery.status == "in_progress"
    assert isinstance(delivery.delivery_time, date)


def test_delivery_invalid_driver_type_raises_validationerror():
    customer = Customer(
        id_user=1,
        username="john_doe",
        password="secure",
        sign_up_date=date(2025, 1, 1),
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

    # driver invalide (chaîne au lieu d’un objet Driver)
    with pytest.raises(ValidationError):
        Delivery(
            id_delivery=1,
            driver="invalid_driver",
            orders=[order],
            status="in_progress",
            delivery_time=date(2025, 1, 2)
        )
