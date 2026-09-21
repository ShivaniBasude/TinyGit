import unittest
import tempfile
import os
import shutil
import pathlib
from tinygit import repository, objects, blob

class TestObjects(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        repository.init()

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_hash_object(self):
        data = b"Hello, TinyGit!\n"
        # Using known header format 'blob 16\0Hello, TinyGit!\n'
        sha1 = objects.hash_object(data, "blob")
        # Should be deterministic
        sha1_again = objects.hash_object(data, "blob")
        self.assertEqual(sha1, sha1_again)

    def test_write_and_read_object(self):
        data = b"Some file content here"
        sha1 = objects.write_object(data, "blob")
        
        # Verify it was saved to the correct path
        obj_path = pathlib.Path(".tinygit/objects") / sha1[:2] / sha1[2:]
        self.assertTrue(obj_path.exists())
        
        # Verify read
        obj_type, read_data = objects.read_object(sha1)
        self.assertEqual(obj_type, "blob")
        self.assertEqual(read_data, data)

    def test_blob_class(self):
        test_file = pathlib.Path("test.txt")
        test_file.write_text("Hello Blob")
        
        b = blob.Blob.from_file(str(test_file))
        sha1 = b.save()
        
        # Read back directly
        obj_type, data = objects.read_object(sha1)
        self.assertEqual(obj_type, "blob")
        self.assertEqual(data, b"Hello Blob")

if __name__ == '__main__':
    unittest.main()
