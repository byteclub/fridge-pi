import main
import env
import os
import logging

def test_main():
    e = env.TestEnvironment()
    main.setup_simple_debug_console_logger()
    main.main(e, main.do_not_loop_forever)

    final_files = os.listdir(e.save_dir)

    if len(final_files) != 1:
        raise Exception("TEST FAILED: expected 1 image file in [%s], but found %d" % (e.save_dir, len(final_files)))

    original_name = e.original_test_file_name(final_files[0])
    if original_name != e.sharp_test_image:
        raise Exception("TEST FAILED: wrong image selected by algorithm! Expected [%s], but got [%s]" % (e.sharp_test_image, final_files[0]))

    temp_files = os.listdir(e.temp_dir)
    if len(temp_files) > 0:
        raise Exception("TEST FAILED: main didn't clean temp files after itself")

def test_env():
    e = env.Environment()
    fn = e.make_temp_file_name('txt')
    f = open(fn, "w")
    f.write("test")
    f.close
    if not os.path.exists(fn):
        raise Exception("TEST FAILED: temp file was created and written to, but cannot be found [%s]" % fn)
    e.cleanup_temp_files()
    if os.path.exists(fn):
        raise Exception("TEST FAILED: env cleaned up temp files, but our file was left behind [%s]" % fn)

if __name__ == '__main__':
    test_main()
    test_env()
    print "TESTS PASSED!"
