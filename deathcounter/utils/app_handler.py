#from utils.overlay import *
import psutil  

#def stop_overlay():
    #raise NotImplementedError

#def handle_app_event(event):
    #if event == "START_OVERLAY":        
    #    start_overlay()
    #elif event == "STOP_OVERLAY":
    #    stop_overlay()


def look_for_game_window(game_process):
    # Implement logic to look for the game window
    for proc in psutil.process_iter(['name']):
        print(proc.info['name'])
        if proc.info['name'] == game_process:
            return True
    return False

print(look_for_game_window("LOTF2-Win64-Shipping.exe"))

