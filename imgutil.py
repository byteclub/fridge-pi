import cv2
import cv

def compute_average_light_value(img_gray):
  return int(cv2.mean(img_gray)[0])

def compute_sharpness_value(img_gray):
  img_lap = cv2.Laplacian(img_gray, cv.CV_16S, ksize=1, scale=1, delta=0)
  return int(cv2.reduce(cv2.reduce(img_lap, 0, cv.CV_REDUCE_MAX), 1, cv.CV_REDUCE_MAX)[0][0])

def read_img_gray(file_name):
  return img_gray = cv2.imread(file_name, cv.CV_LOAD_IMAGE_GRAYSCALE)

class Image:
  def __init__(self, file_name):
    img_gray = read_img_gray(file_name)
    self.average_light_value = get_average_light_value(img_gray)
    self.sharpness_value = get_sharpness_value(img_gray)
    self.file_name = file_name

def is_dark(img):
  return img.average_light_value < 25

def is_not_dark(img):
  return img.average_light_value > 25
