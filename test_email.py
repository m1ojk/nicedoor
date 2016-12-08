#!/usr/bin/env python

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import logging

from helper.pi_tool import PiTool

logging.basicConfig(filename='log/test_email.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = PiTool.RESOLUTION_SQ_L
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.3)
# grab an image from the camera

camera.capture(rawCapture, format="bgr")
#image = PiTool.get_roi_doorhole(rawCapture.array)
image = rawCapture.array
image = PiTool.get_doorhole_roi(image)

# display the image on screen and wait for a keypress
#cv2.imshow("Image", image)
#cv2.waitKey(0)

PiTool.save_and_email(image, "test_email")
