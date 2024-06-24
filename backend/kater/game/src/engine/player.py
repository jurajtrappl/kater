from ast import literal_eval
from pathlib import Path
from typing import Dict, Tuple

from .inventory import Inventory
from .item import Item


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
    def inventory(self) -> Inventory:
        return self._inventory

    @property
    def experience(self) -> int:
        return self._experience

    @experience.setter
    def experience(self, value) -> None:
        self._experience = value

    @property
    def skills_progress(self) -> Dict[str, Tuple[int, int]]:
        return self._skills_progress

    def save(self, path: str) -> None:
        # TODO: Better serialization.
        try:
            p = Path(path)
            with p.open("w", encoding="utf-8") as f:
                f.write(
                    f"{self._energy} {self._hitpoints} {self._balance} {self._level} {self._experience}\n"
                )
                f.write(
                    ";".join([f"{k} {v}" for k, v in self._skills_progress.items()]) + "\n"
                )
                for item, quantity in self._inventory:
                    f.write(f"{item.name},{item.resource_path},{quantity}\n")
        except IOError as e:
            print(f"An error occurred while saving to {path}: {e}")

    def _load_from(self, path: Path) -> None:
        try:
            with Path(path).open("r", encoding="utf-8") as f:
                data = f.read().splitlines()

                (
                    self._energy,
                    self._hitpoints,
                    self._balance,
                    self._level,
                    self._experience,
                ) = map(int, data[0].split())

                self._skills_progress = {}
                for skill in data[1].split(";"):
                    name, level, exp = skill.split()
                    self._skills_progress[name] = literal_eval(level + exp)

                self._inventory = Inventory()
                if len(data) > 1:
                    for item in data[2:]:
                        item_name, item_resource_path, quantity = item.split(",")
                        self._inventory.add(
                            Item(item_name, item_resource_path), int(quantity)
                        )

        except (IOError, ValueError) as e:
            print(f"An error occurred while loading from {path}: {e}")
