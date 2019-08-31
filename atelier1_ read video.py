#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Playing a video record on the hard drive

import cv2

# create a videoCapture object with a video file or a capture device
cap = cv2.VideoCapture('highway.mp4')

# check if we will successfully open the file
if not cap.isOpened():
    print("Error opening the file.")

# read until the end of the video frame by frame
while cap.isOpened():

    # cap.read (): decodes and returns the next video frame
    # variable ret: will get the return value by retrieving the camera frame, true or false (via "cap")
    # variable frame: will get the next image of the video (via "cap")
    ret, frame = cap.read()

    if ret:
        # color to grayscale
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # to display the frame
        cv2.imshow("video", frame)

        # waitKey (0): put the screen in pause because it will wait infinitely that key
        # waitKey (n): will wait for keyPress for only n milliseconds and continue to refresh and read the video frame using cap.read ()
        # ord (character): returns an integer representing the Unicode code point of the given Unicode character.
        if cv2.waitKey(1) == ord('e'):
            break
    else:
        break

# to release software and hardware resources
cap.release()

# to close all windows in imshow ()
cv2.destroyAllWindows()
