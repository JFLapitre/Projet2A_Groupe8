from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class AbstractBundle(BaseModel, ABC):
    id_bundle: Optional[int] = None
    name: str
    description: Optional[str] = None

    @abstractmethod
    def compute_price(self) -> float:
        """Return the price of the bundle."""
        pass
