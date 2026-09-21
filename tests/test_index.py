import unittest
import tempfile
import os
import shutil
import pathlib
from tinygit import repository, index, objects

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        repository.init()

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_add_file(self):
        test_file = pathlib.Path("hello.txt")
        test_file.write_text("Hello World")
        
        index.add("hello.txt")
        
        idx = index.read_index()
        self.assertIn("hello.txt", idx)
        
        # Verify blob was created
        sha1 = idx["hello.txt"]
        obj_type, data = objects.read_object(sha1)
        self.assertEqual(obj_type, "blob")
        self.assertEqual(data, b"Hello World")

    def test_add_directory(self):
        test_dir = pathlib.Path("src")
        test_dir.mkdir()
        test_file = test_dir / "main.py"
        test_file.write_text("print('hi')")
        
        index.add(".")
        
        idx = index.read_index()
        self.assertIn("src/main.py", idx)

    def test_status_output(self):
        # We can test status by capturing stdout, but for now we just 
        # ensure it runs without crashing, since print is hard to test directly here
        # without mocking sys.stdout. Let's just do a basic sanity run.
        test_file = pathlib.Path("hello.txt")
        test_file.write_text("Hello World")
        
        # Should show untracked
        index.status()
        
        index.add("hello.txt")
        
        # Should show staged
        index.status()
        
        # Modify it
        test_file.write_text("Hello World 2")
        
        # Should show modified and staged
        index.status()
        
if __name__ == '__main__':
    unittest.main()
