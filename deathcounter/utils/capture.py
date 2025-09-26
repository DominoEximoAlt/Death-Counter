
import os
import cv2
import mss
import time
import numpy as np
##from ..configuration.config import CAPTURE_MONITOR

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
            img = np.array(sct.grab(monitor))
            img = compare_images(img)

            # Display the picture
            cv2.imshow("OpenCV/Numpy normal", img)

            # Display the picture in grayscale
            ##cv2.imshow('OpenCV/Numpy grayscale',
            ##            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))



            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


def compare_images(currentFrame):
    img_rgb = currentFrame
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("deathcounter/assets/dark_souls_death_test1.png")
    os.path.exists("deathcounter/assets/cropped_template.png")
    assert template is not None, "file could not be read, check with os.path.exists()"
    ##w, h = template.shape[::-1]

    ##FEATURE MATCHING

    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template,None)
    kp2, des2 = sift.detectAndCompute(img_rgb,None)
    
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
        
    # cv.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(template,kp1,img_rgb,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    ##TEMPLATE MATCHING
    ##res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED, None, template)
    ##threshold = 0.7
    ##loc = np.where( res >= threshold)
    ##for pt in zip(*loc[::-1]):
    ##    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    
    if good.__len__() > 28:
        print("DEATH DETECTED")
    print(good.__len__())
    return img3