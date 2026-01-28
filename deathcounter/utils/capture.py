import os
import mss
import gc
import time
import hashlib
import numpy as np
import cv2

from .handle_death import add_death
from .timer import Timer
from .detector import detect_death
import ctypes

CAPTURE_INTERVAL = 0.2

def capture_screen(game_name, selected_monitor):
    was_dead = False
    match_avg = []
    prev_sig = None
    last = 0

    t = Timer.get_instance(game_name)

    with mss.mss() as sct:
        mon = sct.monitors[int(selected_monitor)]
        screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

        monitor = {
            "top": mon["top"],
            "left": mon["left"] + int(0.2 * screensize[0]),
            "width": int(0.6 * screensize[0]),
            "height": screensize[1],
            "mon": int(selected_monitor),
        }

        while True:
            now = time.perf_counter()
            if now - last < CAPTURE_INTERVAL:
                time.sleep(0.005)
                continue
            last = now

            frame = np.array(sct.grab(monitor), dtype=np.uint8)

            # 🔥 Convert early
            gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

            # 🔥 Cheap frame signature (not cryptographic)
            small = cv2.resize(gray, (64, 36))
            sig = small.mean()

            if sig == prev_sig:
                continue
            prev_sig = sig

            match_value = detect_death(gray, game_name)
            match_avg.append(match_value)
            if len(match_avg) > 10:
                match_avg.pop(0)
            
            try:
                avg_match = sum(match_avg) / len(match_avg)
            except TypeError:
                avg_match = 0

            if was_dead and avg_match < 10:
                was_dead = False

            if match_value >= 128 and t.is_running and not was_dead:
                add_death()
                was_dead = True
                t._persist()


