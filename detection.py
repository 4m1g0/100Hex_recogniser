import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
MIN_MATCH_COUNT = 7

img = cv2.imread('full_mask.jpg',0)          # queryImage
imgOrg = cv2.imread('full_mask.jpg',1)   
# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp2, des2 = sift.detectAndCompute(img,None)
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

directory = os.fsencode("images")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith(".png"): 
        continue
    img1 = cv2.imread("images/" + filename,0) # trainImage
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    matches = flann.knnMatch(des1,des2,k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    
    img2 = imgOrg.copy()
    if len(good)>MIN_MATCH_COUNT:
        #print(filename)
        #continue
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        h,w = img1.shape[::-1]
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        try:
            dst = cv2.perspectiveTransform(pts,M)
        except:
            print(filename + ": FAILED")
            continue
        img2 = cv2.polylines(img2,[np.int32(dst)],True,(255, 0, 0),5, cv2.LINE_AA)
        print(filename + ": FOUND!")
    else:
        #continue
        print(filename + ": Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    plt.imshow(img3),plt.show()
