import argparse
import sys
from tinygit import repository

def main():
    parser = argparse.ArgumentParser(prog="tinygit", description="A beginner-friendly Git implementation.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new TinyGit repository")
    
    # add command
    add_parser = subparsers.add_parser("add", help="Add file contents to the index")
    add_parser.add_argument("path", help="Files to add content from")

    # status command
    status_parser = subparsers.add_parser("status", help="Show the working tree status")
    
    # commit command
    commit_parser = subparsers.add_parser("commit", help="Record changes to the repository")
    commit_parser.add_argument("-m", "--message", required=True, help="Commit message")

    # log command
    log_parser = subparsers.add_parser("log", help="Show commit logs")
    
    args = parser.parse_args()
    
    if args.command == "init":
        repository.init()
    elif args.command == "add":
        from tinygit import index
        index.add(args.path)
    elif args.command == "status":
        from tinygit import index
        index.status()
    elif args.command == "commit":
        from tinygit import commit
        commit.create_commit(args.message)
    elif args.command == "log":
        from tinygit import commit
        commit.log()
    else:
        print(f"tinygit: '{args.command}' is not a tinygit command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
