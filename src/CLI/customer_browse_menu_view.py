import logging
from typing import TYPE_CHECKING, Dict, List, Optional

from src.Model.discounted_bundle import DiscountedBundle
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle

if TYPE_CHECKING:
    from src.Model.bundle import Bundle
    from src.Service.item_service import ItemService

    from src.Model.item import Item


class BrowseMenuView:
    """
    Handles all menu browsing and item selection logic for the customer.
    """

    def __init__(self, services: Dict, cart: List["Bundle"]):
        """
        Initializes the Browse Menu View.
        """
        self.item_service: "ItemService" = services.get("item")
        self.cart = cart
        self.all_items: Optional[List["Item"]] = None

    def display(self):
        """
        Displays the top-level menu types (Discounted, Special, Single Item)
        and dispatches to the corresponding selection methods.
        """
        while True:
            print("\n=== 🍔 Choose a Menu Type ===")
            print("1) 🏷️   Discounted Bundle")
            print("2) ⭐  Special Bundle")
            print("3) 🧃  Single Item")
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

    def _show_item_description_if_requested(self, choice: str, available_items: List["Item"]) -> bool:
        """
        Checks if the choice is a request for item description (e.g., '1D', '2+D') and displays it.

        Returns:
            bool: True if a description was handled, False otherwise.
        """
        if choice.lower().endswith(("d", "+d")):
            num_str = choice[:-1].rstrip(" +").strip()
            if num_str.isdigit():
                try:
                    item_idx = int(num_str) - 1
                    item = available_items[item_idx]
                    desc = item.description or "No description available."
                    print(f"   ℹ️ {item.name} description: {desc}")
                    return True
                except IndexError:
                    print("⚠️ Invalid item number for description.")
                    return True
                except Exception as e:
                    logging.error(f"Error displaying description: {e}")
                    print("[ERROR] An unexpected error occurred.")
                    return True
            else:
                print("⚠️ Invalid format for description request.")
                return True
        return False

    def _add_bundle_to_cart(self, bundle: "Bundle"):
        """
        Adds the selected bundle (or item, acting as a bundle) to the cart and confirms.
        """
        self.cart.append(bundle)
        print(f"✅ Added '{bundle.name}' — {bundle.compute_price():.2f}€")

    def _select_item_for_type(
        self, required_type: str, available_items: List["Item"], user_bundle: DiscountedBundle
    ) -> bool:
        """
        Handles the loop for selecting a single item of a specific required type.

        Returns:
            bool: True if an item was successfully selected, False if the process was cancelled.
        """
        while True:
            print(f"\n- Select your {required_type} (Enter Number+D to get item description):")
            for idx_item, item in enumerate(available_items, start=1):
                print(f"   {idx_item}) {item.name} - {(1 - user_bundle.discount) * item.price:.2f}€")

            item_choice = input(f"Choice for {required_type}: ").strip()

            if self._show_item_description_if_requested(item_choice, available_items):
                continue

            try:
                item_idx = int(item_choice) - 1
                if 0 <= item_idx < len(available_items):
                    selected_item = available_items[item_idx]
                    user_bundle.composition.append(selected_item)
                    print(f"   ✅ Added {selected_item.name}.")
                    return True  # Success
                else:
                    print("⚠️ Invalid item number.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a number or number+d.")
            except Exception as e:
                logging.error(f"Error during item selection: {e}")
                print("[ERROR] An unexpected error occurred.")
                return False

        return False

    def _configure_discounted_bundle(self, selected_bundle: DiscountedBundle) -> Optional[DiscountedBundle]:
        """
        Guides the user through selecting items for all required types of the bundle.

        Returns:
            Optional[DiscountedBundle]: The fully configured bundle or None if cancelled/failed.
        """
        user_bundle = DiscountedBundle(
            id_bundle=len(self.cart) + 1,
            name=selected_bundle.name,
            discount=selected_bundle.discount,
            required_item_types=selected_bundle.required_item_types,
            composition=[],
        )

        if self.all_items is None:
            self.all_items = self.item_service.list_items()

        for required_type in user_bundle.required_item_types:
            available_items = [i for i in self.all_items if i.item_type == required_type]

            if not available_items:
                print(f"[ERROR] No items available for type: {required_type}. Bundle cancelled.")
                return None

            if not self._select_item_for_type(required_type, available_items, user_bundle):
                return None

        return user_bundle

    def _choose_discounted_bundle(self):
        """
        Allows the user to select and configure a discounted bundle (dynamic composition).
        """
        try:
            bundles = [
                b
                for b in self.item_service.list_bundles()
                if isinstance(b, DiscountedBundle) and getattr(b, "required_item_types", None)
            ]
        except Exception as e:
            logging.error(f"Cannot fetch discounted bundles: {e}")
            print("[ERROR] Cannot fetch bundles.")
            return

        if not bundles:
            print("No discounted bundles available.")
            return

        while True:
            print("\n=== 🏷️ Discounted Bundles ===")
            for idx, b in enumerate(bundles, start=1):
                print(f"{idx}) {b.name} — {b.discount * 100:.0f}% off")

            choice = input("Select bundle number or B to back: ").strip().lower()
            if choice == "b":
                return

            try:
                idx = int(choice) - 1
                selected_bundle = bundles[idx]

                print(f"\n[INFO] Starting configuration for '{selected_bundle.name}'.")

                user_bundle = self._configure_discounted_bundle(selected_bundle)

                if user_bundle:
                    self._add_bundle_to_cart(user_bundle)
                    return

            except (ValueError, IndexError):
                print("⚠️ Invalid choice.")
            except Exception as e:
                logging.error(f"Error selecting discounted bundle: {e}")
                print(f"[ERROR] Invalid choice or configuration error: {e}")

    def _handle_predefined_description(self, choice: str, bundles: List["PredefinedBundle"]) -> bool:
        """
        Checks if the choice is a request for bundle description (e.g., '1D', '2+D') and displays it.
        """
        if choice.lower().endswith(("d", "+d")):
            num_str = choice[:-1].rstrip(" +").strip()
            if num_str.isdigit():
                try:
                    idx = int(num_str) - 1
                    selected_bundle = bundles[idx]
                    desc = selected_bundle.compute_description()
                    print(f"   ℹ️ {selected_bundle.name} description:")
                    print(f"   {desc}")
                    return True
                except (ValueError, IndexError):
                    print("⚠️ Invalid bundle number for description.")
                    return True
                except Exception as e:
                    logging.error(f"Error computing bundle description: {e}")
                    print("[ERROR] Failed to get bundle description.")
                    return True
            else:
                print("⚠️ Invalid format for description request.")
                return True
        return False

    def _choose_special_bundle(self):
        """
        Allows the user to select a predefined special bundle.
        """
        try:
            bundles = [
                b
                for b in self.item_service.list_bundles()
                if isinstance(b, PredefinedBundle) and getattr(b, "composition", None)
            ]
        except Exception as e:
            logging.error(f"Cannot fetch special bundles: {e}")
            print("[ERROR] Cannot fetch bundles.")
            return
        if not bundles:
            print("No special bundles available.")
            return

        while True:
            print("\n=== ⭐ Special Bundles ===")
            for idx, b in enumerate(bundles, start=1):
                print(f"{idx}) {b.name} — {b.price:.2f}€")

            choice = input("Select a bundle number, number+D for description, or B to back: ").strip()

            if self._handle_predefined_description(choice, bundles):
                continue

            if choice.lower() == "b":
                return

            try:
                idx = int(choice) - 1
                selected_bundle = bundles[idx]
                self._add_bundle_to_cart(selected_bundle)
                return
            except (ValueError, IndexError):
                print("⚠️ Invalid bundle number.")
            except Exception as e:
                logging.error(f"Error selecting special bundle: {e}")
                print(f"[ERROR] {e}")

    def _select_item_in_category(self, filtered_items: List["Item"], chosen_type: str) -> bool:
        """
        Handles the loop for selecting a specific item within the chosen category,
        wrapping it into a OneItemBundle.

        Returns:
            bool: True if an item was successfully selected and added to cart, False if back was chosen.
        """
        while True:
            print(f"\n=== Items — {chosen_type} (Enter Number+D to get item description) ===")
            for idx_item, item in enumerate(filtered_items, start=1):
                print(f"{idx_item}) {item.name} - {item.price:.2f}€")

            item_choice = input("Select item number or B to back: ").strip()

            if self._show_item_description_if_requested(item_choice, filtered_items):
                continue

            if item_choice.lower() == "b":
                return False

            try:
                idx_item = int(item_choice) - 1
                selected_item = filtered_items[idx_item]

                one_item_bundle = OneItemBundle(
                    id_bundle=len(self.cart) + 1, name=selected_item.name, item=selected_item
                )
                self._add_bundle_to_cart(one_item_bundle)
                return True

            except (ValueError, IndexError):
                print("⚠️ Invalid item number.")
            except Exception as e:
                logging.error(f"Error selecting single item: {e}")
                print(f"[ERROR] {e}")
                return True

    def _choose_single_item(self):
        """
        Allows the user to select a single item, wrapping it into a OneItemBundle.
        """
        try:
            items = self.item_service.list_items()
            item_types = sorted(set(i.item_type for i in items))
            self.all_items = items
        except Exception as e:
            logging.error(f"Cannot fetch items: {e}")
            print("[ERROR] Cannot fetch items.")
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

                if not filtered_items:
                    print(f"No items found in category {chosen_type}.")
                    continue

                if self._select_item_in_category(filtered_items, chosen_type):
                    return

            except (ValueError, IndexError):
                print("⚠️ Invalid category number.")
            except Exception as e:
                logging.error(f"Error selecting category: {e}")
                print(f"[ERROR] {e}")
