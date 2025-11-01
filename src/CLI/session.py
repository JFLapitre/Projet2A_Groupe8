from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Session:
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None  # "customer", "driver", "admin"
    token: Optional[str] = None
    cart_bundles: List[Tuple[int, int]] = field(default_factory=list)  # (bundle_id, qty)
    cart_items: List[Tuple[int, int]] = field(default_factory=list)  # (item_id, qty)

    def is_authenticated(self) -> bool:
        return self.user_id is not None

    def clear(self) -> None:
        self.user_id = None
        self.username = None
        self.role = None
        self.token = None
        self.cart_bundles.clear()
        self.cart_items.clear()
