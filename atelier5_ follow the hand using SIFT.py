#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# follow the hand using SIFT points of interest

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# subtract the background using MOG2
mog2 = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=20, detectShadows=True)

# ORB: An effective alternative to SIFT or SURF
# to find the key points
sift = cv2.ORB_create(nfeatures=2000)

while True:
    _, frame = cap.read()

    # get the foreground mask
    mask = mog2.apply(frame)

    # for morphological transformations: openness
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # to find the key points
    pc, des = sift.detectAndCompute(mask, None)

    # to draw small circles on key point locations
    img = cv2.drawKeypoints(mask, pc, None)

    cv2.imshow('hand tracking', img)

    if cv2.waitKey(30) == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()
