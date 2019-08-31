#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# foreground/background segmentation using image difference,time derivation,moving average,Running Average,median filter:

import cv2
import numpy as np

method = 2

# image of the grayscale background, with a reduction of image noise
background = cv2.imread("background.png")
background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background_gray = cv2.GaussianBlur(background_gray, (5, 5), 0)

cap = cv2.VideoCapture("highway.mp4")

# using the image difference:
if method == 1:
    while cap.isOpened():
        _, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        # calculates the absolute difference between two images
        difference = cv2.absdiff(background_gray, gray_frame)

        # thresholding (binarization)
        _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)

        cv2.imshow("Background", background_gray)
        cv2.imshow("video", gray_frame)
        cv2.imshow("the image difference", difference)

        if cv2.waitKey(30) == ord('e'):
            break

# using time derivation
elif method == 2:
    n = 0
    _, bg = cap.read()
    bg_gray = cv2.cvtColor(bg, cv2.COLOR_RGB2GRAY)
    while True:
        n = n + 1
        if n == 12:
            _, bg = cap.read()
            bg_gray = cv2.cvtColor(bg, cv2.COLOR_RGB2GRAY)
            n = 0

        _, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        difference = cv2.absdiff(frame_gray, bg_gray)
        _, difference = cv2.threshold(difference, 32, 255, cv2.THRESH_BINARY)
        cv2.imshow('video', frame)
        cv2.imshow('time derivation', difference)

        if cv2.waitKey(30) == ord('e'):
            break

# using the moving average:
elif method == 3:
    empty = 0

# using The Running Average:
elif method == 4:
    avg1 = np.float32(background)
    avg2 = np.float32(background)

    while 1:
        _, frame = cap.read()

        # RunningAvg: dst = (1-alpha)*dst+(alpha*src)
        cv2.accumulateWeighted(frame, avg1, 0.1)
        cv2.accumulateWeighted(frame, avg2, 0.01)

        # convertScaleAbs(float_image): calcule les valeurs absolues et convertit le résultat en 8 bits
        res1 = cv2.convertScaleAbs(avg1)
        res2 = cv2.convertScaleAbs(avg2)

        cv2.imshow('Background', background)
        cv2.imshow('Running Average 1', res1)
        cv2.imshow('Running Average 2', res2)

        if cv2.waitKey(30) == ord('e'):
            break


# using the median filter:
elif method == 5:
    n = 0
    _, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    list_img = [frame_gray]
    while True:
        _, img = cap.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        median = np.zeros_like(img_gray)
        if n < 10:
            np_list_img = np.array(list_img)
            median = np.median(np_list_img, axis=0)
            median = cv2.convertScaleAbs(median)
            list_img.append(median)
            n = n + 1

        else:
            np_list_img = np.array(list_img)
            median = np.median(np_list_img, axis=0)
            median = cv2.convertScaleAbs(median)
            list_img.pop(0)
            list_img.append(img_gray)

        difference = cv2.absdiff(img_gray, median)
        _, difference = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

        cv2.imshow('median filter', difference)
        cv2.imshow('Background', median)

        if cv2.waitKey(30) == ord('e'):
            break

else:
    print("please choose between 1 and 5")

cap.release()
cv2.destroyAllWindows()
