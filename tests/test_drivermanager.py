import pytest

from src.drivermanager import DriverManager

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


def test_missing_storage_file_starts_empty(storage_path):
    manager = DriverManager(storage_path=storage_path)
    assert manager.drivers == {}


def test_missing_storage_file_is_created_on_first_update(storage_path):
    manager = DriverManager(storage_path=storage_path)

    manager.update_driver("Alice", (0.0, 0.0))

    assert storage_path.exists()
    assert DriverManager(storage_path=storage_path).drivers == {"Alice": (0.0, 0.0)}

def test_raises_with_invalid_storage_file(tmp_path):
    storage_path = tmp_path / "drivers.txt"
    storage_path.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid driver storage file"):
        DriverManager(storage_path=storage_path)


def test_raises_with_malformed_location(storage_path):
    storage_path.write_text('{"Alice": "not_a_list"}', encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid entry in driver storage file"):
        DriverManager(storage_path=storage_path)


def test_raises_with_invalid_coordinates(storage_path):
    storage_path.write_text('{"Alice": ["bad", "coords"]}', encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid coordinates for driver Alice"):
        DriverManager(storage_path=storage_path)


def test_persist_drivers_between_sessions(storage_path):
    first_session = DriverManager(storage_path=storage_path)
    first_session.update_driver("Alice", (10.0, 20.0))
    first_session.update_driver("Bob", (30.0, 40.0))

    second_session = DriverManager(storage_path=storage_path)
    assert second_session.drivers == {
        "Alice": (10.0, 20.0),
        "Bob": (30.0, 40.0),
    }


def test_stop_tracking_removes_driver_from_persisted_state(storage_path):
    manager = DriverManager(storage_path=storage_path)
    manager.update_driver("driver0", (9.0, 8.0))
    manager.update_driver("driver2", (9.0, 9.0))

    manager.delete_driver("driver2")

    second_session = DriverManager(storage_path=storage_path)
    assert second_session.drivers == {"driver0": (9.0, 8.0)}


def test_exercise_example_works_correctly(storage_path):
    manager = DriverManager(storage_path=storage_path)
    manager.update_driver("driver0", (0.0, 0.0))
    manager.update_driver("driver1", (10.0, 10.0))
    manager.update_driver("driver2", (9.0, 9.0))
    manager.update_driver("driver0", (9.0, 8.0))
    manager.delete_driver("driver2")

    assert manager.find_closest_driver((9.0, 9.0)) == "driver0"