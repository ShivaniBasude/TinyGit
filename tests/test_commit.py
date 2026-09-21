import unittest
import tempfile
import os
import shutil
import pathlib
from tinygit import repository, index, commit, tree, objects

class TestCommit(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        repository.init()

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_write_tree(self):
        # Create a simple structure
        pathlib.Path("src").mkdir()
        (pathlib.Path("src") / "hello.py").write_text("print('hello')")
        pathlib.Path("README.md").write_text("# Hello")
        
        index.add(".")
        
        idx = index.read_index()
        tree_sha1 = tree.write_tree(idx)
        
        # Verify root tree object exists
        obj_type, data = objects.read_object(tree_sha1)
        self.assertEqual(obj_type, "tree")
        content = data.decode()
        self.assertIn("blob ", content)
        self.assertIn("README.md", content)
        self.assertIn("tree ", content)
        self.assertIn("src", content)

    def test_create_commit(self):
        pathlib.Path("a.txt").write_text("a")
        index.add("a.txt")
        
        # Test creating a commit
        commit.create_commit("Initial commit")
        
        # Check that refs/heads/main has been updated
        sha1 = commit.get_ref("refs/heads/main")
        self.assertIsNotNone(sha1)
        
        # Check commit object
        obj_type, data = objects.read_object(sha1)
        self.assertEqual(obj_type, "commit")
        
        content = data.decode()
        self.assertIn("tree ", content)
        self.assertIn("author Student ", content)
        self.assertIn("Initial commit", content)
        
        # Verify index was cleared
        self.assertEqual(index.read_index(), {})
        
    def test_commit_with_parent(self):
        # First commit
        pathlib.Path("a.txt").write_text("a")
        index.add("a.txt")
        commit.create_commit("Commit 1")
        commit1_sha1 = commit.get_ref("refs/heads/main")
        
        # Second commit
        pathlib.Path("b.txt").write_text("b")
        index.add("b.txt")
        commit.create_commit("Commit 2")
        commit2_sha1 = commit.get_ref("refs/heads/main")
        
        self.assertNotEqual(commit1_sha1, commit2_sha1)
        
        # Check that commit 2 points to commit 1
        obj_type, data = objects.read_object(commit2_sha1)
        self.assertIn(f"parent {commit1_sha1}", data.decode())

if __name__ == '__main__':
    unittest.main()
