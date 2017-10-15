#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import cv2
from time import *
import numpy

# Callback Function for Trackbar (but do not any work)
def nothing(*arg):
    pass


cv2.namedWindow("capture")
cv2.createTrackbar("Treshold", "capture", 100, 255, nothing)

capture = cv2.VideoCapture(0)

width = 640
height = 480
k_senseble = 0
score = 0
font = cv2.FONT_HERSHEY_SIMPLEX



def make_mask(dframe):
	targets = []
	width, height = 640, 480

	for y in range(0, height):
		for x in range(0, width):
			if dframe[y][x] == 255: #check if zone filled
				mask = numpy.zeros((height + 2, width + 2), numpy.uint8) #создаем массив с будущей зоной\\create zone list
				cv2.floodFill(dframe, mask, (x,y), 10) #fill the zone and repaint it in gray(10)
				targets.append((mask[0:height, 0:width], sum(sum(mask)))) #save the size of zone and mask
	
	
	print("ready")
	return targets







	
while cv2.waitKey(1) != 32: #spacebar
	k_tresh = cv2.getTrackbarPos("Treshold", "capture")
	cframe = capture.read()[1]
	gframe = cv2.cvtColor(cframe, cv2.COLOR_RGB2GRAY)
	value, tframe = cv2.threshold(gframe, k_tresh, 255, cv2.THRESH_BINARY)
	cv2.imshow("capture", tframe)


		


targets = make_mask(tframe)




pframe = capture.read()[1]
pframe = cv2.cvtColor(pframe, cv2.COLOR_RGB2GRAY)

while True:
	
	cframe = capture.read()[1]
	gframe = cv2.cvtColor(cframe, cv2.COLOR_RGB2GRAY)
	dframe = cv2.absdiff(gframe,pframe)
	value, tframe = cv2.threshold(dframe, 70, 255, cv2.THRESH_BINARY)

	

	d = []
	y = 0

	for i in range(1, len(targets)):
		d.append(sum(sum(tframe&targets[i][0])))


	
	c = max(d)
	s = d.index(c)
	if c > k_senseble:
		print(s)
		score += 1
		sleep(0.1)
		
	
		
	cv2.putText(tframe, "score %i"%score, (4,460), font, 1, [255])
	cv2.imshow("capture", tframe)
	pframe = gframe

	if cv2.waitKey(1) == 27:
		break

cv2.ReleaseCapture(capture)
cv2.DestroyWindow("capture")


