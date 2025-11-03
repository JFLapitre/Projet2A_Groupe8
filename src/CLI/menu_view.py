from src.CLI.abstract_view import AbstractView
from src.CLI.order_builder_view import OrderBuilderView


class MenuView(AbstractView):
    """
    Shows bundles and items; allows adding to cart and viewing details.
    Expects services['item'] to implement:
      - list_items()
      - list_bundles()
      - get_item_details(id)
      - get_bundle_details(id)
    """

    def display(self) -> None:
        item_srv = self.services.get("item")
        if item_srv is None:
            self.print_error("Item service not provided.")
            return

        while True:
            print("\n=== Menu ===")
            try:
                bundles = item_srv.list_bundles() if hasattr(item_srv, "list_bundles") else []
                items = item_srv.list_items() if hasattr(item_srv, "list_items") else []
            except Exception as e:
                self.print_error(f"Failed to fetch menu: {e}")
                return

            print("\n-- Bundles --")
            for b in bundles:
                bid = getattr(b, "id_bundle", getattr(b, "id", None))
                price = getattr(b, "price", None)
                if price is not None:
                    price_str = f"{price}€"
                else:
                    discount = getattr(b, "discount", 0.0) or 0.0
                    price_str = f"Discount {int(discount * 100)}%"
                print(f"B{bid}: {getattr(b, 'name', '<no-name>')} — {price_str}")

            print("\n-- Items --")
            for i in items:
                iid = getattr(i, "id_item", getattr(i, "id", None))
                name = getattr(i, "name", "<no-name>")
                price = getattr(i, "price", 0.0)
                avail = getattr(i, "availability", True)
                print(f"I{iid}: {name} — {price}€ {'(unavailable)' if not avail else ''}")

            print("\nCommands: addb <id> <qty> | addi <id> <qty> | d b<id> | d i<id> | cart | back")
            cmd = self.prompt("Choice: ")
            if not cmd:
                continue
            if cmd == "back":
                return
            if cmd == "cart":
                OrderBuilderView(self.session, self.services).display()
                continue

            parts = cmd.split()
            if parts[0] == "addb" and len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit():
                bid = int(parts[1])
                qty = int(parts[2])
                self.session.cart_bundles.append((bid, qty))
                self.print_info(f"Added {qty} x bundle {bid} to cart.")
                continue
            if parts[0] == "addi" and len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit():
                iid = int(parts[1])
                qty = int(parts[2])
                self.session.cart_items.append((iid, qty))
                self.print_info(f"Added {qty} x item {iid} to cart.")
                continue
            if parts[0] == "d" and len(parts) >= 2:
                token = parts[1]
                if token.startswith("b"):
                    try:
                        bid = int(token[1:])
                        b = item_srv.get_bundle_details(bid) if hasattr(item_srv, "get_bundle_details") else None
                        if b:
                            self._print_bundle(b)
                        else:
                            self.print_error("Bundle not found.")
                    except Exception:
                        self.print_error("Invalid bundle id.")
                elif token.startswith("i"):
                    try:
                        iid = int(token[1:])
                        it = item_srv.get_item_details(iid) if hasattr(item_srv, "get_item_details") else None
                        if it:
                            self._print_item(it)
                        else:
                            self.print_error("Item not found.")
                    except Exception:
                        self.print_error("Invalid item id.")
                else:
                    self.print_error("Use d b<id> or d i<id>")
                continue

            self.print_error("Unknown command.")

    def _print_item(self, it):
        print("\n=== Item ===")
        print("Name:", getattr(it, "name", ""))
        print("Type:", getattr(it, "item_type", ""))
        print("Price:", getattr(it, "price", ""))
        print("Stock:", getattr(it, "stock", ""))
        print("Description:", getattr(it, "description", ""))
        self.prompt("Press Enter to continue...")

    def _print_bundle(self, b):
        print("\n=== Bundle ===")
        print("Name:", getattr(b, "name", ""))
        price = getattr(b, "price", None)
        if price is not None:
            print("Price:", price)
        else:
            print("Discount:", getattr(b, "discount", 0.0))
        comp = getattr(b, "composition", [])
        print("Composition:")
        for it in comp:
            print(" -", getattr(it, "name", "<no-name>"), f"({getattr(it, 'item_type', '')})")
        self.prompt("Press Enter to continue...")
