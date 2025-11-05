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
        self.available_items: List["Item"] = []
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
            elif choice == "4" or choice == "q":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    # === 1) Add item to order ===
    def add_item_to_order(self):
        while True:
            print("\n1) Discounted Bundle")
            print("2) Special Bundle")
            print("3) Single Item")
            print("q) Back")
            choice = input("Choice: ").strip().lower()

            if choice == "1":
                self._choose_discounted_bundle()
            elif choice == "2":
                self._choose_predefined_bundle()
            elif choice == "3":
                self._choose_single_item()
            elif choice == "q":
                return
            else:
                print("Invalid choice.")

    def _choose_predefined_bundle(self):
        try:
            bundles = self.item_service.list_bundles()
            regular_bundles = [b for b in bundles if isinstance(b, PredefinedBundle)]
        except Exception as e:
            print(f"[ERROR] Cannot fetch bundles: {e}")
            return

        if not regular_bundles:
            print("No regular bundles available.")
            return

        print("\n=== Regular Bundles ===")
        for idx, b in enumerate(regular_bundles, start=1):
            print(f"{idx}) {b.name} — {b.price:.2f}€")

        try:
            idx = int(input("Select bundle number: ").strip()) - 1
            selected_bundle = regular_bundles[idx]

            # User chooses items matching required types
            chosen_items = []
            for req_type in {i.item_type for i in selected_bundle.composition}:
                items_of_type = [i for i in self.item_service.list_items() if i.item_type == req_type]
                print(f"\nChoose an item of type '{req_type}':")
                for j, it in enumerate(items_of_type, start=1):
                    print(f"{j}) {it.name} — {it.price:.2f}€")
                choice = int(input("Choice: ").strip()) - 1
                chosen_items.append(items_of_type[choice])

            new_bundle = PredefinedBundle(
                id_bundle=len(self.cart) + 1,
                name=selected_bundle.name,
                composition=chosen_items,
                price=sum(i.price for i in chosen_items),
                availability=True,
            )
            self.cart.append(new_bundle)
            print(f"[SUCCESS] Added '{new_bundle.name}' to cart.")
        except Exception as e:
            print(f"[ERROR] {e}")

    def _choose_discounted_bundle(self):
        try:
            bundles = self.item_service.list_bundles()
            special_bundles = [b for b in bundles if isinstance(b, DiscountedBundle)]
        except Exception as e:
            print(f"[ERROR] Cannot fetch bundles: {e}")
            return

        if not special_bundles:
            print("No special bundles available.")
            return

        print("\n=== Special Bundles ===")
        for idx, b in enumerate(special_bundles, start=1):
            print(f"{idx}) {b.name} — -({b.discount * 100}%)")

        try:
            idx = int(input("Select bundle number: ").strip()) - 1
            bundle = special_bundles[idx]
            self.cart.append(bundle)
            print(f"[SUCCESS] Added '{bundle.name}' to cart.")
        except Exception as e:
            print(f"[ERROR] {e}")

    def _choose_single_item(self):
        try:
            items = self.item_service.list_items()
            item_types = sorted(set(i.item_type for i in items))
        except Exception as e:
            print(f"[ERROR] Cannot fetch items: {e}")
            return

        print("\n=== Item Types ===")
        for idx, t in enumerate(item_types, start=1):
            print(f"{idx}) {t}")
        try:
            idx = int(input("Select item type: ").strip()) - 1
            chosen_type = item_types[idx]
            filtered_items = [i for i in items if i.item_type == chosen_type]

            print(f"\n=== Items ({chosen_type}) ===")
            for j, it in enumerate(filtered_items, start=1):
                print(f"{j}) {it.name} — {it.price:.2f}€")
            item_idx = int(input("Select item: ").strip()) - 1
            item = filtered_items[item_idx]

            bundle = OneItemBundle(id_bundle=len(self.cart) + 1, name=item.name, composition=item)
            self.cart.append(bundle)
            print(f"[SUCCESS] Added '{item.name}' to cart ({bundle.compute_price():.2f}€).")
        except Exception as e:
            print(f"[ERROR] {e}")

    # === 2) Check order ===
    def check_order(self):
        if not self.cart:
            print("Your cart is empty.")
            return

        print("\n=== Your Order ===")
        total = 0
        for idx, b in enumerate(self.cart, start=1):
            price = b.compute_price()
            total += price
            print(f"{idx}) {b.name} — {price:.2f}€ ({b.__class__.__name__})")

        print(f"Total: {total:.2f}€")
        print("Enter number to remove item, or press Enter to return.")
        choice = input("Choice: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.cart):
                removed = self.cart.pop(idx)
                print(f"[INFO] Removed '{removed.name}' from order.")

    # === 3) Validate order ===
    def validate_order(self):
        if not self.cart:
            print("Your cart is empty.")
            return

        address = input("Enter delivery address: ").strip()
        if not address:
            print("[ERROR] Address required.")
            return

        try:
            self.order_service.create_order(self.session.user_id, self.cart, address)
            print("[SUCCESS] Order confirmed.")
            self.cart.clear()
        except Exception as e:
            print(f"[ERROR] Cannot confirm order: {e}")
