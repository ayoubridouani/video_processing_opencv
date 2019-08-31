#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# foreground/background segmentation MOG,MO2,GMG:

import cv2

method = 2

# creation of a videoCapture object with the opening of a video file or a capture device
cap = cv2.VideoCapture('highway.mp4')

# create the background subtraction object
if method == 1:
    bgSubtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

elif method == 2:
    bgSubtractor = cv2.createBackgroundSubtractorMOG2()

elif method == 3:
    bgSubtractor = cv2.bgsegm.createBackgroundSubtractorGMG()

else:
    print("please choose between 1 and 3")
    exit(0)

# create the kernel that will be used to remove the noise in the foreground mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while True:
    # get the next picture
    ret, frame = cap.read()

    if ret:
        # get the foreground mask
        foregroundMask = bgSubtractor.apply(frame)

        # remove some of the noise
        foregroundMask = cv2.morphologyEx(foregroundMask, cv2.MORPH_OPEN, kernel)

        cv2.imshow('subtraction', foregroundMask)

        if cv2.waitKey(30) == ord('e'):
            break

cap.release()
cv2.destroyAllWindows()
