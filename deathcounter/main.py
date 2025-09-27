from utils import timer
from utils.app_handler import look_for_game_window
from utils.overlay import start_overlay

from dotenv import load_dotenv

if __name__ == "__main__":
    look_for_game_window()

    load_dotenv()
    ##Start the overlay
    start_overlay()