import json
import os
import pathlib
from tinygit import repository, blob, objects

def read_index() -> dict:
    """Reads the index file and returns a dictionary of path -> sha1."""
    repo_path = repository.get_repo_path()
    index_path = repo_path / ".tinygit" / "index"
    
    if not index_path.exists():
        return {}
        
    content = index_path.read_text()
    if not content:
        return {}
        
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}

def write_index(index_data: dict) -> None:
    """Writes the index dictionary to the index file."""
    repo_path = repository.get_repo_path()
    index_path = repo_path / ".tinygit" / "index"
    index_path.write_text(json.dumps(index_data, indent=2))

def add(path: str) -> None:
    """Adds a file or directory to the index."""
    repo_path = repository.get_repo_path()
    path_obj = pathlib.Path(path).resolve()
    
    if not path_obj.exists():
        raise FileNotFoundError(f"fatal: pathspec '{path}' did not match any files")
        
    index_data = read_index()
    
    if path_obj.is_file():
        _add_file(path_obj, repo_path, index_data)
    elif path_obj.is_dir():
        for root, _, files in os.walk(path_obj):
            root_path = pathlib.Path(root)
            if ".tinygit" in root_path.parts:
                continue
            for file in files:
                _add_file(root_path / file, repo_path, index_data)
                
    write_index(index_data)

def _add_file(file_path: pathlib.Path, repo_path: pathlib.Path, index_data: dict) -> None:
    """Helper to add a single file to the index."""
    # Convert absolute path to relative path from repo root
    rel_path = file_path.relative_to(repo_path).as_posix()
    
    b = blob.Blob.from_file(str(file_path))
    sha1 = b.save()
    
    index_data[rel_path] = sha1

def status() -> None:
    """Prints the status of the repository."""
    repo_path = repository.get_repo_path()
    index_data = read_index()
    
    # We don't have commits yet, so we assume HEAD is empty.
    # Everything in the index is a "staged" file (Added).
    staged = []
    for path, sha1 in index_data.items():
        staged.append(f" A {path}")
        
    # Check working directory against index
    modified = []
    untracked = []
    
    for root, dirs, files in os.walk(repo_path):
        if ".tinygit" in dirs:
            dirs.remove(".tinygit")
            
        root_path = pathlib.Path(root)
        for file in files:
            file_path = root_path / file
            rel_path = file_path.relative_to(repo_path).as_posix()
            
            if rel_path in index_data:
                # Check if modified
                with open(file_path, "rb") as f:
                    data = f.read()
                current_sha1 = objects.hash_object(data, "blob")
                if current_sha1 != index_data[rel_path]:
                    modified.append(f" M {rel_path}")
            else:
                untracked.append(f" ?? {rel_path}")
                
    if not staged and not modified and not untracked:
        print("nothing to commit, working tree clean")
        return
        
    if modified:
        print("Changes not staged:")
        for m in sorted(modified):
            print(m)
        print()
        
    if untracked:
        print("Untracked files:")
        for u in sorted(untracked):
            print(u)
        print()
            
    if staged:
        print("Changes staged:")
        for s in sorted(staged):
            print(s)
        print()
