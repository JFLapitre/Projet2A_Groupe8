from typing import TYPE_CHECKING

from src.CLI.abstract_view import AbstractView
from src.CLI.auth_view import AuthView
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle

if TYPE_CHECKING:
    from src.Model.abstract_bundlebundle import AbstractBundle


class CustomerMainView(AbstractView):
    def display(self):
        auth_view = AuthView(self.session, self.services)

        # Authentification
        if not self.session.is_authenticated():
            if not auth_view.display():
                return

        # Menu principal Customer
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
                self._order_menu()
            elif choice == "3":
                self._view_orders()
            elif choice.lower() == "q":
                self.session.logout()
                print("Logged out.")
                return
            else:
                self.print_error("Invalid choice.")

    # --- Affichage simple de tous les items et bundles ---
    def _browse_menu(self):
        item_service = self.services.get("item")
        print("\n--- Items ---")
        for item in item_service.list_items():
            print(f"#{item.id_item} {item.name} - {item.price}€ ({'✔' if item.availability else '✘'})")

        print("\n--- Bundles ---")
        for b in item_service.list_bundles():
            price = getattr(b, "price", "N/A")
            print(f"#{b.id_bundle} {b.name} - {price}€")

    # --- Menu de prise de commande ---
    def _order_menu(self):
        order_service = self.services.get("order")
        item_service = self.services.get("item")
        cart: list[AbstractBundle] = []

        while True:
            print("\n=== Order Menu ===")
            print("1) Add item / bundle")
            print("2) Check current order")
            print("3) Validate order")
            print("b) Back to main menu")
            choice = self.prompt("Choice: ")

            if choice == "1":
                self._add_bundle(cart, item_service)
            elif choice == "2":
                self._check_order(cart)
            elif choice == "3":
                self._validate_order(cart, order_service)
                if cart:
                    cart.clear()
            elif choice.lower() == "b":
                return
            else:
                self.print_error("Invalid choice.")

    # --- Ajouter un bundle au panier ---
    def _add_bundle(self, cart: list, item_service):
        print("\nSelect bundle type to add:")
        print("1) Discounted Bundle")
        print("2) Special (Predefined) Bundle")
        print("3) Single Item")
        choice = self.prompt("Choice: ")

        bundles = item_service.list_bundles()

        if choice == "1":  # DiscountedBundle
            discounted_bundles = [b for b in bundles if isinstance(b, DiscountedBundle)]
            if not discounted_bundles:
                print("No discounted bundles available.")
                return

            # Affiche les formules disponibles
            formulas = sorted({tuple(b.required_item_types) for b in discounted_bundles})
            print("\nAvailable formulas:")
            for i, f in enumerate(formulas, start=1):
                print(f"{i}) {' / '.join(f)}")
            form_choice = self.prompt("Select a formula: ")
            try:
                selected_formula = formulas[int(form_choice) - 1]
            except (IndexError, ValueError):
                self.print_error("Invalid choice.")
                return

            # Construire le bundle étape par étape
            selected_items = []
            for item_type in selected_formula:
                available_items = [
                    item for item in item_service.list_items() if item.item_type == item_type and item.availability
                ]
                if not available_items:
                    self.print_error(f"No available items for type {item_type}")
                    return
                print(f"\nSelect an item for {item_type}:")
                for i, item in enumerate(available_items, start=1):
                    print(f"{i}) {item.name} - {item.price}€")
                item_choice = self.prompt("Choice: ")
                try:
                    selected_item = available_items[int(item_choice) - 1]
                    selected_items.append(selected_item)
                except (IndexError, ValueError):
                    self.print_error("Invalid choice.")
                    return

            # Créer le DiscountedBundle temporaire pour le panier
            bundle_name = " / ".join([item.name for item in selected_items])
            temp_bundle = DiscountedBundle(
                id_bundle=-1,
                name=bundle_name,
                description="Custom discounted bundle",
                required_item_types=list(selected_formula),
                discount=0.0,
                composition=selected_items,
            )
            cart.append(temp_bundle)
            print(f"Added discounted bundle '{bundle_name}' to your order.")

        elif choice == "2":  # PredefinedBundle
            special_bundles = [b for b in bundles if isinstance(b, PredefinedBundle)]
            self._select_and_add_bundle(special_bundles, cart)

        elif choice == "3":  # OneItemBundle
            single_item_bundles = [b for b in bundles if isinstance(b, OneItemBundle)]
            item_types = sorted({b.composition.item_type for b in single_item_bundles})
            print("\nAvailable item types:")
            for i, t in enumerate(item_types, start=1):
                print(f"{i}) {t}")
            type_choice = self.prompt("Select item type: ")
            try:
                selected_type = item_types[int(type_choice) - 1]
            except (IndexError, ValueError):
                self.print_error("Invalid choice.")
                return
            filtered_bundles = [b for b in single_item_bundles if b.composition.item_type == selected_type]
            self._select_and_add_bundle(filtered_bundles, cart)
        else:
            self.print_error("Invalid choice.")

    # --- Sélectionner un bundle parmi une liste et l'ajouter au panier ---
    def _select_and_add_bundle(self, bundles: list, cart: list):
        if not bundles:
            print("No bundles available.")
            return

        print("\nAvailable bundles:")
        for i, b in enumerate(bundles, start=1):
            price = getattr(b, "price", "N/A")
            print(f"{i}) {b.name} - {price}€")
        choice = self.prompt("Select bundle: ")
        try:
            selected_bundle = bundles[int(choice) - 1]
            cart.append(selected_bundle)
            print(f"Added {selected_bundle.name} to your order.")
        except (IndexError, ValueError):
            self.print_error("Invalid choice.")

    # --- Vérifier et modifier l'ordre en cours ---
    def _check_order(self, cart: list):
        if not cart:
            print("Your order is empty.")
            return
        print("\nCurrent order:")
        for i, b in enumerate(cart, start=1):
            print(f"{i}) {b.name}")
        print("Enter the number of a bundle to remove it, or 'b' to go back.")
        choice = self.prompt("Choice: ")
        if choice.lower() == "b":
            return
        try:
            index = int(choice) - 1
            removed = cart.pop(index)
            print(f"Removed {removed.name} from order.")
        except (IndexError, ValueError):
            self.print_error("Invalid choice.")

    # --- Valider l'ordre et l'envoyer au service ---
    def _validate_order(self, cart: list, order_service):
        if not cart:
            print("Cannot validate empty order.")
            return
        address = self.prompt("Delivery address: ")
        try:
            order = order_service.create_order(
                customer_id=self.session.user_id, address=address, bundles=cart, items=[]
            )
            print(f"Order #{order['id_order']} created successfully!")
        except Exception as e:
            self.print_error(f"Failed to validate order: {e}")

    # --- Afficher les commandes du client ---
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
