from src.CLI.abstract_view import AbstractView
from src.CLI.auth_view import AuthView


class CustomerMainView(AbstractView):
    def display(self):
        auth_view = AuthView(self.session, self.services)

        # Tant que l'utilisateur n'est pas authentifié, afficher AuthView
        if not self.session.is_authenticated():
            if not auth_view.display():
                return  # L'utilisateur a quitté sans login/registration

        # Menu client
        while True:
            print("\n=== EJR Eats — Customer Menu ===")
            print("1) Browse menu (items & bundles)")
            print("2) Place new order")
            print("3) View my orders")
            print("q) Logout")
            choice = self.prompt("Choice: ")

            if choice == "1":
                self._browse_menu()
            elif choice == "2":
                self._create_order()
            elif choice == "3":
                self._view_orders()
            elif choice.lower() == "q":
                self.session.logout()
                print("Logged out.")
                return
            else:
                self.print_error("Invalid choice.")

    def _browse_menu(self):
        item_service = self.services.get("item")
        print("\n--- Items ---")
        for item in item_service.list_items():
            print(f"#{item.id_item} {item.name} - {item.price}€ ({'✔' if item.availability else '✘'})")

        print("\n--- Bundles ---")
        for b in item_service.list_bundles():
            print(f"#{b.id_bundle} {b.name} - {b.price}€")

    def _create_order(self):
        order_service = self.services.get("order")
        address = self.prompt("Delivery address: ")
        try:
            order = order_service.create_order(customer_id=self.session.user_id, address=address, bundles=[], items=[])
            self.print_info(f"Order #{order['id_order']} created successfully.")
        except Exception as e:
            self.print_error(f"Order creation failed: {e}")

    def _view_orders(self):
        order_service = self.services.get("order")
        try:
            orders = order_service._orders.values() if hasattr(order_service, "_orders") else []
            if not orders:
                print("No orders found.")
                return
            for o in orders:
                print(f"Order #{o['id_order']} - {o['status']}")
        except Exception as e:
            self.print_error(f"Failed to retrieve orders: {e}")


class CustomerMainView(AbstractView):
    def display(self):
        auth_view = AuthView(self.session, self.services)

        # Tant que l'utilisateur n'est pas authentifié, afficher AuthView
        if not self.session.is_authenticated():
            if not auth_view.display():
                return  # L'utilisateur a quitté sans login/registration

        # Menu client
        while True:
            print("\n=== EJR Eats — Customer Menu ===")
            print("1) Browse menu (items & bundles)")
            print("2) Place new order")
            print("3) View my orders")
            print("q) Logout")
            choice = self.prompt("Choice: ")

            if choice == "1":
                self._browse_menu()
            elif choice == "2":
                self._create_order()
            elif choice == "3":
                self._view_orders()
            elif choice.lower() == "q":
                self.session.logout()
                print("Logged out.")
                return
            else:
                self.print_error("Invalid choice.")

    def _browse_menu(self):
        item_service = self.services.get("item")
        print("\n--- Items ---")
        for item in item_service.list_items():
            print(f"#{item.id_item} {item.name} - {item.price}€ ({'✔' if item.availability else '✘'})")

        print("\n--- Bundles ---")
        for b in item_service.list_bundles():
            print(f"#{b.id_bundle} {b.name} - {b.price}€")

    def _create_order(self):
        order_service = self.services.get("order")
        address = self.prompt("Delivery address: ")
        try:
            order = order_service.create_order(customer_id=self.session.user_id, address=address, bundles=[], items=[])
            self.print_info(f"Order #{order['id_order']} created successfully.")
        except Exception as e:
            self.print_error(f"Order creation failed: {e}")

    def _view_orders(self):
        order_service = self.services.get("order")
        try:
            orders = order_service._orders.values() if hasattr(order_service, "_orders") else []
            if not orders:
                print("No orders found.")
                return
            for o in orders:
                print(f"Order #{o['id_order']} - {o['status']}")
        except Exception as e:
            self.print_error(f"Failed to retrieve orders: {e}")
