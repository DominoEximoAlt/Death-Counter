import cv2
import sys, os
import numpy as np

_SIFT = cv2.SIFT_create()
_BF = cv2.BFMatcher()

_TEMPLATE_CACHE = {}
'''
def detect_death(currentFrame, game_name):
    img_rgb = currentFrame
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    template_path = resource_path(f"deathcounter\\assets\\{game_name}_cropped_template.png")
    template = cv2.imread(template_path)
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
        try:
            
            if matches.__len__() > 1:
                print(matches.__len__())
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append(m)
        except ValueError:
            pass
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
    cv2.destroyAllWindows()
    return good.__len__()
 '''  
def detect_death(gray_frame, game_name: str) -> int:
    """
    Returns number of good SIFT matches.
    gray_frame MUST be grayscale.
    """

    _, _, des1 = _load_template(game_name)

    # Downscale frame to reduce SIFT cost
    frame_small = cv2.resize(gray_frame, None, fx=0.5, fy=0.5)

    kp2, des2 = _SIFT.detectAndCompute(frame_small, None)
    if des2 is None:
        return 0

    matches = _BF.knnMatch(des1, des2, k=2)

    good = 0

    try:
        

        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good += 1

        return good
    except ValueError:
        pass

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def _load_template(game_name: str):
    if game_name in _TEMPLATE_CACHE:
        return _TEMPLATE_CACHE[game_name]

    path = resource_path(f"deathcounter/assets/{game_name}_cropped_template.png")

    template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise RuntimeError(f"Template not found: {path}")

    kp, des = _SIFT.detectAndCompute(template, None)
    if des is None:
        raise RuntimeError(f"No descriptors in template: {path}")

    _TEMPLATE_CACHE[game_name] = (template, kp, des)
    return template, kp, des