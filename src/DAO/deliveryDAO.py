from src.DBconnector import DBConnector
from src.Model.Delivery import Delivery


class DeliveryDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def find_delivery_by_id(self, delivery_id: int) -> Delivery:
        raw_delivery = self.db_connector.sql_query("SELECT * from fd.delivery WHERE id=%s", [delivery_id], "one")
        if raw_delivery is None:
            return None
        return Delivery(**raw_delivery)

    def find_all_deliveries(self) -> list[Delivery]:
        """Returns a list of all Delivery objects from the database.

        Returns:
            List[Delivery]: A list of Delivery objects (empty if no deliveries exist).
        """
        raw_all_deliveries = self.db_connector.sql_query("SELECT * FROM fd.delivery", "all")
        return [Delivery(**delivery) for delivery in raw_all_deliveries]

    def update_idelivery(self, delivery: Delivery):
        res = self.db_connector.sql_query(
            "UPDATE fd.delivery                                      "
            "   SET name = %(name)s,                             "
            "       delivery_type = %(delivery_type)s,                   "
            "       price = %(price)s                            "
            " WHERE id_item = %(id_item)s                        "
            " RETURNING id_item;                                 ",
            {"id_item": item.id, "name": item.name, "item_type": item.item_type, "price": item.price},
            "one",
        )
        return res is not None

    def add_item(self, item: Item) -> Item:
        raw_created_item = self.db_connector.sql_query(
            """
        INSERT INTO fd.item (id, name, item_type, price)
        VALUES (DEFAULT, %(name)s, %(item_type)s, %(price)s)
        RETURNING *;
        """,
            {"name": item.name, "item_type": item.item_type, "price": item.price},
            "one",
        )
        # pyrefly: ignore
        return Item(**raw_created_item)

    def delete_item(self, item_id: int) -> bool:
        """Delete an item from the database.

        Args:
            item_id: The id of the item to delete.

        Returns:
            bool: True if the deletion suceeded, False otherwise.
        """
        res = self.db_connector.sql_query("DELETE FROM fd.item WHERE id = %(id)s RETURNING id;", {"id": item_id}, "one")
        return res is not None