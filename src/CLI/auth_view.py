from typing import Any

from src.CLI.abstract_view import AbstractView
from src.CLI.session import Session


class AuthView(AbstractView):
    """
    Login / register view. Tries to call realistic methods on provided services:
    - auth service: .login(username,password) or .authenticate(...)
    - user service: .register_customer(...) or .create_user(...)
    """

    def display(self) -> None:
        while True:
            print("\n=== EJR Eats — Authentication ===")
            print("1) Login")
            print("2) Register")
            print("q) Back")
            choice = self.prompt("Choice: ")
            if choice == "1":
                self._login()
                if self.session.is_authenticated():
                    return
            elif choice == "2":
                self._register()
            elif choice.lower() == "q":
                return
            else:
                self.print_error("Invalid choice.")

    def _login(self) -> None:
        username = self.prompt("Username: ")
        password = self.prompt("Password: ")
        auth = self.services.get("auth")
        user_srv = self.services.get("user")

        # First try auth service generic login
        try:
            if auth:
                if hasattr(auth, "login"):
                    user = auth.login(username, password)
                elif hasattr(auth, "authenticate"):
                    user = auth.authenticate(username, password)
                else:
                    raise RuntimeError("Auth service doesn't implement login/authenticate")
            elif user_srv:
                # fallback to user service login names
                if hasattr(user_srv, "login_customer"):
                    user = user_srv.login_customer(username, password)
                elif hasattr(user_srv, "validate_username_password"):
                    # some projects keep validate_username_password as function in utils; it returns user
                    user = user_srv.validate_username_password(username, password)
                else:
                    raise RuntimeError("No usable auth/user service found")
            else:
                raise RuntimeError("No auth/user service provided")
        except Exception as e:
            self.print_error(f"Login failed: {e}")
            return

        # normalize expected return types (dict or object)
        if isinstance(user, dict):
            self.session.user_id = user.get("id") or user.get("user_id") or user.get("id_user")
            self.session.username = user.get("username")
            self.session.role = user.get("role", "customer")
            self.session.token = user.get("token")
        else:
            # object with attributes
            self.session.user_id = getattr(user, "id", None) or getattr(user, "id_user", None)
            self.session.username = getattr(user, "username", None)
            self.session.role = getattr(user, "role", "customer")
            # JWT token optional
            self.session.token = getattr(user, "token", None)

        if self.session.is_authenticated():
            self.print_info(f"Welcome {self.session.username}!")
        else:
            self.print_error("Login succeeded but user id couldn't be resolved.")

    def _register(self) -> None:
        username = self.prompt("Choose username: ")
        password = self.prompt("Choose password: ")
        default_address = self.prompt("Default address (optional): ")

        user_srv = self.services.get("user")
        auth = self.services.get("auth")
        try:
            if user_srv:
                # try common register methods
                if hasattr(user_srv, "register_customer"):
                    user_srv.register_customer(username=username, password=password, default_address=default_address)
                elif hasattr(user_srv, "create_user"):
                    user_srv.create_user(username=username, password=password)
                else:
                    # fallback to auth service
                    raise RuntimeError("User service has no register method")
            elif auth and hasattr(auth, "register"):
                auth.register(id=username, name=username, password=password, default_address=default_address)
            else:
                raise RuntimeError("No service to register user")
            self.print_info("Account created. You can now login.")
        except Exception as e:
            self.print_error(f"Registration failed: {e}")
