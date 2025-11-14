from typing import TYPE_CHECKING, Dict, List

# Imports des vues séparées
from src.CLI.customer_address_checkout_view import AddressCheckoutView
from src.CLI.customer_browse_menu_view import BrowseMenuView
from src.CLI.session import Session

if TYPE_CHECKING:
    from src.Model.bundle import Bundle


class CustomerMainView:
    """
    Main CLI view for the customer dashboard, managing the session, the cart,
    and dispatching control to sub-views.
    """

    def __init__(self, session: Session, services: Dict = None):
        """
        Initializes the Customer Main View and its associated sub-views.

        Args:
            session: The active user session.
            services: Dictionary of all available services.
        """
        self.session = session
        self.services = services or {}
        self.cart: List["Bundle"] = []

        # Instantiate sub-views, injecting services, session, and cart
        self.menu_view = BrowseMenuView(self.services, self.cart)
        self.checkout_view = AddressCheckoutView(self.services, self.session, self.cart)

    def display(self):
        """
        Displays the main customer dashboard and handles top-level user selection.
        """
        while True:
            print("\n=== 🛵 EJR Eats — Order Dashboard ===")
            print("1) 🍽️   Browse Menus")
            print("2) 🛒  View Cart")
            print("3) 💳  Validate Order")
            print("B) 🔚  Logout")

            choice = input("Select an option: ").strip().lower()
            if choice == "1":
                self.menu_view.display()
            elif choice == "2":
                self._check_order()
            elif choice == "3":
                self.checkout_view.validate_order()
            elif choice in ("b"):
                print("👋 Logging out...")
                break
            else:
                print("⚠️  Invalid choice, please try again.")

    def _check_order(self):
        """
        Displays the current contents of the customer's cart and allows items removal.
        """
        if not self.cart:
            print("🛒 Your cart is empty.")
            return

        total = sum(b.compute_price() for b in self.cart)
        print("\n=== 🧾 Your Current Cart ===")
        for idx, b in enumerate(self.cart, start=1):
            print(f"{idx}) {b.name} — {b.compute_price():.2f}€")

        print(f"\n💰 Total: {total:.2f}€")

        choice = input("Enter number to remove an item, or B to go back: ").strip().lower()
        if choice.isdigit():
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.cart):
                    removed = self.cart.pop(idx)
                    print(f"🗑️ Removed '{removed.name}' from cart.")
                else:
                    print("⚠️ Invalid item number.")
            except ValueError:
                print("⚠️ Invalid input.")
        elif choice == "b":
            return
