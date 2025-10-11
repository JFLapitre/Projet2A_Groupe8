import logging
from typing import List, Optional, Union

from src.DBConnector import DBConnector
from src.Model.DiscountedBundle import DiscountedBundle
from src.Model.one_item_bundle import OneItemBundle
from src.Model.PredeinedBundle import PredefinedBundle


class BundleDAO:
    """Data Access Object for Bundle operations."""

    def __init__(self, db_connector: DBConnector):
        """Initialize the DAO with a database connector."""
        self.db_connector = db_connector

    def add_predefined_bundle(self, bundle: PredefinedBundle) -> PredefinedBundle:
        """
        Add a new predefined bundle to the database.

        Args:
            bundle: PredefinedBundle object to add

        Returns:
            PredefinedBundle: The created bundle with updated ID
        """
        try:
            bundle_id = self.db_connector.sql_query(
                """
                INSERT INTO fd.bundles (id_bundle, name, price, bundle_type, composition)
                VALUES (DEFAULT, %(name)s, %(price)s, 'predefined', %(composition)s)
                RETURNING id_bundle;
                """,
                {"name": bundle.name, "price": bundle.price, "composition": bundle.composition},
                "one",
            )

            bundle.id = bundle_id["id_bundle"]
            logging.info(f"Added predefined bundle: {bundle.name}")
            return bundle
        except Exception as e:
            logging.error(f"Failed to add predefined bundle: {e}")
            raise

    def add_discounted_bundle(self, bundle: DiscountedBundle) -> DiscountedBundle:
        """
        Add a new discounted bundle to the database.

        Args:
            bundle: DiscountedBundle object to add

        Returns:
            DiscountedBundle: The created bundle with updated ID
        """
        try:
            bundle_id = self.db_connector.sql_query(
                """
                INSERT INTO fd.bundles (id_bundle, name, discount, bundle_type, components)
                VALUES (DEFAULT, %(name)s, %(discount)s, 'discounted', %(components)s)
                RETURNING id_bundle;
                """,
                {"name": bundle.name, "discount": bundle.discount, "components": bundle.components},
                "one",
            )

            bundle.id = bundle_id["id_bundle"]
            logging.info(f"Added discounted bundle: {bundle.name}")
            return bundle
        except Exception as e:
            logging.error(f"Failed to add discounted bundle: {e}")
            raise

    def find_bundle_by_id(self, bundle_id: int) -> Optional[Union[PredefinedBundle, DiscountedBundle]]:
        """
        Find a bundle by its ID.

        Args:
            bundle_id: ID of the bundle to find

        Returns:
            Optional[Union[PredefinedBundle, DiscountedBundle]]: The found bundle or None
        """
        try:
            raw_bundle = self.db_connector.sql_query(
                """
                SELECT * FROM fd.bundles
                WHERE id_bundle = %(bundle_id)s
                """,
                {"bundle_id": bundle_id},
                "one",
            )

            if not raw_bundle:
                return None

            if raw_bundle["bundle_type"] == "predefined":
                return PredefinedBundle(
                    id=raw_bundle["id_bundle"],
                    name=raw_bundle["name"],
                    price=raw_bundle["price"],
                    composition=raw_bundle["composition"],
                )
            else:
                return DiscountedBundle(
                    id=raw_bundle["id_bundle"],
                    name=raw_bundle["name"],
                    discount=raw_bundle["discount"],
                    components=raw_bundle["components"],
                )
        except Exception as e:
            logging.error(f"Failed to fetch bundle {bundle_id}: {e}")
            return None

    def find_all_bundles(self) -> List[Union[PredefinedBundle, DiscountedBundle]]:
        """
        Find all bundles in the database.

        Returns:
            List[Union[PredefinedBundle, DiscountedBundle]]: List of all bundles
        """
        try:
            raw_bundles = self.db_connector.sql_query("SELECT * FROM fd.bundles", {}, "all")

            bundles = []
            for raw_bundle in raw_bundles:
                if raw_bundle["bundle_type"] == "predefined":
                    bundles.append(
                        PredefinedBundle(
                            id=raw_bundle["id_bundle"],
                            name=raw_bundle["name"],
                            price=raw_bundle["price"],
                            composition=raw_bundle["composition"],
                        )
                    )
                else:
                    bundles.append(
                        DiscountedBundle(
                            id=raw_bundle["id_bundle"],
                            name=raw_bundle["name"],
                            discount=raw_bundle["discount"],
                            components=raw_bundle["components"],
                        )
                    )
            return bundles
        except Exception as e:
            logging.error(f"Failed to fetch all bundles: {e}")
            return []

    def update_bundle(self, bundle: Union[PredefinedBundle, DiscountedBundle]) -> bool:
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
                    UPDATE fd.bundles
                    SET name = %(name)s,
                        price = %(price)s,
                        composition = %(composition)s
                    WHERE id_bundle = %(id)s
                    """,
                    {"id": bundle.id, "name": bundle.name, "price": bundle.price, "composition": bundle.composition},
                )
            else:  # DiscountedBundle
                self.db_connector.sql_query(
                    """
                    UPDATE fd.bundles
                    SET name = %(name)s,
                        discount = %(discount)s,
                        components = %(components)s
                    WHERE id_bundle = %(id)s
                    """,
                    {
                        "id": bundle.id,
                        "name": bundle.name,
                        "discount": bundle.discount,
                        "components": bundle.components,
                    },
                )
            logging.info(f"Updated bundle: {bundle.name}")
            return True
        except Exception as e:
            logging.error(f"Failed to update bundle {bundle.id}: {e}")
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
                "DELETE FROM fd.bundles WHERE id_bundle = %(bundle_id)s", {"bundle_id": bundle_id}
            )
            logging.info(f"Deleted bundle with ID: {bundle_id}")
            return True
        except Exception as e:
            logging.error(f"Failed to delete bundle {bundle_id}: {e}")
            return False
