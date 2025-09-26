
import os
import cv2
import mss
import time
import numpy as np
from .detector import detect_death

def capture_screen():

    with mss.mss() as sct:
        
        monitor_number = 2
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top":      mon["top"] + 0,  # 100px from the top
            "left":     mon["left"] + 400,  # 100px from the left
            "width":    1000,
            "height":   1000,
            "mon":      monitor_number,
        }

        while "Screen capturing":
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            frame = np.array(sct.grab(monitor))
            match_value = detect_death(frame)

            if match_value > 28:
                return True

            # Display the picture
            #cv2.imshow("OpenCV/Numpy normal", frame)

            # Display the picture in grayscale
            ##cv2.imshow('OpenCV/Numpy grayscale',
            ##            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))



            # Press "q" to quit
            #if cv2.waitKey(25) & 0xFF == ord("q"):
            #    cv2.destroyAllWindows()
            #    break


