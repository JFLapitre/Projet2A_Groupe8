from datetime import date

import pytest
from pydantic_core import ValidationError

from src.Model.abstract_user import AbstractUser


class DummyUser(AbstractUser):
    role: str = "tester"


def test_dummy_user_inherits_abstract_user_fields():
    user = DummyUser(
        id_user=1,
        username="test_user",
        password="secure",
        sign_up_date=str(date.today()),
        role="tester",
    )
    assert user.id_user == 1
    assert user.username == "test_user"
    assert user.role == "tester"


def test_dummy_user_invalid_id_raises_validationerror():
    with pytest.raises(ValidationError):
        DummyUser(
            id_user="invalid",
            username="x",
            password="y",
            sign_up_date=str(date.today()),
            role="tester",
        )
