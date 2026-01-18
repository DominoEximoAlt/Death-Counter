from deathcounter.utils.game_selector import start_selector
from deathcounter.utils.version import __version__

from dotenv import load_dotenv

if __name__ == "__main__":
    global game_exe

    load_dotenv()
    ##Start the selector to choose the game
    start_selector()
