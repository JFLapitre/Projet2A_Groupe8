import logging
from typing import TYPE_CHECKING, Dict, List

from src.Model.discounted_bundle import DiscountedBundle
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle

if TYPE_CHECKING:
    from src.Model.bundle import Bundle
    from src.Service.item_service import ItemService

    from src.Model.item import Item  # Import needed for item.description


class BrowseMenuView:
    """
    Handles all menu browsing and item selection logic for the customer.
    """

    def __init__(self, services: Dict, cart: List["Bundle"]):
        """
        Initializes the Browse Menu View.

        Args:
            services: Dictionary of all available services (needs 'item').
            cart: Reference to the customer's current cart list.
        """
        self.item_service: "ItemService" = services.get("item")
        self.cart = cart

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

    def _choose_discounted_bundle(self):
        """
        Allows the user to select and configure a discounted bundle (dynamic composition).
        """
        try:
            # Filter for discounted bundles with required item types
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

                # Create a temporary bundle instance for customization
                user_bundle = DiscountedBundle(
                    id_bundle=len(self.cart) + 1,
                    name=selected_bundle.name,
                    discount=selected_bundle.discount,
                    required_item_types=selected_bundle.required_item_types,
                    composition=[],
                )

                items = self.item_service.list_items()  # Fetch all items once

                # Logic to select items for each required type
                for required_type in user_bundle.required_item_types:
                    # Filter items for the required type
                    available_items = [i for i in items if i.item_type == required_type]

                    if not available_items:
                        print(f"[ERROR] No items available for type: {required_type}. Bundle cancelled.")
                        return  # Cancel bundle if a required item type is missing

                    while True:
                        print(f"\n- Select your {required_type} (Enter Number+D to show description):")
                        for idx_item, item in enumerate(available_items, start=1):
                            # Display item name and price (price is base price, discount applies to bundle total)
                            print(f"   {idx_item}) {item.name} - {((1-user_bundle.discount)*item.price):.2f}€")

                        item_choice = input(f"Choice for {required_type}: ").strip()

                        # --- Description Logic ---
                        if item_choice.lower().endswith(("d", "+d")):
                            # Extract number, removing 'd', '+d', 'D', or '+D'
                            num_str = item_choice[:-1].rstrip(" +").strip()

                            if num_str.isdigit():
                                try:
                                    item_idx = int(num_str) - 1
                                    item = available_items[item_idx]
                                    desc = item.description or "No description available."
                                    print(f"   ℹ️ {item.name} description: {desc}")
                                    continue  # Go back to prompt
                                except IndexError:
                                    print("⚠️ Invalid item number for description.")
                                    continue
                                except Exception as e:
                                    logging.error(f"Error displaying description: {e}")
                                    print("[ERROR] An unexpected error occurred.")
                                    continue
                            else:
                                print("⚠️ Invalid format for description request.")
                                continue
                        # --- End Description Logic ---

                        # --- Selection Logic ---
                        try:
                            item_idx = int(item_choice) - 1
                            if 0 <= item_idx < len(available_items):
                                selected_item = available_items[item_idx]
                                user_bundle.composition.append(selected_item)
                                print(f"   ✅ Added {selected_item.name}.")
                                break  # Move to the next required type
                            else:
                                print("⚠️ Invalid item number.")
                        except ValueError:
                            print("⚠️ Invalid input. Please enter a number or X+D.")
                        except Exception as e:
                            logging.error(f"Error during item selection: {e}")
                            print("[ERROR] An unexpected error occurred.")
                            return

                # Final price calculation and append to cart
                self.cart.append(user_bundle)
                print(f"✅ Added '{user_bundle.name}' — {user_bundle.compute_price():.2f}€")
                return  # Exit sub-menu after successful addition

            except (ValueError, IndexError):
                print("⚠️ Invalid choice.")
            except Exception as e:
                logging.error(f"Error selecting discounted bundle: {e}")
                print(f"[ERROR] Invalid choice or configuration error: {e}")

    def _choose_special_bundle(self):
        """
        Allows the user to select a predefined special bundle.
        """
        try:
            # Filter for predefined bundles with fixed composition
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

            choice = input("Select a bundle number, Number+D for description, or B to back: ").strip()

            # --- Description Logic for Bundle ---
            if choice.lower().endswith(("d", "+d")):
                num_str = choice[:-1].rstrip(" +").strip()
                if num_str.isdigit():
                    try:
                        idx = int(num_str) - 1
                        selected_bundle = bundles[idx]

                        # Use compute_description()
                        desc = selected_bundle.compute_description()
                        print(f"   ℹ️ {selected_bundle.name} description:")
                        print(f"   {desc}")
                        continue  # Restart the loop
                    except (ValueError, IndexError):
                        print("⚠️ Invalid bundle number for description.")
                        continue
                    except Exception as e:
                        logging.error(f"Error computing bundle description: {e}")
                        print("[ERROR] Failed to get bundle description.")
                        continue
                else:
                    print("⚠️ Invalid format for description request.")
                    continue
            # --- End Description Logic ---

            if choice.lower() == "b":
                return

            try:
                idx = int(choice) - 1
                selected_bundle = bundles[idx]
                self.cart.append(selected_bundle)
                print(f"✅ Added '{selected_bundle.name}' — {selected_bundle.compute_price():.2f}€")
                return
            except (ValueError, IndexError):
                print("⚠️ Invalid bundle number.")
            except Exception as e:
                logging.error(f"Error selecting special bundle: {e}")
                print(f"[ERROR] {e}")

    def _choose_single_item(self):
        """
        Allows the user to select a single item, wrapping it into a OneItemBundle.
        """
        try:
            items = self.item_service.list_items()
            item_types = sorted(set(i.item_type for i in items))
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
                # Category selection
                idx = int(choice) - 1
                chosen_type = item_types[idx]
                filtered_items = [i for i in items if i.item_type == chosen_type]

                if not filtered_items:
                    print(f"No items found in category {chosen_type}.")
                    continue

                # Item selection within category
                while True:
                    print(f"\n=== Items — {chosen_type} (Enter Number+D to show description) ===")
                    for idx_item, item in enumerate(filtered_items, start=1):
                        print(f"{idx_item}) {item.name} - {item.price:.2f}€")

                    item_choice = input("Select item number or B to back: ").strip()

                    # --- Description Logic ---
                    if item_choice.lower().endswith(("d", "+d")):
                        num_str = item_choice[:-1].rstrip(" +").strip()

                        if num_str.isdigit():
                            try:
                                item_idx = int(num_str) - 1
                                item = filtered_items[item_idx]
                                desc = item.description or "No description available."
                                print(f"   ℹ️ {item.name} description: {desc}")
                                continue  # Go back to prompt
                            except IndexError:
                                print("⚠️ Invalid item number for description.")
                                continue
                            except Exception as e:
                                logging.error(f"Error displaying description: {e}")
                                print("[ERROR] An unexpected error occurred.")
                                continue
                        else:
                            print("⚠️ Invalid format for description request.")
                            continue
                    # --- End Description Logic ---

                    if item_choice.lower() == "b":
                        break  # Go back to category selection

                    # --- Selection Logic ---
                    try:
                        idx_item = int(item_choice) - 1
                        item = filtered_items[idx_item]

                        # Wrap item in a bundle and add to cart
                        bundle = OneItemBundle(
                            id_bundle=len(self.cart) + 1,
                            name=item.name,
                            composition=[item],
                        )
                        self.cart.append(bundle)
                        print(f"✅ Added '{item.name}' — {bundle.compute_price():.2f}€")
                        return  # Exit to main menu after successful addition

                    except (ValueError, IndexError):
                        print("⚠️ Invalid item number.")

            except (ValueError, IndexError):
                print("⚠️ Invalid category number.")
            except Exception as e:
                logging.error(f"Error selecting single item: {e}")
                print(f"[ERROR] {e}")
