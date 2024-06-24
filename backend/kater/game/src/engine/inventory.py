from typing import Dict, Tuple

from .item import Item


class Inventory:
    def __init__(self, size: int=12):
        self._size = size
        self._items: Dict[str, Tuple[Item, int]] = {}

    def __iter__(self):
        for item, quantity in self._items.values():
            yield item, quantity

    def add(self, item: Item, quantity: int) -> None:
        if item.name in self._items:
            item, old_quantity = self._items[item.name]
            self._items[item.name] = (item, old_quantity + quantity)
            return

        if len(self._items) < self._size:
            self._items[item.name] = (item, quantity)
