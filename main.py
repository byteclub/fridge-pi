import logging
from env import Environment
from imgutil import Image, is_dark, is_not_dark, compare_image

do_not_loop_forever = False
logger = logging.getLogger('fridge-pi')

def main(e, loop_forever = True):
    # Initialize our environment
    global env
    env = e
    env.start()

    # Don't start taking pics until we are inside of an actual fridge
    # which is presumably dark (or somebody is testing us)
    wait_for_dark_image()
    while(True):
        images = get_best_images()
        save_images(images)
        if not loop_forever:
            break

def wait_for_dark_image():
    wait_for_image_that(is_dark)
    env.cleanup_temp_files

def get_best_images():
    logger.debug('Waiting for dark image')
    best_img = wait_for_image_that(is_not_dark)
    logger.debug('Got dark image. Starting image selection')
    started = env.started_collecting_images()
    while(True):
        next_img = Image(env.capture_camera_image_into_temp_file())
        if is_dark(next_img):
            logger.debug('Stopping image selection, got dark image')
            break
        if compare_image(next_img).is_sharper_than(best_img):
            logger.debug('Found a better image [%s]' % next_img.file_name)
            best_img = next_img
        if env.should_stop_collecting_images(started):
            logger.debug('Stopping image selection, got signal from env')
            break
        env.wait_between_active_camera_captures()
    logger.debug('FINAL image in this iteration found! [%s]' % best_img.file_name)
    return [best_img]

def save_images(images):
    for i in images:
        env.save_file_for_later(i.file_name)
    env.cleanup_temp_files()

def wait_for_image_that(meets_criteria):
    while(True):
        env.cleanup_temp_files
        img = Image(env.capture_camera_image_into_temp_file())
        if meets_criteria(img):
            return img
        env.wait_between_camera_captures()

def setup_simple_debug_console_logger():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

if __name__ == "__main__":
    setup_simple_debug_console_logger()
    main(Environment())
