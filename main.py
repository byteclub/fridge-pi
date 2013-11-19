import cv2
import cv
import subprocess
import time
import os

class CameraImage:
  def __init__(self, file_name):
    self.img_gray = cv2.imread(file_name, cv.CV_LOAD_IMAGE_GRAYSCALE)
    self.file_name = file_name

  def averageLightValue(self):
    return cv2.mean(self.img_gray)

  def blurrinessValue(self):
    img_lap = cv2.Laplacian(self.img_gray, cv.CV_16S, ksize=1, scale=1, delta=0)
    return cv2.reduce(cv2.reduce(img_lap, 0, cv.CV_REDUCE_MAX), 1, cv.CV_REDUCE_MAX)[0][0]
    

class Camera:
  def capture_image(self):
    temp_file_name = "tmp/image_%d.jpg" % int(time.time())

    subprocess.call(["/usr/bin/raspistill", "-t", "0", "-o", temp_file_name])

    if not os.path.exists(temp_file_name):
      raise Exception("Called raspistill but can't find output file!")

    return CameraImage(temp_file_name)

def setup_app():
  if not os.path.exists("tmp"):
    os.makedirs("tmp")

# Main loop
setup_app()
cam = Camera()
img = cam.capture_image()
print "File: %s" % img.file_name
print "Light: %d" % img.averageLightValue()
print "Blur: %d" % img.blurrinessValue()
