#!/usr/bin/env python

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from helper.pi_tool import PiTool

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = PiTool.RESOLUTION_SQ_L
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.3)
# grab an image from the camera

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

sim = PiTool.circle_vision_filter(image)
sim = PiTool.find_circles(sim)

image = PiTool.get_doorhole_roi(image)

# display the image on screen and wait for a keypress
cv2.namedWindow("Image",cv2.WINDOW_NORMAL) 
cv2.namedWindow("Vision",cv2.WINDOW_NORMAL) 

cv2.imshow("Image", image)
cv2.imshow("Vision", sim)

cv2.waitKey(0)

