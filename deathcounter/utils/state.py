import os, json
from appdirs import user_data_dir
from deathcounter.utils.game_selector import game_exe

APP_NAME = "DeathCounter"
APP_AUTHOR = "SaveData"

SAVE_DIR = user_data_dir(APP_AUTHOR, APP_NAME)
os.makedirs(SAVE_DIR, exist_ok=True)

SAVE_FILE = os.path.join(SAVE_DIR, "_data.json")

def initialize_state(game_name=None):
    # Initialize state file if it doesn't exist.
    SAVE_FILE = os.path.join(SAVE_DIR, f"{game_name}_data.json")
    initial_state = {"deaths": 0, "elapsed": 0}
    try:
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    except OSError:
        pass
    save_state(initial_state, game_name=game_name)

def load_state(game_name):
    # Load saved state from JSON (deaths, elapsed).
    SAVE_FILE = os.path.join(SAVE_DIR, f"{game_name}_data.json")
    if os.path.exists(SAVE_FILE):

        with open(SAVE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"deaths": 0, "elapsed": 0}
    else:
        initialize_state(game_name=game_name)
        return {"deaths": 0, "elapsed": 0}


def save_state(state, game_name=None):
    # Save state dict to JSON.
    SAVE_FILE = os.path.join(SAVE_DIR, f"{game_name}_data.json") if game_name else SAVE_FILE
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)


