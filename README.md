## Cabify Exercise: Driver Manager

This project implements a small Python module to manage driver locations for the Cabify Rookie Excellence Program technical assessment.

You can find the full project at: https://github.com/jgculebras/CabifyExercise

### What it does

- Updates a driver's location, creating the driver if it does not already exist.
- Stops tracking a driver.
- Finds the closest tracked driver to a given location.
- Persists driver locations to a JSON file between sessions.

### Design choices

- Driver IDs are stored as strings.
- Locations are represented as `(latitude, longitude)` tuples of floats.
- Persistence is file-based and uses a JSON object mapping each driver ID to a two-element coordinate array.
- If the storage file does not exist yet, the manager starts with an empty state and creates the file on the first write.
- Invalid JSON content raises a `ValueError` to avoid silently accepting corrupted persisted data.
- Distance is calculated with: `abs(x1 - x2) + abs(y1 - y2)`.

### Project structure

- `src/drivermanager.py`: main implementation.
- `tests/test_drivermanager.py`: tests for behavior and persistence.
- `requirements.txt`: test dependency list.

### Run locally

Create a new venv:

```bash
python -m venv venv
```

Activate the venv:

```bash
# Windows
venv\Scripts\Activate.ps1

# Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest tests
```

### Notes

This solution keeps persistence simple and explicit by writing to `drivers.json`, while still allowing a custom storage path to be injected for tests.

### Possible improvements

- Add a CLI using `Click` so users can run commands such as `update`, `stop-tracking`, and `find-closest` from the terminal in a more comfortable way.