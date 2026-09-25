from tinygit import repository, commit, refs, checkout

def merge(branch_name: str) -> None:
    """Performs a fast-forward merge of the given branch into the current branch."""
    head_ref = commit.get_head_ref()
    if not head_ref:
        print("fatal: You are not on a branch.")
        return
        
    current_sha1 = commit.get_ref(head_ref)
    if not current_sha1:
        print("fatal: Current branch has no commits.")
        return
        
    target_sha1 = commit.get_ref(f"refs/heads/{branch_name}")
    if not target_sha1:
        print(f"fatal: branch '{branch_name}' does not exist.")
        return
        
    if current_sha1 == target_sha1:
        print("Already up to date.")
        return
        
    # Check if target is a descendant of current
    if _is_descendant(target_sha1, current_sha1):
        # Fast-forward
        print("Updating " + current_sha1[:7] + ".." + target_sha1[:7])
        print("Fast-forward merge completed.")
        
        # Update branch ref
        commit.update_ref(head_ref, target_sha1)
        
        # Checkout the same branch to update working directory
        current_branch = head_ref.split("/")[-1]
        checkout.checkout(current_branch)
    else:
        print("fatal: Non-fast-forward merge is not supported yet.")

def _is_descendant(descendant_sha1: str, ancestor_sha1: str) -> bool:
    """Returns True if ancestor_sha1 is in the parent history of descendant_sha1."""
    from tinygit import objects
    current = descendant_sha1
    
    while current:
        if current == ancestor_sha1:
            return True
            
        obj_type, data = objects.read_object(current)
        if obj_type != "commit":
            break
            
        parent_sha1 = None
        for line in data.decode().split("\n"):
            if line.startswith("parent "):
                parent_sha1 = line.split(" ")[1]
                break
                
        current = parent_sha1
        
    return False
