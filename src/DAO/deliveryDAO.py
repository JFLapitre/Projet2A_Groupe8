import logging
from typing import List, Optional

from src.DAO.DBConnector import DBConnector
from src.Model.delivery import Delivery


class DeliveryDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def find_delivery_by_id(self, id_delivery: int) -> Optional[Delivery]:
        """Find a delivery by its ID.

        Args:
            id_delivery: The ID of the delivery to find.

        Returns:
            Delivery object if found, None otherwise.
        """
        try:
            raw_delivery = self.db_connector.sql_query(
                "SELECT * FROM fd.delivery WHERE id_delivery = %(id_delivery)s", {"id_delivery": id_delivery}, "one"
            )
            if raw_delivery is None:
                return None
            return Delivery(**raw_delivery)
        except Exception as e:
            logging.error(f"Failed to fetch delivery {id_delivery}: {e}")
            return None

    def find_all_deliveries(self) -> List[Delivery]:
        """Returns a list of all Delivery objects from the database.

        Returns:
            List[Delivery]: A list of Delivery objects (empty if no deliveries exist).
        """
        try:
            raw_all_deliveries = self.db_connector.sql_query("SELECT * FROM fd.delivery", {}, "all")
            return [Delivery(**delivery) for delivery in raw_all_deliveries]
        except Exception as e:
            logging.error(f"Failed to fetch all deliveries: {e}")
            return []

    def update_delivery(self, delivery: Delivery) -> bool:
        """Update an existing delivery.

        Args:
            delivery: The Delivery object with updated information.

        Returns:
            bool: True if update succeeded, False otherwise.
        """
        try:
            res = self.db_connector.sql_query(
                """
                UPDATE fd.delivery
                SET id_driver = %(id_driver)s,
                    status = %(status)s,
                    delivery_time = %(delivery_time)s
                WHERE id_delivery = %(id_delivery)s
                RETURNING id_delivery;
                """,
                {
                    "id_delivery": delivery.id_delivery,
                    "id_driver": delivery.id_driver,
                    "status": delivery.status,
                    "delivery_time": delivery.delivery_time,
                },
                "one",
            )
            return res is not None
        except Exception as e:
            logging.error(f"Failed to update delivery {delivery.id_delivery}: {e}")
            return False

    def add_delivery(self, delivery: Delivery) -> Optional[Delivery]:
        """Add a new delivery to the database.

        Args:
            delivery: The Delivery object to add.

        Returns:
            Delivery: The created delivery with its ID, or None if failed.
        """
        try:
            raw_created_delivery = self.db_connector.sql_query(
                """
                INSERT INTO fd.delivery (id_driver, status, delivery_time)
                VALUES (%(id_driver)s, %(status)s, %(delivery_time)s)
                RETURNING *;
                """,
                {"id_driver": delivery.id_driver, "status": delivery.status, "delivery_time": delivery.delivery_time},
                "one",
            )
            return Delivery(**raw_created_delivery)
        except Exception as e:
            logging.error(f"Failed to add delivery: {e}")
            return None

    def delete_delivery(self, id_delivery: int) -> bool:
        """Delete a delivery from the database.

        Args:
            id_delivery: The ID of the delivery to delete.

        Returns:
            bool: True if the deletion succeeded, False otherwise.
        """
        try:
            res = self.db_connector.sql_query(
                "DELETE FROM fd.delivery WHERE id_delivery = %(id_delivery)s RETURNING id_delivery;",
                {"id_delivery": id_delivery},
                "one",
            )
            return res is not None
        except Exception as e:
            logging.error(f"Failed to delete delivery {id_delivery}: {e}")
            return False
