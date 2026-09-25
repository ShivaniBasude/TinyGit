# TinyGit

A beginner-friendly Git-like version control system implemented entirely from scratch in Python. 

TinyGit is designed as an educational project to demystify how version control works under the hood. It implements the core concepts of Git (content-addressable storage, trees, blobs, commits, and a DAG history) without the overwhelming complexity of the real Git codebase.

## Features
- **Standalone:** Operates entirely independently of real Git. Uses a local `.tinygit/` directory.
- **Zero Dependencies:** Built exclusively using the Python 3 standard library.
- **Core CLI:** Supports `init`, `add`, `commit`, `status`, `log`, `branch`, `checkout`, `diff`, and `merge`.
- **Web Visualizer:** Includes a custom HTTP server and HTML/JS frontend to visualize the repository state and commit graph.
- **Uncompressed Objects:** Objects are stored uncompressed for educational purposes, allowing you to manually inspect the object database using standard text editors.

## Architecture & How it works
TinyGit replicates Git's object model:
1. **Blobs:** File contents are hashed using SHA-1 and stored in `.tinygit/objects/`.
2. **Trees:** Directories are represented by Tree objects that point to Blobs.
3. **Commits:** Snapshots are represented by Commit objects that point to a root Tree and the previous Commit (parent).
4. **References:** Branches are simple text files in `.tinygit/refs/heads/` containing a commit hash. `HEAD` points to the active branch.

## Installation
Ensure you have Python 3 installed. No external packages are required.

```bash
git clone https://github.com/yourusername/TinyGit.git
cd TinyGit
```

To run TinyGit, you can execute the module directly:
```bash
python -m tinygit.cli --help
```
*(Optionally, you can alias `python -m tinygit.cli` to `tinygit` in your shell).*

## Commands
* `python -m tinygit.cli init` - Initialize a new repository
* `python -m tinygit.cli status` - Show working tree status
* `python -m tinygit.cli add <path>` - Add file contents to the index
* `python -m tinygit.cli commit -m "message"` - Record changes to the repository
* `python -m tinygit.cli log` - Show commit logs
* `python -m tinygit.cli branch [name]` - List or create branches
* `python -m tinygit.cli checkout [-b] <name>` - Switch branches
* `python -m tinygit.cli diff` - Show changes between working tree and commit
* `python -m tinygit.cli merge <branch>` - Fast-forward merge a branch
* `python -m tinygit.cli serve` - Start the Web Visualizer on port 8080

## Web Visualizer
TinyGit includes a visualizer to help you understand the internal state of the repository.
Run:
```bash
python -m tinygit.cli serve
```
Then navigate to `http://localhost:8080` in your browser to see the live commit graph and tracked files.

## Testing
The project includes a comprehensive suite of unit tests. Run them using:
```bash
python -m unittest discover tests
```

## Limitations
This is an educational project. It does NOT support:
- Remote repositories (push/pull)
- 3-way merges and conflict resolution
- Packfiles and object compression (zlib)

