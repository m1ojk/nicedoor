import cv2
import time

class Sentry:
  #__face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
  __face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
  #__face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')
  __eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
  __ALERT_INTERVAL = 5

  def __init__(self):
    self.face_count = 0
    self.image = None#cv2.imread('notfound.jpg',0)
    self.alert_reason = None

    self.__alert_time = 0.0
    self.__alert_face_count = 0
    self.__faces = None

  def is_alert(self, image, indicate=False):
    is_detected = self.__is_face_detected(image, indicate)
    should_alert = self.__should_alert()
    # print("Detected: %r  alert: %r"%(is_detected, should_alert))
    return is_detected and should_alert

  def __is_face_detected(self, image, indicate):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = self.__face_cascade.detectMultiScale(gray, 1.2, 2)
    self.face_count = len(faces)
    self.image = image

    if self.face_count > 0:
      self.__faces = faces
      if indicate:
        for (x,y,w,h) in self.__faces:
          self.image = cv2.rectangle(self.image,(x,y),(x+w,y+h),(200,10,10),2)


    return self.face_count > 0

  # Alert Requirements
  # - No alert - when no faces were detected currently and previously
  # - alert - first time face_count is different than previous
  # -       - If face_count is same as before and not 0, then alert every 5 seconds
  def __should_alert(self):
    if self.face_count == 0 and self.__alert_face_count == 0: return False

    if self.face_count != self.__alert_face_count :
      self.alert_reason = "Face count was %s but is now %s"%(self.__alert_face_count, self.face_count)
      self.__alert_face_count = self.face_count
      self.__alert_time = time.perf_counter()
      return True

    duration = int(time.perf_counter() - self.__alert_time)
    if duration > self.__ALERT_INTERVAL:
      self.alert_reason = "Duration is greater than %s"%self.__ALERT_INTERVAL
      self.__alert_time = time.perf_counter()
    return duration > self.__ALERT_INTERVAL


