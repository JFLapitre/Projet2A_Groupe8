from typing import List

from src.Model.item import Item

from .DBConnector import DBConnector


class ItemDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def find_item_by_id(self, id_item: int) -> Item:
        raw_item = self.db_connector.sql_query("SELECT * from fd.item WHERE id_item=%s", [id_item], "one")
        if raw_item is None:
            return None
        return Item(**raw_item)

    def find_all_items(self) -> list[Item]:
        """Returns a list of all Item objects from the database.

        Returns:
            List[Item]: A list of Item objects (empty if no items exist).
        """
        raw_all_items = self.db_connector.sql_query("SELECT * FROM fd.item", {}, "all")
        return [Item(**item) for item in raw_all_items]

    def update_item(self, item: Item):
        self.db_connector.sql_query(
            "UPDATE fd.item                                      "
            "   SET name = %(name)s,                             "
            "       item_type = %(item_type)s,                   "
            "       price = %(price)s                            "
            "       description = %(description)s                "
            "       stock = %(stock)s                            "
            "       availability = %(availability)s              "
            " WHERE id_item = %(id_item)s                        "
            " RETURNING id_item;                                 ",
            {"id_item": item.id_item, "name": item.name, "item_type": item.item_type, "price": item.price},
            "one",
        )
        return self.find_item_by_id(item.id_item)

    def add_item(self, item: Item) -> Item:
        raw_created_item = self.db_connector.sql_query(
            """
        INSERT INTO fd.item (id_item, name, item_type, price)
        VALUES (DEFAULT, %(name)s, %(item_type)s, %(price)s, %(description)s, %(stock)s, %(availability)s)
        RETURNING *;
        """,
            {
                "name": item.name,
                "item_type": item.item_type,
                "price": item.price,
                "description": item.description,
                "stock": item.stock,
                "availability": item.availability,
            },
            "one",
        )
        return Item(**raw_created_item)

    def delete_item(self, id_item: int) -> bool:
        """Delete an item from the database.

        Args:
            id_item: The id of the item to delete.

        Returns:
            bool: True if the deletion suceeded, False otherwise.
        """
        res = self.db_connector.sql_query(
            "DELETE FROM fd.item WHERE id_item = %(id_item)s RETURNING id_item;", {"id_item": id_item}, "one"
        )
        return res is not None
