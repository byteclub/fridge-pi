from env import Environment

env = Environment()
file_name = env.capture_camera_image_into_temp_file()
env.save_file_for_later(file_name)

