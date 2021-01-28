
import os


def dir_is_writable(path):
    """Checks to see if the given path is writable"""
    test_file_path = os.path.join(path, "DIR_WRITE_TEST.TESTING_123")

    try:
        with open(test_file_path, "w") as test:
            test.write("test")
    except IOError:
        return False
    finally:
        if os.path.isfile(test_file_path):
            os.remove(test_file_path)
    return True
