from env import Environment
import time
import Image from imgutils


class Main:
  def __init__(self, env):
    self.env = env

  def main(self):
    # Don't start taking pics until we are inside of an actual fridge
    # which is presumably dark (or somebody is testing us)
    self.wait_for_dark_image()
    while(true):
      images = self.get_best_images()
      self.save_images(images)

  def wait_for_dark_image(self):
    wait_for_image_that(imgutil.is_dark)
    self.env.clean_up_temp_files

  def get_best_images(self):
    file_name = wait_for_image_that(imgutil.is_not_dark)
    best_img = Image(file_name)
    start_time = time.time()
    while(true):
      next_img = self.env.capture_camera_image_into_temp_file()
      if imgutil.is_dark(next_img)
        break
      if next_img.sharpness_value > best_img.sharpness_value
        best_img = next_img
      if seconds_elapsed_since(start_time) > 5*60
        break
    [best_img]

  def save_images(self, images):
    self.env.save_file_for_later(i.file_name) for i in images
    self.env.cleanup_temp_files()

  def wait_for_image_that(meets_criteria):
    while(true):
      self.env.clean_up_temp_files
      img = self.env.capture_camera_image_into_temp_file()
      if meets_criteria(img)
        return img.file_name
      time.sleep(10)


def seconds_elapsed_since(timestamp):
  time.time() - timestamp

def quick_test():
  env = Environment()

  file_name = env.make_temp_file_name("jpg")
  img = env.capture_camera_image_into(file_name)

  print "File: %s" % img.file_name
  print "Light: %d" % img.average_light_value
  print "Blur: %d" % img.blurriness_value


# Start it up
if __name__=="__main__":
   main()
