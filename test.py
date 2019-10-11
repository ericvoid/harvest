import unittest

from harvest import harvest


def join(xs):
    return ''.join(xs)


class TestHarvest(unittest.TestCase):
    def test_specific_file(self):
        data = join(harvest('test_data/a.txt'))

        self.assertEqual("contents of test_data/a.txt\n", data)

    def test_specific_file_path_only(self):
        data = join(harvest('test_data/a.txt', paths_only=True))

        self.assertEqual("test_data/a.txt\n", data)


    def test_paths_only(self):
        data = join(harvest('test_data', ['.txt'], paths_only=True))

        self.assertEqual("""test_data/a.txt
test_data/b.txt
test_data/subdir1/a.txt
test_data/subdir1/b.txt
test_data/subdir1/c.txt
test_data/subdir2/a.txt
test_data/subdir2/b.txt
test_data/subdir2/subdir3/a.txt
test_data/subdir2/z.txt
test_data/y.txt
test_data/z.txt
""", data)

    def test_all_files(self):
        data = join(harvest('test_data', ['.txt']))

        self.assertEqual("""contents of test_data/a.txt
contents of test_data/b.txt
contents of test_data/subdir1/a.txt
contents of test_data/subdir1/b.txt
contents of test_data/subdir1/c.txt
contents of test_data/subdir2/a.txt
contents of test_data/subdir2/b.txt
contents of test_data/subdir2/subdir3/a.txt
contents of test_data/subdir2/z.txt
contents of test_data/y.txt
contents of test_data/z.txt
""", data)

    def test_sort_deepfirst(self):
        data = join(harvest('test_data', ['.txt'], glob_sort='depthfirst'))

        self.assertEqual("""contents of test_data/subdir1/a.txt
contents of test_data/subdir1/b.txt
contents of test_data/subdir1/c.txt
contents of test_data/subdir2/subdir3/a.txt
contents of test_data/subdir2/a.txt
contents of test_data/subdir2/b.txt
contents of test_data/subdir2/z.txt
contents of test_data/a.txt
contents of test_data/b.txt
contents of test_data/y.txt
contents of test_data/z.txt
""", data)

    def test_sort_shallowfirst(self):
        data = join(harvest('test_data', ['.txt'], glob_sort='shallowfirst'))

        self.assertEqual("""contents of test_data/a.txt
contents of test_data/b.txt
contents of test_data/y.txt
contents of test_data/z.txt
contents of test_data/subdir1/a.txt
contents of test_data/subdir1/b.txt
contents of test_data/subdir1/c.txt
contents of test_data/subdir2/a.txt
contents of test_data/subdir2/b.txt
contents of test_data/subdir2/z.txt
contents of test_data/subdir2/subdir3/a.txt
""", data)


if __name__ == '__main__':
    unittest.main()
