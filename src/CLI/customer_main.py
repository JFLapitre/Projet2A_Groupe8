# src/CLI/customer_main.py
from typing import TYPE_CHECKING, Dict, List

from src.CLI.session import Session
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle

if TYPE_CHECKING:
    from src.Model.item import Item


class CustomerMainView:
    def __init__(self, session: Session, services: Dict = None):
        self.session = session
        self.services = services or {}
        self.item_service = self.services.get("item")
        self.order_service = self.services.get("order")
        self.address_service = self.services.get("address")  # ✅ ajout du service adresse
        self.cart: List = []

    def display(self):
        while True:
            print("\n=== EJR Eats — Customer Menu ===")
            print("1) Add Item to Order")
            print("2) Check Order")
            print("3) Validate Order")
            print("4) Logout")

            choice = input("Choice: ").strip().lower()
            if choice == "1":
                self.add_item_to_order()
            elif choice == "2":
                self.check_order()
            elif choice == "3":
                self.validate_order()
            elif choice in ("4", "q"):
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    # === Add Item ===
    def add_item_to_order(self):
        while True:
            print("\n1) Regular Bundle")
            print("2) Special Bundle")
            print("3) Single Item")
            print("q) Back")
            choice = input("Choice: ").strip().lower()

            if choice == "1":
                self._choose_regular_bundle()
            elif choice == "2":
                self._choose_special_bundle()
            elif choice == "3":
                self._choose_single_item()
            elif choice == "q":
                return
            else:
                print("Invalid choice.")

    # === Regular Bundle ===
    def _choose_regular_bundle(self):
        try:
            bundles = [
                b
                for b in self.item_service.list_bundles()
                if isinstance(b, DiscountedBundle) and getattr(b, "required_item_types", None)
            ]
        except Exception as e:
            print(f"[ERROR] Cannot fetch bundles: {e}")
            return
        if not bundles:
            print("No regular bundles available.")
            return

        while True:
            print("\n=== Regular Bundles ===")
            for idx, b in enumerate(bundles, start=1):
                print(f"{idx}) {b.name} — {b.discount * 100:.0f}% off")

            choice = input("Select bundle number, q to back: ").strip().lower()
            if choice == "q":
                return

            try:
                idx = int(choice) - 1
                selected_bundle = bundles[idx]
                user_bundle = DiscountedBundle(
                    id_bundle=len(self.cart) + 1,
                    name=selected_bundle.name,
                    discount=selected_bundle.discount,
                    required_item_types=selected_bundle.required_item_types,
                    composition=[],
                )

                for typ in user_bundle.required_item_types:
                    while True:
                        items_of_type = [i for i in self.item_service.list_items() if i.item_type == typ]
                        if not items_of_type:
                            print(f"No items available for type '{typ}'")
                            break
                        print(f"\nChoose an item of type '{typ}':")
                        for j, it in enumerate(items_of_type, start=1):
                            print(f"{j}) {it.name} — {it.price:.2f}€")
                        item_choice = input("Select item number or num+d for description: ").strip().lower()
                        if item_choice.endswith("+d"):
                            idx_item = int(item_choice[:-2]) - 1
                            it = items_of_type[idx_item]
                            if getattr(it, "description", None):
                                print(f"Description: {it.description}")
                            else:
                                print("No description available.")
                            continue
                        idx_item = int(item_choice) - 1
                        user_bundle.composition.append(items_of_type[idx_item])
                        break

                self.cart.append(user_bundle)
                print(f"[SUCCESS] Added '{user_bundle.name}' to cart ({user_bundle.compute_price():.2f}€).")
                return
            except Exception as e:
                print(f"[ERROR] {e}")

    # === Special Bundle ===
    def _choose_special_bundle(self):
        try:
            bundles = [
                b
                for b in self.item_service.list_bundles()
                if isinstance(b, PredefinedBundle) and getattr(b, "composition", None)
            ]
        except Exception as e:
            print(f"[ERROR] Cannot fetch bundles: {e}")
            return
        if not bundles:
            print("No special bundles available.")
            return

        while True:
            print("\n=== Special Bundles ===")
            for idx, b in enumerate(bundles, start=1):
                print(f"{idx}) {b.name} — {b.price:.2f}€")

            choice = input("Select bundle number or num+d for description, q to back: ").strip().lower()
            if choice == "q":
                return

            if choice.endswith("+d"):
                try:
                    idx = int(choice[:-2]) - 1
                    bundle = bundles[idx]
                    print("Descriptions:", bundle.compute_description())
                except Exception as e:
                    print(f"[ERROR] {e}")
                continue

            try:
                idx = int(choice) - 1
                selected_bundle = bundles[idx]
                self.cart.append(selected_bundle)
                print(f"[SUCCESS] Added '{selected_bundle.name}' to cart ({selected_bundle.compute_price():.2f}€).")
                return
            except Exception as e:
                print(f"[ERROR] {e}")

    # === Single Item ===
    def _choose_single_item(self):
        try:
            items = self.item_service.list_items()
            item_types = sorted(set(i.item_type for i in items))
        except Exception as e:
            print(f"[ERROR] Cannot fetch items: {e}")
            return

        while True:
            print("\n=== Item Types ===")
            for idx, t in enumerate(item_types, start=1):
                print(f"{idx}) {t}")
            choice = input("Select item type, q to back: ").strip().lower()
            if choice == "q":
                return
            try:
                idx = int(choice) - 1
                chosen_type = item_types[idx]
                filtered_items = [i for i in items if i.item_type == chosen_type]

                print(f"\n=== Items ({chosen_type}) ===")
                for j, it in enumerate(filtered_items, start=1):
                    print(f"{j}) {it.name} — {it.price:.2f}€")

                while True:
                    item_choice = input("Select item number or num+d for description: ").strip().lower()
                    if item_choice.endswith("+d"):
                        idx_item = int(item_choice[:-2]) - 1
                        it = filtered_items[idx_item]
                        if getattr(it, "description", None):
                            print(f"Description: {it.description}")
                        else:
                            print("No description available.")
                        continue
                    idx_item = int(item_choice) - 1
                    item = filtered_items[idx_item]
                    bundle = OneItemBundle(
                        id_bundle=len(self.cart) + 1,
                        name=item.name,
                        composition=[item],
                    )
                    self.cart.append(bundle)
                    print(f"[SUCCESS] Added '{item.name}' to cart ({bundle.compute_price():.2f}€).")
                    break
                return
            except Exception as e:
                print(f"[ERROR] {e}")

    # === Check Order ===
    def check_order(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        print("\n=== Your Order ===")
        for idx, b in enumerate(self.cart, start=1):
            print(f"{idx}) {b.name} — {b.compute_price():.2f}€ ({b.__class__.__name__})")
        choice = input("Enter number to remove item, or press Enter to return: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.cart):
                removed = self.cart.pop(idx)
                print(f"[INFO] Removed '{removed.name}' from order.")

   # === Validate Order ===
    def validate_order(self):
        if not self.cart:
            print("Your cart is empty.")
            return

        # Demander l'adresse pour chaque commande
        print("\nEnter delivery address details:")
        street_name = input("Street name: ").strip()
        city = input("City: ").strip()
        postal_code = input("Postal code: ").strip()
        street_number = input("Street number: ").strip()

        if not street_name or not city or not postal_code:
            print("[ERROR] Street name, city, and postal code are required.")
            return

        try:
            street_number_int = int(street_number) if street_number else None
            postal_code_int = int(postal_code)

            # Création de l’adresse via AddressService
            address = self.address_service.create_address(
                street_name=street_name,
                city=city,
                postal_code=postal_code_int,
                street_number=street_number_int,
            )

            # Création de la commande avec cette adresse
            created_order = self.order_service.create_order(
                self.session.user_id,
                address.id_address
            )

            # Ajouter tous les bundles du panier à la commande
            for bundle in self.cart:
                self.order_service.add_bundle_to_order(
                    created_order.id_order,
                    bundle.id_bundle
                )

            print(f"[SUCCESS] Order #{created_order.id_order} confirmed with {len(self.cart)} items.")
            self.cart.clear()

        except Exception as e:
            print(f"[ERROR] Cannot confirm order: {e}")

