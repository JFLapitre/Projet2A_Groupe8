# src/CLI/__main__.py

from typing import Dict

from src.CLI.auth_view import AuthView
from src.CLI.customer_main_view import CustomerMainView
from src.CLI.session import Session
from src.CLI.driver_main_view import DriverMainView

def _build_services() -> Dict:
    """Charge les vrais services depuis src.init_app"""
    try:
        import importlib

        init_app = importlib.import_module("src.init_app")

        services = {
            "auth": getattr(init_app, "auth_service", None),
            "item": getattr(init_app, "item_service", None),
            "order": getattr(init_app, "order_service", None),
            "delivery": getattr(init_app, "delivery_service", None),
            "user": getattr(init_app, "admin_user_service", None),
            "jwt": getattr(init_app, "jwt_service", None),
            "address": getattr(init_app, "address_service", None),
            "driver": getattr(init_app, "driver_service", None),
        }

        # Vérifie s’il en manque
        missing = [k for k, v in services.items() if v is None]
        if missing:
            print(f"[WARN] Some services missing: {', '.join(missing)}")

        return services

    except Exception as e:
        print(f"[ERROR] Failed to import real services: {e}")
        raise


def run_cli():
    """Lance le CLI complet (auth + menus)."""
    session = Session()
    services = _build_services()

    # Étape 1 — Authentification
    auth_view = AuthView(session, services)
    authenticated = auth_view.display()
    if not authenticated:
        print("Goodbye.")
        return

    if session.role == "customer":
        view = CustomerMainView(session, services)
        view.display()

    if session.role == "driver":
        view = DriverMainView(session, services)
        view.display()



if __name__ == "__main__":
    run_cli()
