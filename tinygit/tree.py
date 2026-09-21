import pathlib
from tinygit import objects

def write_tree(index_data: dict) -> str:
    """Builds a tree structure from the index and saves it to the object store."""
    root = {}
    for path, sha1 in index_data.items():
        parts = pathlib.Path(path).parts
        current = root
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = sha1
        
    return _build_tree_object(root)

def _build_tree_object(tree_dict: dict) -> str:
    """Recursively builds and saves tree objects."""
    entries = []
    for name, value in tree_dict.items():
        if isinstance(value, dict):
            # It's a subtree
            sha1 = _build_tree_object(value)
            entries.append(f"tree {sha1} {name}")
        else:
            # It's a blob
            entries.append(f"blob {value} {name}")
            
    # Sort entries for deterministic hashing (important!)
    entries.sort()
    
    tree_data = "\n".join(entries).encode()
    return objects.write_object(tree_data, "tree")
