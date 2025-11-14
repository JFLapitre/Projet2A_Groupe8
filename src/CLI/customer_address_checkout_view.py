import logging
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from src.Model.bundle import Bundle

    from src.CLI.session import Session
    from src.Model.address import Address
    from src.Service.address_service import AddressService
    from src.Service.order_service import OrderService


class AddressCheckoutView:
    """
    Handles the final checkout, address validation, order creation, and cart clearing.
    """

    def __init__(self, services: Dict, session: "Session", cart: List["Bundle"]):
        """
        Initializes the Address Checkout View.

        Args:
            services: Dictionary of all available services (needs 'address', 'order').
            session: The active user session.
            cart: Reference to the customer's current cart list.
        """
        self.address_service: "AddressService" = services.get("address")
        self.order_service: "OrderService" = services.get("order")
        self.session = session
        self.cart = cart

    def _get_address_input(self) -> Dict[str, Optional[str]]:
        """
        Prompts the user for address components.

        Returns:
            Dict[str, Optional[str]]: Dictionary containing address components.
        """
        print("\n📦 Enter delivery address:")
        street_number_input = input("Street number (if exists): ").strip()
        street_name = input("Street name: ").strip()
        city = input("City: ").strip()
        postal_code_input = input("Postal code: ").strip()

        return {
            "street_number_input": street_number_input,
            "street_name": street_name,
            "city": city,
            "postal_code_input": postal_code_input,
        }

    def _process_address_validation(self) -> Optional["Address"]:
        """
        Handles the loop for address input, validation (API), confirmation,
        and creation/retrieval in the database.

        Returns:
            Optional[Address]: The confirmed Address object or None if cancelled/failed.
        """
        final_address_obj = None

        while final_address_obj is None:
            address_data = self._get_address_input()

            try:
                postal_code = int(address_data["postal_code_input"])
                street_number = address_data["street_number_input"] if address_data["street_number_input"] else None

                # 1. API Validation
                validation_result = self.address_service.validate_address_api(
                    street_name=address_data["street_name"],
                    city=address_data["city"],
                    postal_code=postal_code,
                    street_number=street_number,
                )

                status = validation_result.get("status")

                if status == "INVALID":
                    print(f"[ERROR] {validation_result.get('message')}. Veuillez réessayer.")
                    continue

                # 'components' exists if status is VALID or AMBIGUOUS
                components = validation_result["components"]

                display_street_number = components["street_number"] or ""
                display_address = (
                    f"{display_street_number} {components['street_name']}, "
                    f"{components['postal_code']} {components['city']}"
                ).strip()

                if status == "AMBIGUOUS":
                    print(f"\n⚠️  Address is ambiguous (Google suggests: {validation_result.get('formatted_address')})")
                    confirm_ambiguous = (
                        input("   Do you want to use the address components entered? (Y/N): ").strip().lower()
                    )
                    if confirm_ambiguous != "y":
                        continue

                # --- Final Confirmation ---
                print(f"\n❓ Do you confirm the delivery address: **{display_address}**?")
                final_confirm = input("Confirm delivery address? (Y/N): ").strip().lower()

                if final_confirm != "y":
                    print("Delivery address confirmation cancelled.")
                    return None

                print("✅ Address confirmed.")

                # 2. Database Creation/Retrieval
                final_address_obj = self.address_service.get_or_create_address(
                    street_name=components["street_name"],
                    city=components["city"],
                    postal_code=components["postal_code"],
                    street_number=components["street_number"],
                )

                if final_address_obj is None:
                    raise Exception("Failed to retrieve or create address in database.")

            except ValueError:
                print("[ERROR] Postal code must be a number. Please try again.")
                continue
            except Exception as e:
                logging.error(f"Address processing failed: {e}")
                print(f"[ERROR] An unexpected error occurred during address processing: {e}")
                return None

        return final_address_obj

    def validate_order(self):
        """
        Initiates the checkout process, including address validation and order creation.
        If successful, clears the cart. Returns to main menu on failure or cancellation.
        """
        if not self.cart:
            print("🛒 Your cart is empty.")
            return

        total = sum(b.compute_price() for b in self.cart)
        print("\n=== 💳 Review Your Order ===")
        for b in self.cart:
            print(f"- {b.name}: {b.compute_price():.2f}€")
            if hasattr(b, "composition") and b.composition:
                for item in b.composition:
                    print(f"    • {item.name}")
        print(f"\n💰 Total to pay: {total:.2f}€")

        confirm = input("Proceed to checkout? (Y/N): ").strip().lower()
        if confirm != "y":
            print("Order cancelled.")
            return

        # 1. Process Address
        final_address_obj = self._process_address_validation()

        if final_address_obj is None:
            return

        # 2. Create Order
        try:
            created_order = self.order_service.create_order(self.session.user_id, final_address_obj.id_address)
            for bundle in self.cart:
                self.order_service.add_bundle_to_order(created_order.id_order, bundle)

            print(f"\n🎉 Order #{created_order.id_order} confirmed!")

            delivery_address = (
                f"{final_address_obj.street_number or ''} {final_address_obj.street_name}, {final_address_obj.city}"
            ).strip()
            print(f"🧾 Total: {total:.2f}€ — {len(self.cart)} items delivered to {delivery_address}.")

            # 3. Clear Cart upon success
            self.cart.clear()

        except Exception as e:
            logging.error(f"Order creation failed: {e}")
            print(f"[ERROR] Cannot confirm order: {e}")
            return
