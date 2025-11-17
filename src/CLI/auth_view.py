# src/CLI/auth_view.py

import logging
from typing import TYPE_CHECKING

from src.CLI.session import Session

if TYPE_CHECKING:
    from src.Service.authentication_service import AuthenticationService


class AuthView:
    def __init__(self, session: Session, services: dict = None):
        """
        Vue CLI pour l'authentification.
        :param session: objet Session pour gérer l'état de l'utilisateur
        :param services: dictionnaire optionnel de services, doit contenir 'auth'
        """
        self.session = session
        if services and "auth" in services:
            self.auth_service: AuthenticationService = services["auth"]
        else:
            raise ValueError("Auth service must be provided in services dictionary.")

    def display(self) -> bool:
        """
        Affiche le menu d'authentification.
        Retourne True si l'utilisateur est connecté, False sinon.
        """
        while True:
            print("\n=== EJR Eats — Authentication ===")
            print("1) Login")
            print("2) Create a Customer account")
            print("q) Back")

            choice = input("Choice: ").strip().lower()
            if choice == "1":
                if self._login():
                    return True
            elif choice == "2":
                if self._register():
                    return True
            elif choice == "q":
                return False
            else:
                print("Invalid choice.")

    # -------------------- LOGIN --------------------

    def _login(self) -> bool:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        try:
            user = self.auth_service.login(username, password)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return False
        except Exception as e:
            logging.exception("Unexpected error during login:")
            print(f"[ERROR] Unexpected error: {e}")
            return False

        if user.__class__.__name__.lower() == "admin":
            print("[INFO] Admins must use the web interface.")
            return False

        # Mise à jour de la session
        self.session.user_id = user.id_user
        self.session.username = user.username
        self.session.role = user.__class__.__name__.lower()
        self.session.user = user

        print(f"[SUCCESS] Logged in as {user.username} ({self.session.role})")
        return True

    # -------------------- REGISTER --------------------

    def _register(self) -> bool:
        print("\n=== Registration ===")
        username = input("Username: ").strip()
        print("Enter a password. Your password must be at least 8 caracters long and have all the caracters' types "
                + "(capital letter, lower letter, digit and special)")
        password = input("Password: ").strip()
        phone_number = input("Phone number: ").strip()

        try:
            user = self.auth_service.register_customer(username, password, phone_number)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return False
        except Exception as e:
            logging.exception("Unexpected error during registration:")
            print(f"[ERROR] Registration failed: {e}")
            return False

        self.session.user_id = user.id_user
        self.session.username = user.username
        self.session.role = user.__class__.__name__.lower()
        self.session.user = user

        print(f"[SUCCESS] Customer '{user.username}' registered successfully.")
        return True
