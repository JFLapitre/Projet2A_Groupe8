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
        self.auth_service = self.services.get("auth")
        self.available_items: List[Item] = []
        self.cart: List = []

    def display(self):
        while True:
            print("\n=== EJR Eats — Customer Menu ===")
            print("1) View items")
            print("2) Create a bundle")
            print("3) View cart")
            print("4) Confirm order")
            print("q) Logout")

            choice = input("Choice: ").strip().lower()

            if choice == "1":
                self.show_items()
            elif choice == "2":
                self.create_bundle()
            elif choice == "3":
                self.show_cart()
            elif choice == "4":
                self.confirm_order()
            elif choice == "q":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def show_items(self):
        try:
            self.available_items = self.item_service.list_items()
        except Exception as e:
            print(f"[ERROR] Cannot fetch items: {e}")
            return

        if not self.available_items:
            print("No items available.")
            return

        print("\n=== Available Items ===")
        for item in self.available_items:
            print(f"{item.id_item}) {item.name} — {item.price:.2f}€ ({item.item_type})")

        try:
            bundles = self.item_service.list_bundles()
            if bundles:
                print("\n=== Available Bundles ===")
                for b in bundles:
                    price = getattr(b, "price", None)
                    name = getattr(b, "name", "Unknown Bundle")
                    print(f"{getattr(b, 'id_bundle', '?')}) {name} — {price if price is not None else 'N/A'}€")
        except Exception as e:
            print(f"[ERROR] Cannot fetch bundles: {e}")

    def create_bundle(self):
        """Menu création de bundle CLI"""
        if not self.available_items:
            self.show_items()
        print("\n1) One Item Bundle\n2) Predefined Bundle\n3) Discounted Bundle\nq) Back")
        choice = input("Choice: ").strip().lower()
        if choice == "1":
            self._create_one_item_bundle()
        elif choice == "2":
            self._create_predefined_bundle()
        elif choice == "3":
            self._create_discounted_bundle()
        elif choice == "q":
            return
        else:
            print("Invalid choice.")

    def _create_one_item_bundle(self):
        self.show_items()
        try:
            item_id = int(input("Select item ID: ").strip())
            item = next(i for i in self.available_items if i.id_item == item_id)
            bundle = OneItemBundle(id_bundle=item.id_item, name=item.name, composition=[item])
            self.cart.append(bundle)
            print(f"[SUCCESS] Added {item.name} to cart ({bundle.compute_price():.2f}€).")
        except Exception as e:
            print(f"[ERROR] {e}")

    def _create_predefined_bundle(self):
        self.show_items()
        ids = input("Enter item IDs separated by commas: ").strip().split(",")
        try:
            selected_items = [i for i in self.available_items if str(i.id_item) in ids]
            price = sum(i.price for i in selected_items) * 0.95
            bundle = PredefinedBundle(
                id_bundle=len(self.cart) + 1, name="Predefined Bundle", composition=selected_items, price=price
            )
            self.cart.append(bundle)
            print(f"[SUCCESS] Added Predefined Bundle ({bundle.compute_price():.2f}€).")
        except Exception as e:
            print(f"[ERROR] {e}")

    def _create_discounted_bundle(self):
        self.show_items()
        ids = input("Enter item IDs separated by commas: ").strip().split(",")
        discount = float(input("Enter discount (0.1 for 10%): ").strip())
        try:
            selected_items = [i for i in self.available_items if str(i.id_item) in ids]
            required_item_types = list({i.item_type for i in selected_items})
            bundle = DiscountedBundle(
                id_bundle=len(self.cart) + 1,
                name="Discounted Bundle",
                composition=selected_items,
                required_item_types=required_item_types,
                discount=discount,
            )
            self.cart.append(bundle)
            print(f"[SUCCESS] Added Discounted Bundle ({bundle.compute_price():.2f}€).")
        except Exception as e:
            print(f"[ERROR] {e}")

    def show_cart(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        print("\n=== Your Cart ===")
        total = 0
        for b in self.cart:
            price = b.compute_price()
            total += price
            print(f"- {b.name} ({b.__class__.__name__}): {price:.2f}€")
        print(f"Total: {total:.2f}€")

    def confirm_order(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        try:
            self.order_service.create_order(self.session.user_id, self.cart)
            print("[SUCCESS] Order confirmed.")
            self.cart.clear()
        except Exception as e:
            print(f"[ERROR] Cannot confirm order: {e}")
