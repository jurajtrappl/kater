from pathlib import Path
from typing import List, Tuple

from engine.item import Item


class Player:
    def __init__(self, character_save_path: Path) -> None:
        self._load_from(character_save_path)

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value) -> None:
        self._energy = value

    @property
    def hitpoints(self) -> int:
        return self._hitpoints

    @hitpoints.setter
    def hitpoints(self, value) -> None:
        self._hitpoints = value

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value) -> None:
        self._balance = value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value) -> int:
        self._level = value

    @property
    def inventory(self) -> List[Tuple[Item, int]]:
        return self._inventory

    def save(self, path: str) -> None:
        # TODO: Better serialization.
        try:
            p = Path(path)
            with p.open("w", encoding="utf-8") as f:
                f.write(
                    f"{self._energy} {self._hitpoints} {self._balance} {self._level}\n"
                )
                for item, quantity in self._inventory:
                    f.write(f"{item.name},{item.resource_path},{quantity}\n")
        except IOError as e:
            print(f"An error occurred while saving to {path}: {e}")

    def _load_from(self, path: Path) -> None:
        try:
            with Path(path).open("r", encoding="utf-8") as f:
                data = f.read().splitlines()

                self._energy, self._hitpoints, self._balance, self._level = map(
                    int, data[0].split()
                )

                self._inventory = []
                if len(data) > 1:
                    for item in data[1:]:
                        item_name, item_resource_path, quantity = item.split(",")
                        self._inventory.append(
                            (Item(item_name, item_resource_path), quantity)
                        )

        except (IOError, ValueError) as e:
            print(f"An error occurred while loading from {path}: {e}")
