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
    
    # branch command
    branch_parser = subparsers.add_parser("branch", help="List or create branches")
    branch_parser.add_argument("name", nargs="?", help="Name of the new branch")
    
    # checkout command
    checkout_parser = subparsers.add_parser("checkout", help="Switch branches or restore working tree files")
    checkout_parser.add_argument("-b", action="store_true", help="Create and checkout a new branch")
    checkout_parser.add_argument("name", help="Branch name to checkout")
    
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
    elif args.command == "branch":
        from tinygit import refs, commit
        if args.name:
            refs.create_branch(args.name)
        else:
            branches = refs.list_branches()
            current = commit.get_head_ref().split("/")[-1] if commit.get_head_ref() else ""
            for b in branches:
                if b == current:
                    print(f"* {b}")
                else:
                    print(f"  {b}")
    elif args.command == "checkout":
        from tinygit import checkout
        checkout.checkout(args.name, create=args.b)
    else:
        print(f"tinygit: '{args.command}' is not a tinygit command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
