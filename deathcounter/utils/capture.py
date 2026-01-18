import os
import mss
import gc
import time
import hashlib
import numpy as np

from deathcounter.utils.handle_death import add_death
from deathcounter.utils.timer import Timer
from .detector import detect_death
from dotenv import load_dotenv
import ctypes
    
load_dotenv()

def capture_screen(game_name, selected_monitor):
    was_dead = False
    match_avg = []
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    t = Timer.get_instance(game_name)
    with mss.mss() as sct:

        monitor_number = int(selected_monitor)
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top":      mon["top"],  # 100px from the top
            "left":     mon["left"] +  int(0.2 *screensize[0]),  # 100px from the left
            "width":    int(0.6 *screensize[0]),
            "height":   screensize[1],
            "mon":      monitor_number,
        }
        prev_hash = None
        while True:
            if match_avg.__len__() >1:
                if was_dead and (sum(match_avg) / len(match_avg)) <= 10:
                    was_dead = False
            
            last_gc = time.time()
            # Get raw pixels from the screen, save it to a Numpy array
            frame = np.array(sct.grab(monitor))
            new_hash = hashlib.md5(frame).hexdigest()
            
                
            if new_hash != prev_hash:
                prev_hash = new_hash
                match_value = detect_death(frame, game_name)
                match_avg.append(match_value)
                if len(match_avg) > 10:
                    match_avg.pop(0)
                del frame

                if time.time() - last_gc > 10:
                    gc.collect()
                    last_gc = time.time()

                if match_value > 128 and t.is_running and not was_dead:
                    add_death()
                    print("Death detected")
                    was_dead = True
                    t._persist()
                
            print(was_dead, match_avg)

            


