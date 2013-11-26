import os
import shutil

class Environment:
  temp_dir = "tmp"
  save_dir = "final_images"

  def __init__(self):
    if not os.path.exists(self.temp_dir):
      os.makedirs(self.temp_dir)
    if not os.path.exists(self.save_dir):
      os.makedirs(self.save_dir)

  def make_temp_file_name(self, extension):
    return "%s/image_%d.%s" % (self.temp_dir, int(time.time()), extension)

  def capture_camera_image_into(self, file_name):
    subprocess.call(["/usr/bin/raspistill", "-t", "0", "-o", file_name])
    if not os.path.exists(file_name):
      raise Exception("Called raspistill but can't find output file [%s]!" % file_name)
    return Image(file_name)

  def capture_camera_image_into_temp_file(self, extension = "jpg"):
    fn = make_temp_file_name(extension)
    self.capture_camera_image_into(fn)

  def cleanup_temp_files(self):
    os.remove(f) for f in os.listdir(temp_dir)

  def save_file_for_later(file_name):
    shutil.move(file_name, save_dir)
