from utils.overlay import start_overlay

from dotenv import load_dotenv
from configuration import config

if __name__ == "__main__":
    load_dotenv()
    ##Start the overlay
    start_overlay()