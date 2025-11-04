from src.CLI.abstract_view import AbstractView


class DriverDeliveryView(AbstractView):
    """
    View for drivers to see and manage deliveries.
    Relies on the 'delivery' service if available.
    """

    def display(self) -> None:
        while True:
            print("\n=== EJR Eats — Deliveries ===")
            print("1) View deliveries")
            print("2) Start a delivery")
            print("3) Validate a delivery")
            print("q) Back")
            choice = self.prompt("Choice: ")

            if choice == "1":
                self._list_deliveries()
            elif choice == "2":
                self._start_delivery()
            elif choice == "3":
                self._validate_delivery()
            elif choice.lower() == "q":
                return
            else:
                self.print_error("Invalid choice.")

    def _list_deliveries(self) -> None:
        delivery_service = self.services.get("delivery")
        if not delivery_service:
            self.print_error("Delivery service unavailable.")
            return

        try:
            deliveries = delivery_service.list_deliveries()
        except Exception as e:
            self.print_error(f"Error fetching deliveries: {e}")
            return

        if not deliveries:
            self.print_info("No deliveries found.")
            return

        print("\n--- Active Deliveries ---")
        for d in deliveries:
            # Accept dict or object types
            did = getattr(d, "id_delivery", None) or d.get("id_delivery", "N/A")
            status = getattr(d, "status", None) or d.get("status", "Unknown")
            driver = getattr(d, "driver", None) or d.get("driver", "N/A")
            nb_orders = len(getattr(d, "orders", [])) or len(d.get("orders", []))
            print(f"[{did}] Status: {status} | Orders: {nb_orders} | Driver: {driver}")

    def _start_delivery(self) -> None:
        delivery_service = self.services.get("delivery")
        if not delivery_service:
            self.print_error("Delivery service unavailable.")
            return

        try:
            delivery_service.start_delivery()
            self.print_info("Delivery started successfully!")
        except Exception as e:
            self.print_error(f"Failed to start delivery: {e}")

    def _validate_delivery(self) -> None:
        delivery_service = self.services.get("delivery")
        if not delivery_service:
            self.print_error("Delivery service unavailable.")
            return

        try:
            delivery_service.validate_delivery()
            self.print_info("Delivery validated successfully!")
        except Exception as e:
            self.print_error(f"Failed to validate delivery: {e}")
