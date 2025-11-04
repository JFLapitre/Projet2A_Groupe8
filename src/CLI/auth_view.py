import logging

from src.CLI.session import Session
from src.Service.authentication_service import AuthenticationService


class AuthView:
    def __init__(self, session: Session, services: dict = None):
        """
        Vue CLI pour l'authentification.
        :param session: objet Session pour gérer l'état de l'utilisateur
        :param services: dictionnaire optionnel de services, doit contenir 'auth'
        """
        self.session = session
        self.auth_service = services["auth"] if services and "auth" in services else AuthenticationService()

    def display(self):
        """
        Affiche l'interface d'authentification.
        Retourne True si l'utilisateur est maintenant authentifié, False sinon.
        """
        while True:
            print("\n=== EJR Eats — Authentication ===")
            print("1) Login")
            print("2) Create a Customer account")
            print("q) Back")

            choice = input("Choice: ").strip()
            if choice == "1":
                if self._login():
                    return True
            elif choice == "2":
                if self._register():
                    return True
            elif choice.lower() == "q":
                return False
            else:
                print("Invalid choice.")

    def _login(self) -> bool:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        try:
            user = self.auth_service.login(username, password)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return False

        if user.__class__.__name__.lower() == "admin":
            print("[INFO] Admins must use the web API interface (not CLI).")
            return False

        # Met à jour la session
        self.session.user_id = user.id_user
        self.session.username = user.username
        self.session.role = user.__class__.__name__

        print(f"[SUCCESS] Logged in as {user.username} ({user.__class__.__name__})")
        return True

    def _register(self) -> bool:
        print("\n=== Registration ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        try:
            user = self.auth_service.register(username=username, password=password)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Registration failed: {e}")
            return False

        # Met à jour la session avec le nouvel utilisateur
        self.session.user_id = user.id_user
        self.session.username = user.username
        self.session.role = user.__class__.__name__

        print(f"[SUCCESS] Customer '{user.username}' registered successfully.")
        return True
