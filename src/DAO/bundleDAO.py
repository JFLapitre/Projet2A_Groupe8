import logging
from typing import List, Optional, Union

from pydantic import BaseModel

from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle


class BundleDAO(BaseModel):
    """Data Access Object for Bundle operations."""

    db_connector: DBConnector
    item_dao: ItemDAO

    class Config:
        arbitrary_types_allowed = True

    def find_bundle_by_id(self, bundle_id: int) -> Optional[Union[PredefinedBundle, DiscountedBundle, OneItemBundle]]:
        """
        Find a bundle by its ID.

        Args:
            bundle_id: ID of the bundle to find

        Returns:
            Optional bundle object or None
        """
        try:
            raw_bundle = self.db_connector.sql_query(
                "SELECT * FROM fd.bundle WHERE id_bundle = %(bundle_id)s", {"bundle_id": bundle_id}, "one"
            )

            if not raw_bundle:
                return None

            raw_items = self.db_connector.sql_query(
                """
                SELECT i.*
                FROM fd.item i
                JOIN fd.bundle_item bi ON i.id_item = bi.id_item
                WHERE bi.id_bundle = %(bundle_id)s
                """,
                {"bundle_id": bundle_id},
                "all",
            )

            composition = []
            for item_data in raw_items:
                item = self.item_dao.find_item_by_id(item_data["id_item"])
                if item:
                    composition.append(item)

            bundle_type = raw_bundle["bundle_type"]

            if bundle_type == "predefined":
                return PredefinedBundle(
                    id_bundle=raw_bundle["id_bundle"],
                    name=raw_bundle["name"],
                    description=raw_bundle["description"],
                    price=raw_bundle["price"],
                    composition=composition,
                )
            elif bundle_type == "discount":
                return DiscountedBundle(
                    id_bundle=raw_bundle["id_bundle"],
                    name=raw_bundle["name"],
                    description=raw_bundle["description"],
                    discount=raw_bundle["discount"],
                    required_item_types=raw_bundle["required_item_types"],
                    composition=composition,
                )
            elif bundle_type == "single_item":
                return OneItemBundle(
                    id_bundle=raw_bundle["id_bundle"],
                    name=raw_bundle["name"],
                    description=raw_bundle["description"],
                    price=raw_bundle["price"],
                    composition=composition,  # composition must be a list
                )
            else:
                logging.warning(f"Unknown bundle type: {bundle_type}")
                return None

        except Exception as e:
            logging.error(f"Failed to fetch bundle {bundle_id}: {e}")
            return None

    def find_all_bundles(self) -> List[Union[PredefinedBundle, DiscountedBundle, OneItemBundle]]:
        """
        Find all bundles in the database.

        Returns:
            List of all bundles
        """
        try:
            raw_bundles = self.db_connector.sql_query("SELECT * FROM fd.bundle", {}, "all")

            bundles = []
            for raw_bundle in raw_bundles:
                bundle = self.find_bundle_by_id(raw_bundle["id_bundle"])
                if bundle:
                    bundles.append(bundle)

            return bundles
        except Exception as e:
            logging.error(f"Failed to fetch all bundles: {e}")
            return []

    def add_predefined_bundle(self, bundle: PredefinedBundle) -> Optional[PredefinedBundle]:
        """
        Add a new predefined bundle to the database.

        Args:
            bundle: PredefinedBundle object to add

        Returns:
            PredefinedBundle: The created bundle with updated ID
        """
        try:
            raw_created_bundle = self.db_connector.sql_query(
                """
                INSERT INTO fd.bundle (name, description, bundle_type, price, discount)
                VALUES (%(name)s, %(description)s, 'predefined', %(price)s, NULL)
                RETURNING *;
                """,
                {"name": bundle.name, "description": bundle.description, "price": bundle.price},
                "one",
            )

            id_bundle = raw_created_bundle["id_bundle"]

            for item in bundle.composition:
                item_id = item.id_item if hasattr(item, "id_item") else item
                self.db_connector.sql_query(
                    """
                    INSERT INTO fd.bundle_item (id_bundle, id_item)
                    VALUES (%(id_bundle)s, %(id_item)s)
                    """,
                    {"id_bundle": id_bundle, "id_item": item_id},
                    None,
                )

            logging.info(f"Added predefined bundle: {bundle.name}")
            return self.find_bundle_by_id(id_bundle)
        except Exception as e:
            logging.error(f"Failed to add predefined bundle: {e}")
            return None

    def add_discounted_bundle(self, bundle: DiscountedBundle) -> Optional[DiscountedBundle]:
        """
        Add a new discounted bundle to the database.

        Args:
            bundle: DiscountedBundle object to add

        Returns:
            DiscountedBundle: The created bundle with updated ID
        """
        try:
            raw_created_bundle = self.db_connector.sql_query(
                """
                INSERT INTO fd.bundle (name, description, bundle_type, price, discount)
                VALUES (%(name)s, %(description)s, 'discount', NULL, %(discount)s)
                RETURNING *;
                """,
                {"name": bundle.name, "description": bundle.description, "discount": bundle.discount},
                "one",
            )

            id_bundle = raw_created_bundle["id_bundle"]

            for item in bundle.composition:
                item_id = item.id_item if hasattr(item, "id_item") else item
                self.db_connector.sql_query(
                    """
                    INSERT INTO fd.bundle_item (id_bundle, id_item)
                    VALUES (%(id_bundle)s, %(id_item)s)
                    """,
                    {"id_bundle": id_bundle, "id_item": item_id},
                    None,
                )

            logging.info(f"Added discounted bundle: {bundle.name}")
            return self.find_bundle_by_id(id_bundle)
        except Exception as e:
            logging.error(f"Failed to add discounted bundle: {e}")
            return None

    def add_one_item_bundle(self, bundle: OneItemBundle) -> Optional[OneItemBundle]:
        """
        Add a new single item bundle to the database.

        Args:
            bundle: OneItemBundle object to add

        Returns:
            OneItemBundle: The created bundle with updated ID
        """
        try:
            raw_created_bundle = self.db_connector.sql_query(
                """
                INSERT INTO fd.bundle (name, description, bundle_type, price, discount)
                VALUES (%(name)s, %(description)s, 'single_item', %(price)s, NULL)
                RETURNING *;
                """,
                {"name": bundle.name, "description": bundle.description, "price": bundle.price},
                "one",
            )

            id_bundle = raw_created_bundle["id_bundle"]

            for item in bundle.composition:
                item_id = item.id_item if hasattr(item, "id_item") else item
                self.db_connector.sql_query(
                    """
                    INSERT INTO fd.bundle_item (id_bundle, id_item)
                    VALUES (%(id_bundle)s, %(id_item)s)
                    """,
                    {"id_bundle": id_bundle, "id_item": item_id},
                    None,
                )

            logging.info(f"Added one item bundle: {bundle.name}")
            return self.find_bundle_by_id(id_bundle)
        except Exception as e:
            logging.error(f"Failed to add one item bundle: {e}")
            return None

    def update_bundle(self, bundle: Union[PredefinedBundle, DiscountedBundle, OneItemBundle]) -> bool:
        """
        Update an existing bundle.

        Args:
            bundle: Bundle object to update

        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if isinstance(bundle, PredefinedBundle):
                self.db_connector.sql_query(
                    """
                    UPDATE fd.bundle
                    SET name = %(name)s,
                        description = %(description)s,
                        price = %(price)s
                    WHERE id_bundle = %(id_bundle)s
                    """,
                    {
                        "id_bundle": bundle.id_bundle,
                        "name": bundle.name,
                        "description": bundle.description,
                        "price": bundle.price,
                    },
                    None,
                )
            elif isinstance(bundle, DiscountedBundle):
                self.db_connector.sql_query(
                    """
                    UPDATE fd.bundle
                    SET name = %(name)s,
                        description = %(description)s,
                        discount = %(discount)s,
                        required_item_types = %(required_item_types)s
                    WHERE id_bundle = %(id_bundle)s
                    """,
                    {
                        "id_bundle": bundle.id_bundle,
                        "name": bundle.name,
                        "description": bundle.description,
                        "discount": bundle.discount,
                        "required_item_types": bundle.required_item_types,
                    },
                    None,
                )
            elif isinstance(bundle, OneItemBundle):
                self.db_connector.sql_query(
                    """
                    UPDATE fd.bundle
                    SET name = %(name)s,
                        description = %(description)s,
                        price = %(price)s
                    WHERE id_bundle = %(id_bundle)s
                    """,
                    {
                        "id_bundle": bundle.id_bundle,
                        "name": bundle.name,
                        "description": bundle.description,
                        "price": bundle.price,
                    },
                    None,
                )

            self.db_connector.sql_query(
                "DELETE FROM fd.bundle_item WHERE id_bundle = %(id_bundle)s", {"id_bundle": bundle.id_bundle}, None
            )

            for item in bundle.composition:
                item_id = item.id_item if hasattr(item, "id_item") else item
                self.db_connector.sql_query(
                    """
                    INSERT INTO fd.bundle_item (id_bundle, id_item)
                    VALUES (%(id_bundle)s, %(id_item)s)
                    """,
                    {"id_bundle": bundle.id_bundle, "id_item": item_id},
                    None,
                )

            logging.info(f"Updated bundle: {bundle.name}")
            return True
        except Exception as e:
            logging.error(f"Failed to update bundle {bundle.id_bundle}: {e}")
            return False

    def delete_bundle(self, bundle_id: int) -> bool:
        """
        Delete a bundle by its ID.

        Args:
            bundle_id: ID of the bundle to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            self.db_connector.sql_query(
                "DELETE FROM fd.bundle_item WHERE id_bundle = %(bundle_id)s", {"bundle_id": bundle_id}, None
            )

            self.db_connector.sql_query(
                "DELETE FROM fd.bundle WHERE id_bundle = %(bundle_id)s", {"bundle_id": bundle_id}, None
            )

            logging.info(f"Deleted bundle with ID: {bundle_id}")
            return True
        except Exception as e:
            logging.error(f"Failed to delete bundle {bundle_id}: {e}")
            return False
