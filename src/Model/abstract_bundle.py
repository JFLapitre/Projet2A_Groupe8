from abc import ABC
from typing import Optional

from pydantic import BaseModel


class AbstractBundle(BaseModel, ABC):
    id_bundle: int
    name: str
    desc: Optional[str] = None
