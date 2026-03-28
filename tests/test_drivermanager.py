import pytest
from src.drivermanager import DriverManager


def test_register_driver_if_not_exists():
    manager = DriverManager()
    manager.update_driver("Alice", (0.0, 0.0))
    assert "Alice" in manager.drivers

def test_update_driver_location():
    manager = DriverManager()
    manager.register_driver("Bob", (1.0, 1.0))
    assert manager.drivers["Bob"] == (1.0, 1.0)
    manager.update_driver("Bob", (2.0, 2.0))
    assert manager.drivers["Bob"] == (2.0, 2.0)

def test_delete_driver():
    manager = DriverManager()
    manager.register_driver("Charlie", (3.0, 3.0))
    assert "Charlie" in manager.drivers
    manager.delete_driver("Charlie")
    assert "Charlie" not in manager.drivers

def test_find_closest_driver():
    manager = DriverManager()
    manager.register_driver("Dave", (2.0, 0.0))
    manager.register_driver("Eve", (1.0, 1.0))
    closest = manager.find_closest_driver((0.5, 0.5))
    assert closest == "Eve"

def test_find_closest_driver_no_drivers():
    manager = DriverManager()
    closest = manager.find_closest_driver((0.0, 0.0))
    assert closest is None