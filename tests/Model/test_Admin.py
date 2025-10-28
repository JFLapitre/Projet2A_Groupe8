from datetime import date

import pytest
from pydantic_core import ValidationError

from src.Model.address import Address
from src.Model.admin import Admin
from src.Model.customer import Customer
from src.Model.item import Item
from src.Model.order import Order


def test_admin_constructor_ok():
    # Création d’un client validepdm run pytest src/tests/Model
    customer = Customer(
        id_user=1,
        username="john_doe",
        password="secret",
        sign_up_date=date.today(),
        phone_number="0606060606",
    )

    # Création d’une adresse valide
    address = Address(
        id_address=1, street_name="Rue de la Galette", street_number="7", city="Rennes", postal_code="35000"
    )

    # Création d’un item
    item = Item(id_item=1, name="Burger", item_type="main", price=5.0)

    # Création d’une commande valide
    order = Order(
        id_order=1,
        customer=customer,
        address=address,
        bundles=[],
        status="pending",
    )

    # Création d’un admin avec la commande dans la file
    admin = Admin(
        id_user=1,
        username="admin",
        password="secure",
        sign_up_date=None,
        adress="EJR HQ",
        queue=[order],
    )

    assert admin.id_user == 1
    assert admin.username == "admin"
    assert admin.adress == "EJR HQ"
    assert isinstance(admin.queue, list)
    assert admin.queue[0].status == "pending"
    assert admin.queue[0].address.city == "Rennes"


def test_admin_invalid_id_raises_validationerror():
    # Création d’un client valide
    customer = Customer(
        id_user=1,
        username="john_doe",
        password="secret",
        sign_up_date=date.today(),
    )

    # Création d’une adresse valide
    address = Address(
        id_address=1, street_name="Rue de la Galette", street_number=7, city="Rennes", postal_code="35000"
    )

    # Création d’une commande valide
    order = Order(
        id_order=1,
        customer=customer,
        address=address,
        bundles=[],
        status="pending",
    )

    # id_user invalide (chaîne au lieu d’un entier)
    with pytest.raises(ValidationError):
        Admin(
            id_user="one",
            username="admin",
            password="secure",
            sign_up_date=None,
            adress="EJR HQ",
            queue=[order],
        )
