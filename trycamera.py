import env
import raspicam
import shutil
import os


def main():
    global env
    env = env.Environment()
    temp_dir = prepare_temp_dir()
    take_pictures_and_make_html(temp_dir)
    env.expose_directory_via_webserver(temp_dir)

def prepare_temp_dir():
    dir = './camera_demo'
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    return dir

def take_pictures_and_make_html(temp_dir):
    html = HtmlResult(temp_dir)
    cam = raspicam.RaspiCamera()
    html.begin()
    for m in raspicam.RaspiCameraConfig.ALL_METERING_MODES:
        print("Taking picture with %s metering mode..." % m)
        fn = "%s/%s_image.jpg" % (temp_dir, m)
        cam.capture_image_into_file(fn, raspicam.RaspiCameraConfig(mm = m, rotation_degrees = 90))
        html.add_image_with_description(fn, "Image captured with '%s' metering mode:" % m)
    html.end()


class HtmlResult:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir
        self.html_file = open("%s/camera.html" % temp_dir, 'w')

    def begin(self):
        self.html_file.write("<html><head><title>Raspberry Pi camera test</title></head>\n")
        self.html_file.write("<body>\n")

    def add_image_with_description(self, image_file_name, desc):
	file_basename = os.path.basename(image_file_name)
        self.html_file.write("<br/><p>%s</p>\n" % desc)
        self.html_file.write("<a href='%s'><img width='33%%' src='%s'></a>\n" % (file_basename, file_basename))
        self.html_file.write("<hr>\n")

    def end(self):
        self.html_file.write("</body></html>")
        self.html_file.close()

if __name__ == "__main__":
    main()
