from typing import List

from src.Model.Item import Item

from .DBConnector import DBConnector


class ItemDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def find_item_by_id(self, item_id: int) -> Item:
        raw_item = self.db_connector.sql_query("SELECT * from fd.item WHERE id=%s", [item_id], "one")
        if raw_item is None:
            return None
        return Item(**raw_item)

    def find_all_items(self) -> list[Item]:
        """Returns a list of all Item objects from the database.

        Returns:
            List[Item]: A list of Item objects (empty if no items exist).
        """
        raw_all_items = self.db_connector.sql_query("SELECT * FROM fd.item", "all")
        return [Item(**item) for item in raw_all_items]

    def update_item(self, item: Item):
        res = self.db_connector.sql_query(
            "UPDATE fd.item                                      "
            "   SET name = %(name)s,                             "
            "       item_type = %(item_type)s,                   "
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
