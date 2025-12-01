import unittest
import os
import tempfile
import shutil
from compareJars import compare_directories

class TestCompareJars(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.dir1 = os.path.join(self.test_dir, 'dir1')
        self.dir2 = os.path.join(self.test_dir, 'dir2')
        os.makedirs(self.dir1)
        os.makedirs(self.dir2)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_file(self, directory, filename, content=""):
        path = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

    def test_no_differences(self):
        self.create_file(self.dir1, 'file.txt', 'content')
        self.create_file(self.dir2, 'file.txt', 'content')
        added, removed, modified = compare_directories(self.dir1, self.dir2)
        self.assertEqual(added, [])
        self.assertEqual(removed, [])
        self.assertEqual(modified, [])

    def test_added_file(self):
        self.create_file(self.dir2, 'new.txt', 'content')
        added, removed, modified = compare_directories(self.dir1, self.dir2)
        self.assertEqual(added, ['new.txt'])
        self.assertEqual(removed, [])
        self.assertEqual(modified, [])

    def test_removed_file(self):
        self.create_file(self.dir1, 'old.txt', 'content')
        added, removed, modified = compare_directories(self.dir1, self.dir2)
        self.assertEqual(added, [])
        self.assertEqual(removed, ['old.txt'])
        self.assertEqual(modified, [])

    def test_modified_file(self):
        self.create_file(self.dir1, 'file.txt', 'content1')
        self.create_file(self.dir2, 'file.txt', 'content2')
        added, removed, modified = compare_directories(self.dir1, self.dir2)
        self.assertEqual(added, [])
        self.assertEqual(removed, [])
        self.assertEqual(modified, ['file.txt'])

    def test_nested_files(self):
        self.create_file(self.dir1, 'subdir/file.txt', 'content')
        self.create_file(self.dir2, 'subdir/file.txt', 'content')
        added, removed, modified = compare_directories(self.dir1, self.dir2)
        self.assertEqual(added, [])
        self.assertEqual(removed, [])
        self.assertEqual(modified, [])

        self.create_file(self.dir2, 'subdir/new.txt', 'content')
        added, removed, modified = compare_directories(self.dir1, self.dir2)
        self.assertIn(os.path.join('subdir', 'new.txt'), added)

if __name__ == '__main__':
    unittest.main()
