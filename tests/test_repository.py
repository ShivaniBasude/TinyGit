import unittest
import tempfile
import os
import shutil
import pathlib
from tinygit import repository

class TestRepository(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_init(self):
        repository.init()
        base = pathlib.Path(".tinygit")
        self.assertTrue(base.exists())
        self.assertTrue((base / "objects").is_dir())
        self.assertTrue((base / "refs" / "heads").is_dir())
        
        with open(base / "HEAD", "r") as f:
            self.assertEqual(f.read(), "ref: refs/heads/main\n")
            
        with open(base / "index", "r") as f:
            self.assertEqual(f.read(), "")

    def test_get_repo_path(self):
        repository.init()
        repo_path = repository.get_repo_path()
        self.assertEqual(repo_path, pathlib.Path(".").resolve())
        
        # Test finding it from a subdirectory
        sub_dir = pathlib.Path("some/sub/dir")
        sub_dir.mkdir(parents=True)
        os.chdir(sub_dir)
        repo_path = repository.get_repo_path()
        self.assertEqual(repo_path, pathlib.Path(self.test_dir).resolve())

    def test_not_a_repo(self):
        with self.assertRaisesRegex(ValueError, "fatal: not a TinyGit repository"):
            repository.get_repo_path()

if __name__ == '__main__':
    unittest.main()
