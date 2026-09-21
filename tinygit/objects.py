import hashlib
import os
import pathlib
import zlib
from typing import Tuple
from tinygit import repository

def hash_object(data: bytes, obj_type: str = "blob") -> str:
    """Calculates the SHA-1 hash of an object."""
    header = f"{obj_type} {len(data)}\0".encode()
    store_data = header + data
    return hashlib.sha1(store_data).hexdigest()

def write_object(data: bytes, obj_type: str = "blob") -> str:
    """Hashes the data, writes it to the object store, and returns the hash."""
    repo_path = repository.get_repo_path()
    
    header = f"{obj_type} {len(data)}\0".encode()
    store_data = header + data
    sha1 = hashlib.sha1(store_data).hexdigest()
    
    # Store objects using the first two chars as dir name and rest as file name
    obj_dir = repo_path / ".tinygit" / "objects" / sha1[:2]
    obj_dir.mkdir(exist_ok=True)
    
    obj_path = obj_dir / sha1[2:]
    
    if not obj_path.exists():
        # Keep it readable for learning, but real Git compresses it with zlib.
        # We will compress it to show how git does it, but it's optional.
        # Let's not compress it for TinyGit to keep it easily readable via standard tools!
        with open(obj_path, "wb") as f:
            f.write(store_data)
            
    return sha1

def read_object(sha1: str) -> Tuple[str, bytes]:
    """Reads an object from the object store and returns (type, data)."""
    repo_path = repository.get_repo_path()
    obj_path = repo_path / ".tinygit" / "objects" / sha1[:2] / sha1[2:]
    
    if not obj_path.exists():
        raise ValueError(f"fatal: Not a valid object name {sha1}")
        
    with open(obj_path, "rb") as f:
        store_data = f.read()
        
    # Split header and content
    header_end = store_data.find(b'\0')
    if header_end == -1:
        raise ValueError(f"fatal: Corrupt object {sha1}")
        
    header = store_data[:header_end].decode()
    obj_type, size_str = header.split(" ", 1)
    
    data = store_data[header_end + 1:]
    
    if len(data) != int(size_str):
        raise ValueError(f"fatal: Corrupt object {sha1} (size mismatch)")
        
    return obj_type, data
