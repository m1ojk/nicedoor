#!/usr/bin/env python
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from helper.pi_tool import PiTool
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
#(f_x, f_y) = (112,112)
(f_x, f_y) = PiTool.RESOLUTION_SQ_S
camera.resolution = (f_x, f_y)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(f_x, f_y))
cv2.namedWindow("Frame",cv2.WINDOW_AUTOSIZE)
cv2.moveWindow("Frame",int(screen_width/2 - f_x/2),int( screen_height/2 - f_y/2))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  image = frame.array
  image = PiTool.circle_vision_filter(image)#find_circles(image)#get_roi_doorhole(image)
  image = PiTool.find_circles(image)
  cv2.imshow("Frame", image)
  key = cv2.waitKey(1) & 0xFF
  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)

  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break
