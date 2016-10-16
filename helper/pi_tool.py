import cv2
import numpy as np

class PiTool:
  RESOLUTION_5MP=(2560, 1920)
  RESOLUTION_1080P=(1920,1088)
  RESOLUTION_720P=(1280,720)

  RESOLUTION_SQ_L=(1920,1904)
  RESOLUTION_SQ_M=(1088,1088)
  RESOLUTION_SQ_S=(736,720)
  RESOLUTION_SQ_X=(320,304)

  @staticmethod
  def get_doorhole_roi(image):
    filtered = PiTool.circle_vision_filter(image)
    (h,w)=filtered.shape
    # detect circles in the image
    circles = cv2.HoughCircles(filtered, cv2.HOUGH_GRADIENT, 1.2, int(w/10))

    # ensure at least some circles were found
    if circles is not None:
      # convert the (x, y) coordinates and radius of the circles to integers
      circles = np.round(circles[0, :]).astype("int")
      if len(circles) > 1:return image

      # loop over the (x, y) coordinates and radius of the circles
      for (x, y, r) in circles:
        image = image[y-r:y+r, x-r:x+r]
    return image

  @staticmethod
  def circle_vision_filter(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.blur(image, (40,40))
    ret,image = cv2.threshold(image,25,255,cv2.THRESH_BINARY)
    image = cv2.blur(image, (20,20))
    return image

  # input - gray image
  @staticmethod
  def find_circles(image):
    (h,w) = image.shape
    # detect circles in the image
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, int(w/10))

    # ensure at least some circles were found
    if circles is not None:
      # convert the (x, y) coordinates and radius of the circles to integers
      circles = np.round(circles[0, :]).astype("int")
      print("found Circles %s"%(len(circles)))
      # loop over the (x, y) coordinates and radius of the circles
      for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(image, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    return image

