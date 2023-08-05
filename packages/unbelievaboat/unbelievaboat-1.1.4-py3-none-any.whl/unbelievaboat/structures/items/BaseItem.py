from typing import Any, Dict, List, Optional

from .StoreItemAction import StoreItemAction
from .StoreItemRequirement import StoreItemRequirement


class BaseItem:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.name: str = data["name"]
        self.description: Optional[str] = data.get("description", None)
        self.is_usable: bool = data["is_usable"]
        self.is_sellable: bool = data["is_sellable"]
        self.requirements: List[StoreItemRequirement] = [
            StoreItemRequirement(requirement)
            for requirement in data.get("requirements", [])
        ]
        self.actions: List[StoreItemAction] = [
            StoreItemAction(action) for action in data.get("actions", [])
        ]
        self.emoji_unicode: Optional[str] = data.get("emoji_unicode", None)
        self.emoji_id: Optional[str] = data.get("emoji_id", None)

    def __str__(self) -> str:
        return "<BaseItem name={} description={} is_usable={} is_sellable={} requirements={} actions={} emoji_unicode={} emoji_id={}>".format(
            self.name,
            self.description,
            self.is_usable,
            self.is_sellable,
            self.requirements,
            self.actions,
            self.emoji_unicode,
            self.emoji_id,
        )
