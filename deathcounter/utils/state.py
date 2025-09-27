import os, json
from appdirs import user_data_dir

APP_NAME = "DeathCounter"
APP_AUTHOR = "YourName"

SAVE_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
os.makedirs(SAVE_DIR, exist_ok=True)

SAVE_FILE = os.path.join(SAVE_DIR, "data.json")

def initialize_state():
    """Initialize state file if it doesn't exist."""
    initial_state = {"deaths": 0, "elapsed": 0}
    try:
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    except OSError:
        pass
    save_state(initial_state)

def load_state():
    """Load saved state from JSON (deaths, elapsed)."""
    if os.path.exists(SAVE_DIR):
        with open(SAVE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"deaths": 0, "elapsed": 0}
    else:
        initialize_state()
        return {"deaths": 0, "elapsed": 0}


def save_state(state):
    """Save state dict to JSON."""
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)


