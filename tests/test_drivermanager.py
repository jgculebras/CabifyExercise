import pytest
from src.drivermanager import DriverManager
import re

@pytest.fixture
def storage_path(tmp_path):
    path = tmp_path / "drivers.json"
    path.write_text("{}", encoding="utf-8")
    return path


def test_register_driver_if_not_exists(storage_path):
    manager = DriverManager(storage_path=storage_path)
    manager.update_driver("Alice", (0.0, 0.0))
    assert "Alice" in manager.drivers

def test_update_driver_location(storage_path):
    manager = DriverManager(storage_path=storage_path)
    manager.register_driver("Bob", (1.0, 1.0))
    assert manager.drivers["Bob"] == (1.0, 1.0)
    manager.update_driver("Bob", (2.0, 2.0))
    assert manager.drivers["Bob"] == (2.0, 2.0)

def test_delete_driver(storage_path):
    manager = DriverManager(storage_path=storage_path)
    manager.register_driver("Charlie", (3.0, 3.0))
    assert "Charlie" in manager.drivers
    manager.delete_driver("Charlie")
    assert "Charlie" not in manager.drivers

def test_find_closest_driver(storage_path):
    manager = DriverManager(storage_path=storage_path)
    manager.register_driver("Dave", (2.0, 0.0))
    manager.register_driver("Eve", (1.0, 1.0))
    closest = manager.find_closest_driver((0.5, 0.5))
    assert closest == "Eve"

def test_find_closest_driver_no_drivers(storage_path):
    manager = DriverManager(storage_path=storage_path)
    closest = manager.find_closest_driver((0.0, 0.0))
    assert closest is None

def test_raises_with_nonexistent_storage_file(tmp_path):
    storage_path = tmp_path / "nonexistent.json"
    with pytest.raises(ValueError, match=f"Driver storage file {re.escape(str(storage_path))} does not exist"):
        DriverManager(storage_path=storage_path)

def test_raises_with_invalid_storage_file(tmp_path):
    storage_path = tmp_path / "drivers.txt"
    storage_path.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match=f"Invalid driver storage file {re.escape(str(storage_path))}"):
        DriverManager(storage_path=storage_path)


def test_raises_with_malformed_location(storage_path):
    storage_path.write_text('{"Alice": "not_a_list"}', encoding="utf-8")
    with pytest.raises(ValueError, match=f"Invalid entry in driver storage file {re.escape(str(storage_path))}"):
        DriverManager(storage_path=storage_path)


def test_raises_with_invalid_coordinates(storage_path):
    storage_path.write_text('{"Alice": ["bad", "coords"]}', encoding="utf-8")
    with pytest.raises(ValueError, match=f"Invalid coordinates for driver Alice in {re.escape(str(storage_path))}"):
        DriverManager(storage_path=storage_path)