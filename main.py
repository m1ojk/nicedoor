#!/usr/bin/env python
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import logging

from models.sentry import Sentry
from helper.pi_tool import PiTool

logging.basicConfig(filename='log/main.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

SHOW_WINDOW = False
USE_CIRCLE_FIRST = False

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
(f_x, f_y) = PiTool.RESOLUTION_SQ_S
camera.resolution = (f_x, f_y)
camera.framerate = 15

rawCapture = PiRGBArray(camera, size=(f_x, f_y))

if SHOW_WINDOW:
  cv2.namedWindow("Frame",cv2.WINDOW_NORMAL)

# allow the camera to warmup
time.sleep(0.1)

guard = Sentry()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  image = frame.array

  if USE_CIRCLE_FIRST:
    image = PiTool.get_doorhole_roi(image)
  
  if guard.is_alert(image, True):
    #image = guard.get_pic_with_indicators()
    print(guard.alert_reason)
    PiTool.save_and_email(image, guard.alert_reason)
  image = guard.image
  key = cv2.waitKey(1) & 0xFF

  if SHOW_WINDOW:
    cv2.imshow("Frame", image)

  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)

  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break
