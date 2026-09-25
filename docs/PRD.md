# TinyGit - Product Requirements Document

## Project Goal
TinyGit is a beginner-friendly, simplified version-control system implemented from scratch in Python. It is designed as an educational portfolio project to demonstrate core computer science and software engineering concepts:
- File systems
- Hashing
- Data structures
- Version control
- Graphs (DAGs)
- Command-line applications (CLI)
- Software architecture

The project must operate independently of real Git, storing its data in a `.tinygit/` directory.


## Key Features & Commands
- `tinygit init`: Initialize a new repository (`.tinygit/` structure).
- `tinygit status`: Show untracked, modified, and staged files.
- `tinygit add <file> | .`: Stage files (create blobs and update index).
- `tinygit commit -m "message"`: Create trees and commit objects, update HEAD.
- `tinygit log`: Display commit history by traversing parent links.
- `tinygit branch [name]`: List or create branches (references to commits).
- `tinygit checkout [-b] <name>`: Switch branches and update working directory.
- `tinygit diff`: Show line-level differences between working directory and latest commit.
- **Web Visualizer**: A simple HTML/CSS/JS frontend to visualize the commit graph and repo state.

## Storage Model
- Content-addressable object store (using SHA-1 hashing).
- Objects stored as loose files in `.tinygit/objects/`.
- References (branches) stored in `.tinygit/refs/heads/`.
- Simple staging area representation in `.tinygit/index`.


