# src/CLI/__main__.py
"""
Entrypoint to run the Customer CLI.

Try to import real services from src.init_app; if not present, fallback to minimal fakes.
Run with:
    python -m src.CLI
or
    pdm run python -m src.CLI
"""

from typing import Dict

from src.CLI.customer_main import CustomerMainView
from src.CLI.session import Session


# --- Minimal fake services for local dev if real ones not available ---
class _FakeItemService:
    def __init__(self):
        from dataclasses import dataclass

        @dataclass
        class Item:
            id_item: int
            name: str
            item_type: str
            price: float
            availability: bool = True
            stock: int = 10
            description: str = ""

        @dataclass
        class Bundle:
            id_bundle: int
            name: str
            composition: list
            price: float = None
            discount: float = None

        self._items = [
            Item(1, "Galette-saucisse", "main", 5.0, True, 10, "Local favorite"),
            Item(2, "Breizh-Cola", "drink", 2.0, True, 50, "Soda"),
        ]
        self._bundles = [Bundle(1, "Galette+Drink", [self._items[0], self._items[1]], 6.0, None)]

    def list_items(self):
        return self._items

    def list_bundles(self):
        return self._bundles

    def get_item_details(self, iid):
        return next((i for i in self._items if i.id_item == iid), None)

    def get_bundle_details(self, bid):
        return next((b for b in self._bundles if b.id_bundle == bid), None)


class _FakeOrderService:
    def __init__(self):
        self._next = 1
        self._orders = {}

    def create_order(self, customer_id, address, bundles, items):
        oid = self._next
        self._next += 1
        self._orders[oid] = {
            "id_order": oid,
            "customer": customer_id,
            "address": address,
            "bundles": bundles,
            "items": items,
            "status": "pending",
        }
        return self._orders[oid]


class _FakeAuthService:
    def __init__(self):
        self._users = {}
        self._n = 1

    def register(self, username, password, default_address=None):
        uid = self._n
        self._n += 1
        self._users[username] = {"id": uid, "username": username, "password": password, "address": default_address}
        return self._users[username]

    def login(self, username, password):
        u = self._users.get(username)
        if not u or u["password"] != password:
            raise Exception("Invalid credentials")
        return {"id": u["id"], "username": username, "role": "customer", "token": f"fake-{u['id']}"}


def _build_services() -> Dict:
    # try to import src.init_app for real services
    try:
        import importlib

        init_app = importlib.import_module("src.init_app")
        services = {}
        # user_service
        if hasattr(init_app, "user_service"):
            services["user"] = init_app.user_service
        if hasattr(init_app, "jwt_service"):
            services["auth"] = init_app.jwt_service
        # item/order may not exist in init_app
        if hasattr(init_app, "item_service"):
            services["item"] = init_app.item_service
        if hasattr(init_app, "order_service"):
            services["order"] = init_app.order_service
        # ensure required keys
        if "auth" not in services and "user" not in services:
            raise ImportError("no auth/user in init_app")
        if "item" not in services:
            services["item"] = _FakeItemService()
        if "order" not in services:
            services["order"] = _FakeOrderService()
        return services
    except Exception:
        # fallback to fakes
        return {
            "auth": _FakeAuthService(),
            "item": _FakeItemService(),
            "order": _FakeOrderService(),
            "user": _FakeAuthService(),
        }


def run_cli():
    session = Session()
    services = _build_services()
    view = CustomerMainView(session, services)
    view.display()


if __name__ == "__main__":
    run_cli()
