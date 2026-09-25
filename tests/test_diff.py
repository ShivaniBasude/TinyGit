import unittest
import tempfile
import os
import shutil
import pathlib
from io import StringIO
import sys
from tinygit import repository, index, commit, diff

class TestDiff(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        repository.init()

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_diff(self):
        # Create file and commit
        test_file = pathlib.Path("hello.txt")
        test_file.write_text("Hello World\n")
        index.add("hello.txt")
        commit.create_commit("Initial")
        
        # Modify file
        test_file.write_text("Hello World\nUpdated line\n")
        
        # Capture diff output
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            diff.diff()
            output = out.getvalue()
            
            self.assertIn("--- a/hello.txt", output)
            self.assertIn("+++ b/hello.txt", output)
            self.assertIn("+Updated line", output)
        finally:
            sys.stdout = saved_stdout

if __name__ == '__main__':
    unittest.main()
