MAX_DISTANCE = float('inf')

Location = tuple[float, float]

class DriverManager:
    def __init__(self):
        self.drivers: dict[str, Location] = {}

    def register_driver(self, name: str, location: Location) -> None:
        self.drivers[name] = location

    def update_driver(self, name: str, location: Location) -> None:
        if name not in self.drivers:
            self.register_driver(name, location)
        else:
            self.drivers[name] = location

    def delete_driver(self, name: str) -> None:
        self.drivers.pop(name, None)

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