#!/usr/bin/env python

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from helper.pi_tool import PiTool

def save_and_email(image):
  t=time.strftime("%d-%m-%y.%H_%M_%S")
  path = "/home/pi/Pictures/img.%s.png"%(t)
  cv2.imwrite(path, image)
  PiEmail.email_attachment(path)

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
