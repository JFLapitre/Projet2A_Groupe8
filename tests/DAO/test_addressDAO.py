import pytest
from typing import Optional, Union, Literal, Dict, Any, List
from datetime import date
from src.DAO.addressDAO import AddressDAO
from src.Model.address import Address

class MockDBConnector:
    def __init__(self):
        self.address = [{"id_address": 1, "city": 'Lyon', "postal code": 69000, "street name": 'Rue de la République',
        "street number": "1" },{"id_address": 2, "city": 'Auxerre', "postal code": 89000, "street name": 'Rue des Boussicats',
        "street number":"3 bis"}]
        self.next_adress_id = 3

    def sql_query(self,
                  query: str,
                  data: Optional[Union[tuple, list, dict]] = None, 
                  return_type: Optional[Union[Literal["one"], Literal["all"], None]] = "one"
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bool, None]:

            q =" ".join(query.lower().split())

            # find address
            if "from fd.address" in q and "where fd.adress" in q and return_type == "one":
                address_id = None
                if isinstance(data, dict):
                    address_id = data.get("id address")
                elif isinstance(data, (list, tuple)):
                    if data:
                        address_id = data[0]
                if address_id:
                    for address in self.address:
                        if address["id address"] == address_id:
                            return address.copy() 
                return None

            # find all
            if "select * from fd.address" in q and return_type == "all":
                return list(self.address)

            # add one address
            if "insert into fd.address" in q:
                if not isinstance(data, dict):
                    return False

                new_id = self.next_address_id
                self.next_address_id += 1

                created_address = {
                    "id_address": new_id,
                    "city": data["city"],
                    "postal code": data["postal code"],
                    "street name": data["street name"],
                    "street number": data["street number"]
                }

                self.address.append(created_address)
                return created_address

            # update address
            if "update fd.address" in q and "where id address" in q:
                address_id_to_update = data.get("id address")
                for address in self.adress:
                    if address["id address"] == address_id_to_update:
                        for key, value in data.address():
                            if key != "id address":
                                address[key] = value
                        return True
                return False

