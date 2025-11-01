from src.CLI.abstract_view import AbstractView


class OrderBuilderView(AbstractView):
    """
    View that shows cart, allows removing and checkout.
    OrderService expected method:
      - create_order(customer_id, address, bundles, items)
    """

    def display(self) -> None:
        while True:
            print("\n=== Your cart ===")
            if not (self.session.cart_bundles or self.session.cart_items):
                print("Cart is empty.")
            else:
                total = 0.0
                print("Bundles:")
                for bid, qty in self.session.cart_bundles:
                    # can't compute bundle price reliably here; call item service if available
                    bprice = None
                    item_srv = self.services.get("item")
                    if item_srv and hasattr(item_srv, "get_bundle_details"):
                        b = item_srv.get_bundle_details(bid)
                        if b:
                            bprice = getattr(b, "price", None)
                    price_str = f"{bprice}€" if bprice is not None else "?"
                    print(f"- {qty} x B{bid} = {price_str}")
                    if bprice:
                        total += bprice * qty

                print("Items:")
                for iid, qty in self.session.cart_items:
                    item_srv = self.services.get("item")
                    iprice = None
                    if item_srv and hasattr(item_srv, "get_item_details"):
                        it = item_srv.get_item_details(iid)
                        if it:
                            iprice = getattr(it, "price", 0.0)
                    price_str = f"{iprice}€" if iprice is not None else "?"
                    print(f"- {qty} x I{iid} = {price_str}")
                    if iprice:
                        total += iprice * qty

                print(f"Total (approx): {total:.2f}€")

            print("\nOptions: remove b <id> | remove i <id> | clear | checkout | back")
            cmd = self.prompt("Choice: ")
            if not cmd:
                continue
            if cmd == "back":
                return
            if cmd == "clear":
                self.session.cart_bundles.clear()
                self.session.cart_items.clear()
                self.print_info("Cart cleared.")
                continue
            parts = cmd.split()
            if len(parts) >= 3 and parts[0] == "remove":
                kind = parts[1]
                try:
                    id_ = int(parts[2])
                except ValueError:
                    self.print_error("id must be a number")
                    continue
                if kind == "b":
                    before = len(self.session.cart_bundles)
                    self.session.cart_bundles = [(b, q) for (b, q) in self.session.cart_bundles if b != id_]
                    self.print_info(f"Removed {before - len(self.session.cart_bundles)} bundles.")
                elif kind == "i":
                    before = len(self.session.cart_items)
                    self.session.cart_items = [(it, q) for (it, q) in self.session.cart_items if it != id_]
                    self.print_info(f"Removed {before - len(self.session.cart_items)} items.")
                else:
                    self.print_error("Usage: remove <b|i> <id>")
                continue
            if cmd == "checkout":
                self._checkout()
                return
            self.print_error("Unknown command.")

    def _checkout(self) -> None:
        if not self.session.is_authenticated():
            self.print_error("You must be logged in to checkout.")
            return
        if not (self.session.cart_bundles or self.session.cart_items):
            self.print_error("Cart is empty.")
            return

        order_srv = self.services.get("order")
        if order_srv is None:
            self.print_error("Order service not available.")
            return

        customer_id = self.session.user_id
        address = self.prompt("Delivery address (or press Enter to use your default): ").strip()
        if not address:
            address = None

        # build payload expected by service
        bundles_payload = [(b, q) for (b, q) in self.session.cart_bundles]
        items_payload = [(i, q) for (i, q) in self.session.cart_items]

        try:
            # Try many possible service signatures gracefully
            if hasattr(order_srv, "create_order"):
                created = order_srv.create_order(
                    customer_id=customer_id, address=address, bundles=bundles_payload, items=items_payload
                )
            elif hasattr(order_srv, "add_order"):
                created = order_srv.add_order(
                    customer_id=customer_id, address=address, bundles=bundles_payload, items=items_payload
                )
            else:
                raise RuntimeError("Order service has no create_order/add_order method")

            # created may be dict or model
            if isinstance(created, dict):
                oid = created.get("id_order") or created.get("id") or created.get("order_id")
            else:
                oid = getattr(created, "id_order", None) or getattr(created, "id", None)

            self.print_info(f"Order placed (id={oid}).")
            # clear cart
            self.session.cart_bundles.clear()
            self.session.cart_items.clear()
        except Exception as e:
            self.print_error(f"Failed to place order: {e}")
