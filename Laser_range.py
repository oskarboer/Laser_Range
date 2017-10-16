#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import cv2
import time
import numpy


# Callback Function for Trackbar (but do not any work)
def nothing(*arg):
    pass


cv2.namedWindow("capture")
cv2.createTrackbar("Threshold", "capture", 100, 255, nothing)

capture = cv2.VideoCapture(0)

score = 0
font = cv2.FONT_HERSHEY_SIMPLEX


def make_mask(dframe):
    targets = []
    height, width = dframe.shape[:2]

    for y in range(0, height):
        for x in range(0, width):
            if dframe[y][x] == 255:  # check if zone filled
                mask = numpy.zeros((height + 2, width + 2),
                                   numpy.uint8)  # создаем массив с будущей зоной\\create zone list
                cv2.floodFill(dframe, mask, (x, y), 10)  # fill the zone and repaint it in gray(10)
                targets.append((mask[1:(height + 1), 1:(width + 1)], sum(sum(mask))))  # save the size of zone and mask

    print("ready")
    return targets


while cv2.waitKey(1) != 32:  # space bar
    k_tresh = cv2.getTrackbarPos("Threshold", "capture")
    cframe = capture.read()[1]
    gframe = cv2.cvtColor(cframe, cv2.COLOR_RGB2GRAY)
    reval, tframe = cv2.threshold(gframe, k_tresh, 255, cv2.THRESH_BINARY)
    cv2.imshow("capture", tframe)

targets = make_mask(tframe)

pframe = capture.read()[1]
pframe = cv2.cvtColor(pframe, cv2.COLOR_RGB2GRAY)

height, width = pframe.shape[:2]
last_hit_target = 0
last_hit_time = 0

while True:

    cframe = capture.read()[1]
    gframe = cv2.cvtColor(cframe, cv2.COLOR_RGB2GRAY)
    dframe = cv2.absdiff(gframe, pframe)
    retval, tframe = cv2.threshold(dframe, 70, 255, cv2.THRESH_BINARY)

    results = []
    y = 0

    for i in range(0, len(targets)):
        results.append(sum(sum(tframe & targets[i][0])))

    max_number_of_pixels = max(results)

    shot_target_index = results.index(max_number_of_pixels)

    # check if there more then 10 pixels
    if ((max_number_of_pixels > 250) and ((abs(last_hit_time - time.time()) > 0.25) or (last_hit_time == 0))):
        print(shot_target_index)
        score += shot_target_index
        last_hit_time = time.time()

        # remember last successful hit
        if shot_target_index:
            last_hit_target = shot_target_index

    cv2.putText(tframe, "score %i" % score, (10, height - 20), font, 1, [255])
    cv2.putText(tframe, "Hit %i" % last_hit_target, (int(width / 2), height - 20), font, 1, [255])

    cv2.imshow("capture", tframe)
    pframe = gframe

    if cv2.waitKey(1) == 27:  # ESC
        break

capture.release()
cv2.destroyAllWindows()
