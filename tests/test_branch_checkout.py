import unittest
import tempfile
import os
import shutil
import pathlib
from tinygit import repository, index, commit, refs, checkout

class TestBranchCheckout(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        repository.init()

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_branch_and_checkout(self):
        # Create initial commit on main
        pathlib.Path("hello.txt").write_text("v1")
        index.add("hello.txt")
        commit.create_commit("v1")
        
        # Create branch
        refs.create_branch("feature")
        self.assertIn("feature", refs.list_branches())
        
        # Checkout feature
        checkout.checkout("feature")
        self.assertEqual(commit.get_head_ref(), "refs/heads/feature")
        
        # Modify file and commit on feature
        pathlib.Path("hello.txt").write_text("v2")
        index.add("hello.txt")
        commit.create_commit("v2")
        
        # Checkout main
        checkout.checkout("main")
        self.assertEqual(commit.get_head_ref(), "refs/heads/main")
        
        # Verify working directory was updated to v1
        self.assertEqual(pathlib.Path("hello.txt").read_text(), "v1")

    def test_checkout_b(self):
        pathlib.Path("hello.txt").write_text("v1")
        index.add("hello.txt")
        commit.create_commit("v1")
        
        # Checkout -b new_branch
        checkout.checkout("new_branch", create=True)
        self.assertEqual(commit.get_head_ref(), "refs/heads/new_branch")
        self.assertIn("new_branch", refs.list_branches())

if __name__ == '__main__':
    unittest.main()
