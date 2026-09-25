import os
import shutil
import pathlib
from tinygit import repository, commit, objects, refs, index

def checkout(name: str, create: bool = False) -> None:
    """Checks out a branch and updates the working directory."""
    repo_path = repository.get_repo_path()
    
    if create:
        refs.create_branch(name)
        
    branch_path = repo_path / ".tinygit" / "refs" / "heads" / name
    if not branch_path.exists():
        raise ValueError(f"error: pathspec '{name}' did not match any file(s) known to tinygit")
        
    # Get the commit hash the branch points to
    commit_sha1 = branch_path.read_text().strip()
    
    # Read the commit to get the root tree
    obj_type, commit_data = objects.read_object(commit_sha1)
    if obj_type != "commit":
        raise ValueError(f"fatal: branch '{name}' does not point to a commit")
        
    tree_sha1 = None
    for line in commit_data.decode().split("\n"):
        if line.startswith("tree "):
            tree_sha1 = line.split(" ")[1]
            break
            
    if not tree_sha1:
        raise ValueError("fatal: commit does not contain a tree")
        
    # Clear working directory (except .tinygit)
    _clear_working_directory(repo_path)
    
    # Restore files from the tree
    _restore_tree(tree_sha1, repo_path)
    
    # Update HEAD
    head_path = repo_path / ".tinygit" / "HEAD"
    head_path.write_text(f"ref: refs/heads/{name}\n")
    
    # Clear index (for simplicity, we assume checkout gives a clean index)
    index.write_index({})
    
    print(f"Switched to branch '{name}'")

def _clear_working_directory(repo_path: pathlib.Path) -> None:
    """Deletes all files and folders in the repo except .tinygit."""
    for item in repo_path.iterdir():
        if item.name == ".tinygit":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

def _restore_tree(tree_sha1: str, base_path: pathlib.Path) -> None:
    """Recursively restores files and directories from a tree object."""
    obj_type, tree_data = objects.read_object(tree_sha1)
    if obj_type != "tree":
        raise ValueError(f"fatal: {tree_sha1} is not a tree")
        
    lines = tree_data.decode().strip().split("\n")
    if not lines or lines == [""]:
        return
        
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) != 3:
            continue
            
        entry_type, sha1, name = parts
        target_path = base_path / name
        
        if entry_type == "tree":
            target_path.mkdir(exist_ok=True)
            _restore_tree(sha1, target_path)
        elif entry_type == "blob":
            b_type, b_data = objects.read_object(sha1)
            target_path.write_bytes(b_data)
