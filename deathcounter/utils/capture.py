import os
import mss
import gc
import time
import hashlib
import numpy as np

from utils.handle_death import add_death

from .detector import detect_death
from dotenv import load_dotenv
import ctypes
    
load_dotenv()

def capture_screen(game_name, selected_monitor):

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

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
            last_gc = time.time()
            # Get raw pixels from the screen, save it to a Numpy array
            frame = np.array(sct.grab(monitor))
            new_hash = hashlib.md5(frame).hexdigest()
            if new_hash != prev_hash:
                prev_hash = new_hash
                match_value = detect_death(frame, game_name)
                del frame

                if time.time() - last_gc > 10:
                    gc.collect()
                    last_gc = time.time()

                if match_value > 28:
                    add_death()
                    time.sleep(14)  # to avoid multiple detections in a short time

            
            # Display the picture
            #cv2.imshow("OpenCV/Numpy normal", frame)
            print(match_value)
            # Display the picture in grayscale
            #cv2.imshow('OpenCV/Numpy grayscale',
            #            cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY))



            # Press "q" to quit
            #if cv2.waitKey(25) & 0xFF == ord("q"):
            #    cv2.destroyAllWindows()
            #    break


