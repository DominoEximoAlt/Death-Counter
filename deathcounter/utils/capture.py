import os
import mss
import time
import numpy as np

from utils.handle_death import add_death

from .detector import detect_death
from dotenv import load_dotenv
import ctypes
    
load_dotenv()

def capture_screen(game_name):

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    with mss.mss() as sct:

        monitor_number = int(os.getenv("CAPTURE_MONITOR"))
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top":      mon["top"],  # 100px from the top
            "left":     mon["left"] +  int(0.2 *screensize[0]),  # 100px from the left
            "width":    int(0.6 *screensize[0]),
            "height":   screensize[1],
            "mon":      monitor_number,
        }

        while True:

            # Get raw pixels from the screen, save it to a Numpy array
            frame = np.array(sct.grab(monitor))
            match_value = detect_death(frame, game_name)

            if match_value > 28:
                add_death()
                time.sleep(10)  # to avoid multiple detections in a short time

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


