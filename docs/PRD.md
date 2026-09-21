# TinyGit - Product Requirements Document

## 1. Project Goal
TinyGit is a beginner-friendly, simplified version-control system implemented from scratch in Python. It is designed as an educational portfolio project to demonstrate core computer science and software engineering concepts:
- File systems
- Hashing
- Data structures
- Version control
- Graphs (DAGs)
- Command-line applications (CLI)
- Software architecture

The project must operate independently of real Git, storing its data in a `.tinygit/` directory.

## 2. Target Audience
- Beginners and CS students learning version control internals.
- Interviewers evaluating portfolio projects.

## 3. Core Principles
- **Teach, don't just generate:** Code must be simple, readable, and well-documented.
- **No over-engineering:** No distributed systems, microservices, unnecessary databases, or advanced Git features (rebase, cherry-pick, submodules, etc.).
- **Minimal dependencies:** Use Python 3 standard library exclusively for the core CLI.

## 4. Key Features & Commands
- `tinygit init`: Initialize a new repository (`.tinygit/` structure).
- `tinygit status`: Show untracked, modified, and staged files.
- `tinygit add <file> | .`: Stage files (create blobs and update index).
- `tinygit commit -m "message"`: Create trees and commit objects, update HEAD.
- `tinygit log`: Display commit history by traversing parent links.
- `tinygit branch [name]`: List or create branches (references to commits).
- `tinygit checkout [-b] <name>`: Switch branches and update working directory.
- `tinygit diff`: Show line-level differences between working directory and latest commit.
- **Web Visualizer**: A simple HTML/CSS/JS frontend to visualize the commit graph and repo state.

## 5. Storage Model
- Content-addressable object store (using SHA-1 hashing).
- Objects stored as loose files in `.tinygit/objects/`.
- References (branches) stored in `.tinygit/refs/heads/`.
- Simple staging area representation in `.tinygit/index`.

## 6. Definition of Done
The core CLI workflow (init -> add -> commit -> branch -> checkout -> diff -> log) must execute flawlessly on local files without relying on real Git. Accompanying documentation, an interview guide, and a resume bullet list must be provided.
