import unittest
import tempfile
import os
import shutil
import pathlib
from tinygit import repository, index, commit, refs, checkout, merge

class TestMerge(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        repository.init()

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_fast_forward_merge(self):
        # Create commit on main
        pathlib.Path("hello.txt").write_text("v1")
        index.add("hello.txt")
        commit.create_commit("v1")
        
        # Checkout feature
        checkout.checkout("feature", create=True)
        
        # Commit on feature
        pathlib.Path("hello.txt").write_text("v2")
        index.add("hello.txt")
        commit.create_commit("v2")
        feature_sha1 = commit.get_ref("refs/heads/feature")
        
        # Checkout main
        checkout.checkout("main")
        
        # Merge feature into main
        merge.merge("feature")
        
        # Verify main points to feature's commit
        self.assertEqual(commit.get_ref("refs/heads/main"), feature_sha1)
        
        # Verify working directory was updated
        self.assertEqual(pathlib.Path("hello.txt").read_text(), "v2")

if __name__ == '__main__':
    unittest.main()
