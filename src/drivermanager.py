"""Driver location management with optional JSON-backed persistence."""

import json
from pathlib import Path

MAX_DISTANCE = float('inf')
DEFAULT_STORAGE_PATH = Path(__file__).resolve().parent.parent / "drivers.json"

Location = tuple[float, float]

class DriverManager:
    """Manage tracked drivers in memory and persist them to a JSON file."""

    def __init__(self, storage_path: str | Path | None = None):
        self.storage_path = Path(storage_path) if storage_path is not None else DEFAULT_STORAGE_PATH
        self.drivers: dict[str, Location] = self._load_drivers()

    def _load_drivers(self) -> dict[str, Location]:
        """Load tracked drivers from storage, or start empty on first run."""

        if not self.storage_path.exists():
            return {}

        try:
            with self.storage_path.open("r", encoding="utf-8") as storage_file:
                data = json.load(storage_file)
        except (json.JSONDecodeError, ValueError) as error:
            raise ValueError(f"Invalid driver storage file {self.storage_path}") from error

        if not isinstance(data, dict):
            raise ValueError(f"Invalid driver storage file {self.storage_path}: expected a JSON object")

        drivers: dict[str, Location] = {}
        for name, location in data.items():
            if not isinstance(name, str) or not isinstance(location, list) or len(location) != 2:
                raise ValueError(f"Invalid entry in driver storage file {self.storage_path}")

            try:
                latitude = float(location[0])
                longitude = float(location[1])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid coordinates for driver {name} in {self.storage_path}") from error

            drivers[name] = (latitude, longitude)

        return drivers

    def _save_drivers(self) -> None:
        """Persist the current in-memory driver state to the storage file."""

        serialized = {
            name: [location[0], location[1]]
            for name, location in self.drivers.items()
        }
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w", encoding="utf-8") as storage_file:
            json.dump(serialized, storage_file, indent=2)

    def register_driver(self, name: str, location: Location) -> None:
        self.drivers[name] = location
        self._save_drivers()

    def update_driver(self, name: str, location: Location) -> None:
        if name not in self.drivers:
            self.register_driver(name, location)
        else:
            self.drivers[name] = location
            self._save_drivers()

    def delete_driver(self, name: str) -> None:
        if name in self.drivers:
            self.drivers.pop(name)
            self._save_drivers()

    def find_closest_driver(self, location: Location) -> str | None:
        closest_driver = None
        closest_distance = MAX_DISTANCE

        for driver_name, driver_location in self.drivers.items():
            distance = self.calculate_distance(location, driver_location)
            if distance < closest_distance:
                closest_distance = distance
                closest_driver = driver_name

        return closest_driver

    def calculate_distance(self, loc1: Location, loc2: Location) -> float:
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])