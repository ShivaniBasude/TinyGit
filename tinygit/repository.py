import os
import pathlib

def get_repo_path(start_path: str = ".") -> pathlib.Path:
    """Finds the root of the tinygit repository by looking for .tinygit."""
    current = pathlib.Path(start_path).resolve()
    while True:
        if (current / ".tinygit").is_dir():
            return current
        if current.parent == current:
            # Reached root directory
            raise ValueError("fatal: not a TinyGit repository")
        current = current.parent

def init(repo_path: str = ".") -> None:
    """Initializes a new TinyGit repository."""
    base = pathlib.Path(repo_path).resolve() / ".tinygit"
    
    if base.exists():
        print(f"TinyGit repository already initialized in {base}")
        return

    # Create directories
    base.mkdir(parents=True)
    (base / "objects").mkdir()
    (base / "refs").mkdir()
    (base / "refs" / "heads").mkdir()
    
    # Create files
    with open(base / "HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
        
    with open(base / "index", "w") as f:
        f.write("") # empty index for now
        
    print(f"Initialized empty TinyGit repository in {base}")
