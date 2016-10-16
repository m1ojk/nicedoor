#!/usr/bin/env python
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from models.sentry import Sentry
from helper.pi_email import PiEmail
from helper.pi_tool import PiTool
#import tkinter as tk

#root = tk.Tk()

#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()

def save_and_email(image, message):
  t=time.strftime("%d-%m-%y.%H_%M_%S")
  path = "/home/pi/Pictures/img.%s.png"%(t)
  cv2.imwrite(path, image)
  PiEmail.email_message_attachment(message, path)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
(f_x, f_y) = PiTool.RESOLUTION_SQ_M
camera.resolution = (f_x, f_y)
camera.framerate = 10

rawCapture = PiRGBArray(camera, size=(f_x, f_y))
#cv2.namedWindow("Frame",cv2.WINDOW_AUTOSIZE)
#cv2.moveWindow("Frame",int(screen_width/2 - f_x/2),int( screen_height/2 - f_y/2))

# allow the camera to warmup
time.sleep(0.1)

guard = Sentry()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  image = frame.array
  image = PiTool.get_doorhole_roi(image)
  if guard.is_alert(image, True):
    #image = guard.get_pic_with_indicators()
    print(guard.alert_reason)
    save_and_email(image, guard.alert_reason)
  image = guard.image
  key = cv2.waitKey(1) & 0xFF
  # cv2.imshow("Frame", image)
  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)

  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break
