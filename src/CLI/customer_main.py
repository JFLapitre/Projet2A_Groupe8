from src.CLI.abstract_view import AbstractView
from src.CLI.auth_view import AuthView
from src.CLI.menu_view import MenuView


class CustomerMainView(AbstractView):
    def display(self) -> None:
        # If not logged in, go to AuthView
        if not self.session.is_authenticated():
            AuthView(self.session, self.services).display()

        while True:
            print("\n=== EJR Eats — Customer ===")
            if not self.session.is_authenticated():
                # user pressed back in auth
                AuthView(self.session, self.services).display()
                if not self.session.is_authenticated():
                    return

            print(f"Logged in as: {self.session.username} (id={self.session.user_id})")
            print("1) Browse menu")
            print("2) View cart")
            print("3) Logout")
            print("q) Quit")

            choice = self.prompt("Choice: ")
            if choice == "1":
                MenuView(self.session, self.services).display()
            elif choice == "2":
                # reuse OrderBuilderView
                from src.CLI.order_builder_view import OrderBuilderView

                OrderBuilderView(self.session, self.services).display()
            elif choice == "3":
                self.session.clear()
                self.print_info("Logged out")
                AuthView(self.session, self.services).display()
            elif choice.lower() == "q":
                print("Goodbye!")
                return
            else:
                self.print_error("Invalid choice.")
