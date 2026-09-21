import datetime
import pathlib
from typing import Optional
from tinygit import repository, index, tree, objects

def get_head_ref() -> str:
    """Reads the HEAD file and returns the ref path (e.g., refs/heads/main)."""
    repo_path = repository.get_repo_path()
    head_path = repo_path / ".tinygit" / "HEAD"
    content = head_path.read_text().strip()
    if content.startswith("ref: "):
        return content[5:]
    return ""

def get_ref(ref_path: str) -> Optional[str]:
    """Reads a reference file and returns the commit SHA-1."""
    repo_path = repository.get_repo_path()
    path = repo_path / ".tinygit" / ref_path
    if path.exists():
        return path.read_text().strip()
    return None

def update_ref(ref_path: str, sha1: str) -> None:
    """Updates a reference file to point to a new commit."""
    repo_path = repository.get_repo_path()
    path = repo_path / ".tinygit" / ref_path
    path.write_text(sha1 + "\n")

def create_commit(message: str) -> None:
    """Creates a commit object and updates the current branch."""
    index_data = index.read_index()
    if not index_data:
        print("nothing to commit")
        return
        
    tree_sha1 = tree.write_tree(index_data)
    
    head_ref = get_head_ref()
    parent_sha1 = get_ref(head_ref) if head_ref else None
    
    # Construct commit content
    lines = [f"tree {tree_sha1}"]
    if parent_sha1:
        lines.append(f"parent {parent_sha1}")
        
    author = "Student"
    date_str = datetime.datetime.now().strftime("%Y-%m-%d") # simplified date as per user request example
    lines.append(f"author {author} {date_str}")
    lines.append("")
    lines.append(message)
    
    commit_data = "\n".join(lines).encode()
    commit_sha1 = objects.write_object(commit_data, "commit")
    
    if head_ref:
        update_ref(head_ref, commit_sha1)
        branch_name = head_ref.split("/")[-1]
    else:
        # In detached HEAD state, update HEAD directly
        repo_path = repository.get_repo_path()
        (repo_path / ".tinygit" / "HEAD").write_text(commit_sha1 + "\n")
        branch_name = "detached"
        
    # Clear the staging area as requested
    index.write_index({})
    
    # Print output
    short_sha1 = commit_sha1[:7]
    num_files = len(index_data)
    file_word = "file" if num_files == 1 else "files"
    print(f"[{branch_name} {short_sha1}] {message}")
    print(f"{num_files} {file_word} changed")

def log() -> None:
    """Displays the commit history starting from HEAD."""
    repo_path = repository.get_repo_path()
    head_ref = get_head_ref()
    
    if head_ref:
        current_sha1 = get_ref(head_ref)
    else:
        # Check if HEAD is detached
        current_sha1 = (repo_path / ".tinygit" / "HEAD").read_text().strip()
        
    if not current_sha1:
        print("fatal: your current branch does not have any commits yet")
        return
        
    while current_sha1:
        obj_type, data = objects.read_object(current_sha1)
        if obj_type != "commit":
            print(f"fatal: {current_sha1} is not a commit")
            return
            
        content = data.decode()
        lines = content.split("\n")
        
        # Parse commit data
        parent_sha1 = None
        author_line = ""
        message_lines = []
        in_message = False
        
        for line in lines:
            if in_message:
                message_lines.append(line)
            elif line.startswith("parent "):
                parent_sha1 = line.split(" ")[1]
            elif line.startswith("author "):
                author_line = line[7:]
            elif line == "":
                in_message = True
                
        # Format output similar to real git
        print(f"commit {current_sha1[:7]}")
        
        # Parse author: "Name YYYY-MM-DD"
        author_parts = author_line.rsplit(" ", 1)
        if len(author_parts) == 2:
            author, date = author_parts
            print(f"Author: {author}")
            print(f"Date: {date}")
        else:
            print(f"Author: {author_line}")
            
        print("\n    " + "\n    ".join(message_lines) + "\n")
        
        # Traverse to parent
        current_sha1 = parent_sha1
