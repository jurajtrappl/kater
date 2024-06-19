from pathlib import Path


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

    def save(self, path: str) -> None:
        # TODO: Better serialization.
        try:
            p = Path(path)
            with p.open("w", encoding="utf-8") as f:
                f.write(f"{self._energy} {self._hitpoints} {self._balance} {self._level}")
        except IOError as e:
            print(f"An error occurred while saving to {path}: {e}")

    def _load_from(self, path: Path) -> None:
        try:
            with Path(path).open("r", encoding="utf-8") as file:
                data = file.readline().strip().split()
                if len(data) != 4:
                    raise ValueError("File content is invalid.")
                self._energy, self._hitpoints, self._balance, self._level = map(int, data)
        except (IOError, ValueError) as e:
            print(f"An error occurred while loading from {path}: {e}")
