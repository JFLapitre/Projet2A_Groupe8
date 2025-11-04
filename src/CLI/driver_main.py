from src.CLI.abstract_view import AbstractView
from src.CLI.auth_view import AuthView


class DriverMainView(AbstractView):
    def display(self):
        auth_view = AuthView(self.session, self.services)
        if not self.session.is_authenticated():
            auth_view.display()

        if not self.session.is_authenticated():
            return

        if self.session.role != "driver":
            print("Access denied. This menu is for drivers only.")
            return

        while True:
            print("\n=== EJR Eats — Driver Menu ===")
            print("1) View pending deliveries")
            print("2) Assign myself to a delivery")
            print("3) Mark delivery as completed")
            print("q) Logout")
            choice = self.prompt("Choice: ")

            if choice == "1":
                self._view_pending_deliveries()
            elif choice == "2":
                self._assign_delivery()
            elif choice == "3":
                self._complete_delivery()
            elif choice.lower() == "q":
                self.session.logout()
                print("Logged out.")
                return
            else:
                self.print_error("Invalid choice.")

    def _view_pending_deliveries(self):
        delivery_service = self.services.get("delivery")
        try:
            deliveries = delivery_service.list_pending_deliveries()
            if not deliveries:
                print("No pending deliveries.")
                return
            for d in deliveries:
                print(f"Delivery #{d.id_delivery} - Status: {d.status} - Orders: {[o.id_order for o in d.orders]}")
        except Exception as e:
            self.print_error(f"Error retrieving deliveries: {e}")

    def _assign_delivery(self):
        delivery_service = self.services.get("delivery")
        delivery_id = int(self.prompt("Delivery ID to take: "))
        try:
            delivery_service.assign_driver_to_delivery(delivery_id, self.session.user_id)
            self.print_info(f"Assigned to delivery #{delivery_id}.")
        except Exception as e:
            self.print_error(f"Assignment failed: {e}")

    def _complete_delivery(self):
        delivery_service = self.services.get("delivery")
        delivery_id = int(self.prompt("Delivery ID to mark complete: "))
        try:
            delivery_service.complete_delivery(delivery_id)
            self.print_info(f"Delivery #{delivery_id} marked as completed.")
        except Exception as e:
            self.print_error(f"Completion failed: {e}")
