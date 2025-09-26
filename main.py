import cv2
import numpy as np
import mss
import mss.tools
import time
import json
import os


with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": 100, "left": 450, "width": 1000, "height": 1000}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)