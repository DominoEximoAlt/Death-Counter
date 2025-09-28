import cv2
import numpy as np

def detect_death(currentFrame, game_name):
    img_rgb = currentFrame
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    template = cv2.imread(f"deathcounter/assets/{game_name}_cropped_template.png")
    assert template is not None, "file could not be read, check with os.path.exists()"
    ##w, h = template.shape[::-1]

    ##FEATURE MATCHING

    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template,None)
    kp2, des2 = sift.detectAndCompute(img_rgb,None)
    good = []
    # BFMatcher with default params
    if des1 is not None and des2 is not None:
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)  
        # Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)
    else:
        good.append(0)
        print("⚠️ No descriptors found in one of the images!")
        #print(type(des1), des1.shape if des1 is not None else "None")
        #print(type(des2), des2.shape if des2 is not None else "None")
        
    # cv2.drawMatchesKnn expects list of lists as matches.
    #img3 = cv2.drawMatchesKnn(template,kp1,img_rgb,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    ##TEMPLATE MATCHING
    ##res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED, None, template)
    ##threshold = 0.7
    ##loc = np.where( res >= threshold)
    ##for pt in zip(*loc[::-1]):
    ##    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    
    return good.__len__()