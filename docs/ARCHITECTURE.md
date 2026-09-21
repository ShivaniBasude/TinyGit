# TinyGit - Architecture Plan

## Overview
TinyGit is built with a modular, layered architecture. The system separates the command-line interface (CLI) from the core version control logic and object storage.

## Components

### 1. CLI Layer (`tinygit/cli.py`)
Parses command-line arguments and routes them to the appropriate repository actions. Handles user-facing output, formatting, and error messages.

### 2. Repository Layer (`tinygit/repository.py`)
Manages the `.tinygit` directory structure. Coordinates high-level operations like initializing the repo, checking status, and managing the active workspace.

### 3. Index / Staging (`tinygit/index.py`)
Manages the `.tinygit/index` file, which acts as a staging area keeping track of files prepared for the next commit. It bridges the working directory and the object store.

### 4. Object Store & Core Objects
Handles reading and writing content-addressable objects to `.tinygit/objects/`.
- **Blob (`tinygit/blob.py`)**: Stores raw file contents.
- **Tree (`tinygit/tree.py`)**: Represents a directory, storing references (hashes) to blobs and sub-trees.
- **Commit (`tinygit/commit.py`)**: Stores a snapshot, including a reference to the root tree, author metadata, a timestamp, a message, and a reference to its parent commit(s).
- **Core Storage (`tinygit/objects.py`)**: Responsible for serializing/deserializing these objects, hashing (SHA-1), and writing them to disk.

### 5. References (`tinygit/refs.py`)
Manages named pointers to commits (branches) stored in `.tinygit/refs/heads/`, and the `HEAD` file which indicates the currently checked-out branch.

### 6. Operations (`tinygit/checkout.py`, `tinygit/diff.py`)
Contains logic for complex operations like traversing the commit graph, updating the working directory to match a commit, and calculating file diffs.

## Data Flow Examples

### `tinygit add <file>`
1. CLI receives command and file path.
2. Index reads the file from the working directory.
3. Object Store hashes the content, creates a Blob, and saves it to `.tinygit/objects/`.
4. Index updates the `.tinygit/index` file with the file path and new blob hash.

### `tinygit commit -m "msg"`
1. CLI receives the commit command.
2. Repository reads the current Index.
3. Trees are created recursively for all paths in the Index, saved to the Object Store.
4. A new Commit object is created, pointing to the root Tree and the parent commit (found via HEAD).
5. The Commit is saved to the Object Store.
6. The active branch reference (in `refs/heads/`) is updated to the new Commit hash.
7. Index is cleared or marked as committed.
