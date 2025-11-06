from typing import List, Optional
import os
from dotenv import load_dotenv
import requests
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


    def create_address(
        self, street_name: str, city: str, postal_code: int, street_number: str = None
    ) -> Optional[Address]:
        """
        Validates the data and creates a new address in the database.
        """
        if not street_name:
            raise ValueError("Street name cannot be empty.")
        if not city:
            raise ValueError("City name cannot be empty.")
        if not postal_code:
            raise ValueError("Postal code cannot be empty.")
        full_address = f"{street_number or ''} {street_name}, {postal_code} {city}".strip()
        if not self.api_key:
            raise EnvironmentError("Missing Google Maps API key in environment variables.")
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": full_address, "key": self.api_key},
        )

        data = response.json()
        status = data.get("status")
        ad=data.get("results")
        print(ad)
        if status != "OK":
            raise ValueError(
                f"Invalid address: {full_address}. Google Maps returned status: {status}"
            )
        new_address = Address(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postal_code=postal_code,
        )

        created_address = self.address_dao.add_address(new_address)

        if not created_address:
            raise Exception("Failed to create the address in the database.")

        return created_address

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
