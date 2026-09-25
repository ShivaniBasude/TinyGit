import pathlib
from typing import List
from tinygit import repository, commit

def list_branches() -> List[str]:
    """Returns a list of all branch names."""
    repo_path = repository.get_repo_path()
    heads_dir = repo_path / ".tinygit" / "refs" / "heads"
    
    branches = []
    if heads_dir.exists():
        for path in heads_dir.iterdir():
            if path.is_file():
                branches.append(path.name)
    return branches

def create_branch(name: str) -> None:
    """Creates a new branch pointing to the current commit."""
    repo_path = repository.get_repo_path()
    heads_dir = repo_path / ".tinygit" / "refs" / "heads"
    
    branch_path = heads_dir / name
    if branch_path.exists():
        raise ValueError(f"fatal: A branch named '{name}' already exists.")
        
    head_ref = commit.get_head_ref()
    if head_ref:
        current_sha1 = commit.get_ref(head_ref)
    else:
        current_sha1 = (repo_path / ".tinygit" / "HEAD").read_text().strip()
        
    if not current_sha1:
        raise ValueError("fatal: Not a valid object name: 'HEAD'. Cannot create branch.")
        
    branch_path.write_text(current_sha1 + "\n")
