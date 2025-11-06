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
        self.address_service = self.services.get("address")
        self.cart: List = []

    # === MAIN MENU ===
    def display(self):
        while True:
            print("\n=== 🛵 EJR Eats — Order Dashboard ===")
            print("1) 🍽️   Browse Menus")
            print("2) 🛒  View Cart")
            print("3) 💳  Validate Order")
            print("B) 🔚  Logout")

            choice = input("Select an option: ").strip().lower()
            if choice == "1":
                self.add_item_to_order()
            elif choice == "2":
                self.check_order()
            elif choice == "3":
                self.validate_order()
            elif choice in ("B", "b"):
                print("👋 Logging out...")
                break
            else:
                print("⚠️ Invalid choice, please try again.")

    # === ADD ITEM MENU ===
    def add_item_to_order(self):
        while True:
            print("\n=== 🍔 Choose a Menu Type ===")
            print("1) 🏷️  Discounted Bundle")
            print("2) ⭐ Special Bundle")
            print("3) 🧃 Single Item")
            print("B) Back")
            choice = input("Select an option: ").strip().lower()

            if choice == "1":
                self._choose_discounted_bundle()
            elif choice == "2":
                self._choose_special_bundle()
            elif choice == "3":
                self._choose_single_item()
            elif choice == "b":
                return
            else:
                print("⚠️ Invalid choice.")

    # === DISCOUNTED BUNDLE ===
    def _choose_discounted_bundle(self):
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
            print("No discounted bundles available.")
            return

        while True:
            print("\n=== 🏷️ Discounted Bundles ===")
            for idx, b in enumerate(bundles, start=1):
                # On affiche seulement le nom et le pourcentage ici — pas de prix avant sélection
                print(f"{idx}) {b.name} — {b.discount * 100:.0f}% off")

            choice = input("Select bundle number or B to back: ").strip().lower()
            if choice == "b":
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

                # Sélectionner un item pour chaque type requis
                for typ in user_bundle.required_item_types:
                    while True:
                        items_of_type = [i for i in self.item_service.list_items() if i.item_type == typ]
                        if not items_of_type:
                            print(f"No items available for type '{typ}'")
                            break

                        print(f"\nChoose an item of type '{typ}':")
                        for j, it in enumerate(items_of_type, start=1):
                            print(
                                f"{j}) {it.name} — {it.price * (1 - user_bundle.discount):.2f}€ (Instead of {it.price:.2f}€)"
                            )

                        item_choice = input("Select number or B to back: ").strip().lower()
                        if item_choice == "b":
                            return

                        idx_item = int(item_choice) - 1
                        chosen_item = items_of_type[idx_item]
                        user_bundle.composition.append(chosen_item)

                        # Après chaque choix, afficher le prix original courant et le prix réduit
                        current_original = sum(it.price for it in user_bundle.composition)
                        current_discounted = current_original * (1 - user_bundle.discount)
                        print(
                            f"Current selection subtotal: {current_original:.2f}€ -> "
                            f"{current_discounted:.2f}€ (~~{current_original:.2f}€~~, {user_bundle.discount * 100:.0f}% off)"
                        )
                        break

                # Après avoir rempli tous les types requis, afficher récapitulatif prix final
                original_price = sum(it.price for it in user_bundle.composition)
                discounted_price = original_price * (1 - user_bundle.discount)
                print(
                    f"\nFinal price for '{user_bundle.name}': {discounted_price:.2f}€ "
                    f"(~~{original_price:.2f}€~~, {user_bundle.discount * 100:.0f}% off)"
                )

                self.cart.append(user_bundle)
                print(f"✅ Added '{user_bundle.name}' — {user_bundle.compute_price():.2f}€")
                return

            except Exception as e:
                print(f"[ERROR] {e}")

    # === SPECIAL BUNDLE ===
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
            print("\n=== ⭐ Special Bundles ===")
            for idx, b in enumerate(bundles, start=1):
                print(f"{idx}) {b.name} — {b.price:.2f}€")

            choice = input("Select a bundle number or B to back: ").strip().lower()
            if choice == "b":
                return

            try:
                idx = int(choice) - 1
                selected_bundle = bundles[idx]
                self.cart.append(selected_bundle)
                print(f"✅ Added '{selected_bundle.name}' — {selected_bundle.compute_price():.2f}€")
                return
            except Exception as e:
                print(f"[ERROR] {e}")

    # === SINGLE ITEM ===
    def _choose_single_item(self):
        try:
            items = self.item_service.list_items()
            item_types = sorted(set(i.item_type for i in items))
        except Exception as e:
            print(f"[ERROR] Cannot fetch items: {e}")
            return

        while True:
            print("\n=== 🧃 Item Categories ===")
            for idx, t in enumerate(item_types, start=1):
                print(f"{idx}) {t}")
            choice = input("Select a category or B to back: ").strip().lower()
            if choice == "b":
                return
            try:
                idx = int(choice) - 1
                chosen_type = item_types[idx]
                filtered_items = [i for i in items if i.item_type == chosen_type]

                print(f"\n=== Items — {chosen_type} ===")
                for j, it in enumerate(filtered_items, start=1):
                    print(f"{j}) {it.name} — {it.price:.2f}€")

                while True:
                    item_choice = input("Select item number or B to back: ").strip().lower()
                    if item_choice == "b":
                        return
                    idx_item = int(item_choice) - 1
                    item = filtered_items[idx_item]
                    bundle = OneItemBundle(
                        id_bundle=len(self.cart) + 1,
                        name=item.name,
                        composition=[item],
                    )
                    self.cart.append(bundle)
                    print(f"✅ Added '{item.name}' — {bundle.compute_price():.2f}€")
                    return
            except Exception as e:
                print(f"[ERROR] {e}")

    # === CHECK ORDER ===
    def check_order(self):
        if not self.cart:
            print("🛒 Your cart is empty.")
            return

        total = sum(b.compute_price() for b in self.cart)
        print("\n=== 🧾 Your Current Cart ===")
        for idx, b in enumerate(self.cart, start=1):
            print(f"{idx}) {b.name} — {b.compute_price():.2f}€ ({b.__class__.__name__})")
        print(f"\n💰 Total: {total:.2f}€")
        choice = input("Enter number to remove an item, or B to go back: ").strip().lower()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.cart):
                removed = self.cart.pop(idx)
                print(f"🗑️ Removed '{removed.name}' from cart.")
        elif choice == "b":
            return

    # === VALIDATE ORDER ===
    def validate_order(self):
        if not self.cart:
            print("🛒 Your cart is empty.")
            return

        total = sum(b.compute_price() for b in self.cart)
        print("\n=== 💳 Review Your Order ===")
        for b in self.cart:
            print(f"- {b.name}: {b.compute_price():.2f}€")
            if hasattr(b, "composition") and b.composition:
                for item in b.composition:
                    print(f"    • {item.name}")
        print(f"\n💰 Total to pay: {total:.2f}€")

        confirm = input("Proceed to checkout? (Y/N): ").strip().lower()
        if confirm != "y":
            print("Order cancelled.")
            return

        print("\n📦 Enter delivery address:")
        street_name = input("Street name: ").strip()
        city = input("City: ").strip()
        postal_code_input = input("Postal code: ").strip()
        street_number_input = input("Street number: ").strip()

        if not street_name or not city or not postal_code_input:
            print("[ERROR] Street name, city, and postal code are required.")
            return

        try:
            postal_code = int(postal_code_input)
            street_number = street_number_input if street_number_input else None

            address = self.address_service.create_address(
                street_name=street_name,
                city=city,
                postal_code=postal_code,
                street_number=street_number,
            )

            created_order = self.order_service.create_order(self.session.user_id, address.id_address)
            for bundle in self.cart:
                self.order_service.add_bundle_to_order(created_order.id_order, bundle)

            print(f"\n🎉 Order #{created_order.id_order} confirmed!")
            print(f"🧾 Total: {total:.2f}€ — {len(self.cart)} items delivered to {street_name}, {city}.")
            self.cart.clear()

        except Exception as e:
            print(f"[ERROR] Cannot confirm order: {e}")
