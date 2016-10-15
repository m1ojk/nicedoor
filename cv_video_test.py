#!/usr/bin/env python
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

import helper.pi_email as pi_email
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

def save_and_email(image):
  t=time.strftime("%d-%m-%y.%H_%M_%S")
  path = "/home/pi/Pictures/img.%s.png"%(t)
  cv2.imwrite(path, image)
  pi_email.email_attachment(path)

def flip_upside_down(image):
  # grab the dimensions of the image and calculate the center
  # of the image
  (h, w) = image.shape[:2]
  center = (w / 2, h / 2)
 
  # rotate the image by 180 degrees
  M = cv2.getRotationMatrix2D(center, 180, 1.0)
  rotated = cv2.warpAffine(image, M, (w, h))
  return rotated

def draw(img):
  #img = cv2.line(img,(20,50),(511,511),(255,0,0),5)
  #img = cv2.circle(img,(447,63), 10, (0,0,255), -1)
  return img

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
#(f_x, f_y) = (1280,720)
(f_x, f_y) = (640,480)
camera.resolution = (f_x, f_y)
camera.framerate = 10

rawCapture = PiRGBArray(camera, size=(f_x, f_y))
cv2.namedWindow("Frame",cv2.WINDOW_AUTOSIZE)

cv2.moveWindow("Frame",int(screen_width/2 - f_x/2),int( screen_height/2 - f_y/2))
# allow the camera to warmup
time.sleep(0.1)
face_count = 0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  # grab the raw NumPy array representing the image, then initialize the timestamp
  # and occupied/unoccupied text
  image = frame.array
#  image = flip_upside_down(frame.array)
  image = draw(image)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, 1.2, 2)
  face_count = len(faces)
#  print("face-count: %s"%str(face_count))
  done = False
  for (x,y,w,h) in faces:
    save_and_email(image)
    done = True
    break
    image = cv2.rectangle(image,(x,y),(x+w,y+h),(200,10,10),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
      cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
  if done :
    break
  # show the frame
  cv2.imshow("Frame", image)
  key = cv2.waitKey(1) & 0xFF

  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)
 
  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break
