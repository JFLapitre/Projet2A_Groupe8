from abc import ABC

from pydantic import BaseModel


class AbstractBundle(BaseModel, ABC):
    id: int
    name: str
