import time
import os
import shutil
import os.path
import subprocess
import raspicam

class Environment:
    temp_dir = "tmp"
    save_dir = "final_images"

    def __init__(self):
        self.temp_file_counter = 0
        camconfig = raspicam.RaspiCameraConfig()
        camconfig.set_metering_mode(raspicam.RaspiCameraConfig.METERING_MODE_AVERAGE)
        self.cam = raspicam.RaspiCamera(camconfig)

    def start(self):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def make_temp_file_name(self, extension):
        self.temp_file_counter += 1
        return "%s/image_cnt%d_time%d.%s" % (self.temp_dir, self.temp_file_counter, int(time.time()), extension)

    def capture_camera_image_into(self, file_name):
        self.cam.capture_image_into_file(file_name)
        return file_name

    def capture_camera_image_into_temp_file(self, extension = "jpg"):
        fn = self.make_temp_file_name(extension)
        return self.capture_camera_image_into(fn)

    def cleanup_temp_files(self):
        for f in os.listdir(self.temp_dir):
            os.remove("%s/%s" % (self.temp_dir, f))

    def save_file_for_later(self, file_name):
        imgutil.rotate_image_file_90_degrees_right(file_name)
        self.expose_file_via_webserver(file_name)
        shutil.move(file_name, self.save_dir)

    def expose_file_via_webserver(self, file_name):
        shutil.copy(file_name, "/home/pi/public_html/fridge.jpg")

    def expose_directory_via_webserver(self, path):
        dest_path = "/home/pi/public_html/fridge-pi"
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        shutil.copytree(path, dest_path)

    def started_collecting_images(self):
        return time.time()

    def should_stop_collecting_images(self, started_when):
        elapsed = time.time() - started_when
        return elapsed > 5*60

    def wait_between_idle_camera_captures(self):
        time.sleep(1)

    def wait_between_active_camera_captures(self):
        pass

class TestEnvironment(Environment):
    sharp_test_image = "img2_sharp.jpg"
    test_images = [ "test_images/img0_dark.jpg",
                    "test_images/img1_blurry.jpg",
                    "test_images/%s" % sharp_test_image,
                    "test_images/img3_blurry.jpg",
                    "test_images/img0_dark.jpg"]

    def __init__(self):
        Environment.__init__(self)
        self.current_test_image_index = 0
        self.test_file_names = {}

    def start(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        if os.path.exists(self.save_dir):
            shutil.rmtree(self.save_dir)
        Environment.start(self)

    def capture_camera_image_into(self, file_name):
        if self.should_stop_collecting_images(0):
            raise Exception("Ran out of test images!!!")
        next_test_image = self.test_images[self.current_test_image_index]
        self.test_file_names[os.path.basename(file_name)] = os.path.basename(next_test_image)
        shutil.copy(next_test_image, file_name)
        self.current_test_image_index = self.current_test_image_index + 1
        print "DEBUG: 'captured' test image [%s] into file [%s]" % (next_test_image, file_name)
        return file_name

    def wait_between_idle_camera_captures(self):
        pass

    def wait_between_active_camera_captures(self):
        pass

    def started_collecting_images(self):
        pass

    def should_stop_collecting_images(self, started_when):
        return self.current_test_image_index >= len(self.test_images)

    def original_test_file_name(self, file_name):
        return self.test_file_names[os.path.basename(file_name)]

    def expose_file_via_webserver(self, file_name):
        pass
