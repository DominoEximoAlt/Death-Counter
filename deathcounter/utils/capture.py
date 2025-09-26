
import cv2
import mss
import time
import numpy as np
##from ..configuration.config import CAPTURE_MONITOR

def capture_screen():

    with mss.mss() as sct:
        
        monitor_number = 1
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
            img = np.array(sct.grab(monitor))

            # Display the picture
            cv2.imshow("OpenCV/Numpy normal", img)

            # Display the picture in grayscale
            # cv2.imshow('OpenCV/Numpy grayscale',
            #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

            print(f"fps: {1 / (time.time() - last_time)}")

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break