import cv2
import cv

def compute_average_light_value(img_gray):
    return int(cv2.mean(img_gray)[0])

def compute_sharpness_value(img_gray):
    img_lap = cv2.Laplacian(img_gray, cv.CV_16S, ksize=1, scale=1, delta=0)
    row_lap = cv2.reduce(img_lap, 0, cv.CV_REDUCE_MAX)
    point_lap = cv2.reduce(row_lap, 1, cv.CV_REDUCE_MAX)[0][0]
    return int(point_lap)

def read_img_gray(file_name):
    return cv2.imread(file_name, cv.CV_LOAD_IMAGE_GRAYSCALE)

def rotate_image_file_90_degrees_right(file_name):
    src = cv2.imread(file_name, 1)
    dst = cv2.transpose(src)
    cv2.imwrite(file_name, dst)

class Image:
    def __init__(self, file_name):
        img_gray = read_img_gray(file_name)
        self.average_light_value = compute_average_light_value(img_gray)
        self.sharpness_value = compute_sharpness_value(img_gray)
        self.file_name = file_name

def is_dark(img):
    return img.average_light_value < 25

def is_not_dark(img):
    return img.average_light_value > 25

def compare_image(first_image):
    return ImageComparator(first_image)

class ImageComparator:
    def __init__(self, first_image):
        self.first_image = first_image

    def is_sharper_than(self, second_image):
        return self.first_image.sharpness_value > second_image.sharpness_value
