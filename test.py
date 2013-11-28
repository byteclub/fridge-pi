import main
import env
import os

e = env.TestEnvironment()
main.main(e, main.do_not_loop_forever)

final_files = os.listdir(e.save_dir)

if len(final_files) != 1:
    raise Exception("TEST FAILED: expected 1 image file in [%s], but found %d" % (e.save_dir, len(final_files)))

original_name = e.original_test_file_name(final_files[0])
if original_name != e.sharp_test_image:
    raise Exception("TEST FAILED: wrong image selected by algorithm! Expected [%s], but got [%s]" % (e.sharp_test_image, final_files[0]))

print "TEST PASSED!"

