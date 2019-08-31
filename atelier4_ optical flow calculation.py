#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# optical flow calculation

import numpy as np
import cv2

question = 2

cap = cv2.VideoCapture('highway.mp4')

# parameters for ShiTomasi corner detection
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# parameters for lucas kanade optics flow
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# creation of random colors
color = np.random.randint(0, 255, (100, 3))

# take the first picture in the video and find corners on it
_, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# determine the strong angles of an image
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# create a mask image for design purposesn
mask = np.zeros_like(old_frame)

while 1:
    if question == 1:
        for i in range(1, 5):
            ret, frame = cap.read()
    else:
        ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # optical flow calculation
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select the right points
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # draw the tracks (trackage)
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
    img = cv2.add(frame, mask)

    if question == 1:
        cv2.imshow('image en t=0', old_frame)
        cv2.imshow('image en t+5', img)
        cv2.waitKey(0)
        break
    else:
        cv2.imshow('optical flow', img)
        if cv2.waitKey(30) == ord('e'):
            break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cv2.destroyAllWindows()
cap.release()
