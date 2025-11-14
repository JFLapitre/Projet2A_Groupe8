import os
from typing import List, Optional

import requests
from dotenv import load_dotenv

from src.DAO.addressDAO import AddressDAO
from src.DAO.DBConnector import DBConnector
from src.Model.address import Address


class AddressService:
    def __init__(self, db_connector: DBConnector):
        """
        Initializes the service and injects the connector into the DAO.
        """
        load_dotenv()
        self.address_dao = AddressDAO(db_connector=db_connector)
        self.api_key = os.environ["GOOGLE_MAPS_API_KEY"]

    def get_or_create_address(
        self, street_name: str, city: str, postal_code: int, street_number: str = None
    ) -> Optional[Address]:
        """
        Retrieves an address from the database if it exists.
        If not found, creates a new address record.
        This assumes the address components have already been validated.
        """

        # 1. Try to find the address first
        existing_address = self.address_dao.find_address_by_components(
            city=city, postal_code=postal_code, street_name=street_name, street_number=street_number
        )

        if existing_address:
            return existing_address  # Return the existing one

        # 2. If not found, create it
        try:
            new_address = Address(
                street_name=street_name,
                street_number=street_number,
                city=city,
                postal_code=postal_code,
            )

            created_address = self.address_dao.add_address(new_address)

            if not created_address:
                raise Exception("DAO failed to add new address.")

            return created_address

        except Exception as e:
            # Raise exception if database insertion fails
            raise ValueError(f"Database error while saving address: {e}") from e

    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """
        Retrieves a specific address by its ID.
        """
        address = self.address_dao.find_address_by_id(address_id)
        if not address:
            raise ValueError(f"No address found with ID {address_id}.")
        return address

    def delete_address(self, address_id: int) -> bool:
        """
        Deletes an address by its ID.
        Checks if the address exists first.
        """
        address = self.address_dao.find_address_by_id(address_id)
        if not address:
            raise ValueError(f"No address found with ID {address_id}.")

        if not self.address_dao.delete_address(address_id):
            raise Exception(f"Failed to delete address {address_id}.")

        return True

    def list_all_addresses(self) -> List[Address]:
        """
        Returns a list of all registered addresses.
        """
        return self.address_dao.find_all_addresses()

    def validate_address_api(self, street_name: str, city: str, postal_code: int, street_number: str = None) -> dict:
        """
        Calls Google Maps API for validation WITHOUT saving to DB.
        Returns a dictionary with the check result.
        """
        if not street_name or not city or not postal_code:
            return {"status": "INVALID", "message": "Street name, city, and postal code are required."}

        full_address = f"{street_number or ''} {street_name}, {postal_code} {city}".strip()

        if not self.api_key:
            raise EnvironmentError("Missing Google Maps API key.")

        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": full_address, "key": self.api_key},
        )
        data = response.json()
        status = data.get("status")

        if status != "OK":
            return {"status": "INVALID", "message": f"Address not found by Google (Status: {status})"}

        result = data["results"][0]
        location_type = result["geometry"]["location_type"]
        formatted_address = result["formatted_address"]

        # Si l'adresse est vague (juste la ville, la rue, etc.)
        if location_type not in ["ROOFTOP", "RANGE_INTERPOLATED"]:
            return {
                "status": "AMBIGUOUS",
                "formatted_address": formatted_address,
                "components": {
                    "street_name": street_name,  # Garde les composants d'origine
                    "city": city,
                    "postal_code": postal_code,
                    "street_number": street_number,
                },
            }

        # L'adresse est précise et correcte
        return {
            "status": "VALID",
            "formatted_address": formatted_address,
            "components": {
                "street_name": street_name,
                "city": city,
                "postal_code": postal_code,
                "street_number": street_number,
            },
        }
