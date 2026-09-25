import difflib
import os
import pathlib
from typing import Dict
from tinygit import repository, commit, objects

def get_tree_blobs(tree_sha1: str, base_path: str = "") -> Dict[str, bytes]:
    """Recursively fetches all blobs in a tree and returns a mapping of path -> content."""
    blobs = {}
    if not tree_sha1:
        return blobs
        
    obj_type, tree_data = objects.read_object(tree_sha1)
    if obj_type != "tree":
        return blobs
        
    lines = tree_data.decode().strip().split("\n")
    if not lines or lines == [""]:
        return blobs
        
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) != 3:
            continue
            
        entry_type, sha1, name = parts
        full_path = f"{base_path}/{name}" if base_path else name
        
        if entry_type == "tree":
            blobs.update(get_tree_blobs(sha1, full_path))
        elif entry_type == "blob":
            b_type, b_data = objects.read_object(sha1)
            blobs[full_path] = b_data
            
    return blobs

def get_working_directory_files() -> Dict[str, bytes]:
    """Reads all tracked files in the working directory and returns path -> content."""
    repo_path = repository.get_repo_path()
    files = {}
    
    for root, dirs, filenames in os.walk(repo_path):
        if ".tinygit" in dirs:
            dirs.remove(".tinygit")
            
        root_path = pathlib.Path(root)
        for name in filenames:
            file_path = root_path / name
            rel_path = file_path.relative_to(repo_path).as_posix()
            
            with open(file_path, "rb") as f:
                files[rel_path] = f.read()
                
    return files

def diff() -> None:
    """Prints a unified diff between the working directory and the latest commit."""
    repo_path = repository.get_repo_path()
    head_ref = commit.get_head_ref()
    
    tree_sha1 = None
    if head_ref:
        commit_sha1 = commit.get_ref(head_ref)
        if commit_sha1:
            obj_type, commit_data = objects.read_object(commit_sha1)
            for line in commit_data.decode().split("\n"):
                if line.startswith("tree "):
                    tree_sha1 = line.split(" ")[1]
                    break
                    
    committed_files = get_tree_blobs(tree_sha1) if tree_sha1 else {}
    working_files = get_working_directory_files()
    
    all_paths = set(committed_files.keys()).union(set(working_files.keys()))
    
    for path in sorted(list(all_paths)):
        old_data = committed_files.get(path, b"").decode(errors='replace').splitlines(keepends=True)
        new_data = working_files.get(path, b"").decode(errors='replace').splitlines(keepends=True)
        
        if old_data != new_data:
            sys_diff = difflib.unified_diff(
                old_data, 
                new_data, 
                fromfile=f"a/{path}", 
                tofile=f"b/{path}",
                n=3
            )
            for line in sys_diff:
                print(line, end='')
