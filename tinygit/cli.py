import argparse
import sys
from tinygit import repository

def main():
    parser = argparse.ArgumentParser(prog="tinygit", description="A beginner-friendly Git implementation.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new TinyGit repository")
    
    args = parser.parse_args()
    
    if args.command == "init":
        repository.init()
    else:
        print(f"tinygit: '{args.command}' is not a tinygit command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
