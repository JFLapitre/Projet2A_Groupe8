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
            print("1) View pending order")
            print("2) Create delivery")
            print("3) Get itinerary")
            print("4) Get delivery details")
            print("5) Mark delivery as completed")

            print("q) Logout")
            choice = self.prompt("Choice: ")

            if choice == "1":
                self._view_pending_order()
            elif choice == "2":
                self._assign_delivery()
            elif choice == "3":
                self._get_itinerary()
            elif choice == "4":
                self._get_delivery_details()
            elif choice == "5":
                self._complete_delivery()
            elif choice.lower() == "q":
                self.session.logout()
                print("Logged out.")
                return
            else:
                self.print_error("Invalid choice.")

    def _view_pending_order(self):
        driver_service = self.services.get("driver")
        try:
            orders = driver_service.list_pending_orders()
            if not orders:
                print("No pending orders.")
                return
            for o in orders:
                print(f"Order #{o.id_order} - Status: {o.status}")
        except Exception as e:
            self.print_error(f"Error retrieving orders: {e}")

    def _assign_delivery(self):
        driver_service = self.services.get("driver")
        order_ids= int(self.prompt("Orders ID to take: "))
        try:
            driver_service.create_and_assign_delivery(order_ids, self.session.user_id)
            new_del=driver_service.create_and_assign_delivery(order_ids, self.session.user_id)
            self.print_info(f"Assigned to delivery #{new_del.id_delivery}.")
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
