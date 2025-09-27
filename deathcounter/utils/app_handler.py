from utils.overlay import *
import psutil  

def handle_app_event(event):
    if event == "START_OVERLAY":        
        start_overlay()
    elif event == "STOP_OVERLAY":
        stop_overlay()


def look_for_game_window():
    # Implement logic to look for the game window
    (p.name().__str__() for p in psutil.process_iter(attrs=['name']))