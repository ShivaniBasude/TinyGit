import http.server
import json
import socketserver
import os
import pathlib
import sys

# Add the parent directory (project root) to sys.path so we can import tinygit
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from tinygit import repository, commit, objects

class TinyGitHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/repo':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                repo_path = repository.get_repo_path()
            except ValueError:
                self.wfile.write(json.dumps({"error": "Not a TinyGit repository"}).encode())
                return
                
            head_ref = commit.get_head_ref()
            current_branch = head_ref.split("/")[-1] if head_ref else "detached"
            
            commits = []
            current_sha1 = commit.get_ref(head_ref) if head_ref else None
            if not current_sha1:
                # check detached head
                head_path = repo_path / ".tinygit" / "HEAD"
                if head_path.exists():
                    current_sha1 = head_path.read_text().strip()
                    if current_sha1.startswith("ref:"):
                        current_sha1 = None
            
            files = []
            if current_sha1:
                obj_type, commit_data = objects.read_object(current_sha1)
                tree_sha1 = None
                for line in commit_data.decode().split("\n"):
                    if line.startswith("tree "):
                        tree_sha1 = line.split(" ")[1]
                        break
                if tree_sha1:
                    from tinygit import diff
                    files_dict = diff.get_tree_blobs(tree_sha1)
                    files = list(files_dict.keys())
            
            curr = current_sha1
            while curr:
                try:
                    obj_type, data = objects.read_object(curr)
                except Exception:
                    break
                    
                if obj_type != "commit": 
                    break
                    
                content = data.decode()
                
                parent_sha1 = None
                author = ""
                message_lines = []
                in_msg = False
                for line in content.split("\n"):
                    if in_msg: message_lines.append(line)
                    elif line.startswith("parent "): parent_sha1 = line.split(" ")[1]
                    elif line.startswith("author "): author = line[7:]
                    elif line == "": in_msg = True
                
                commits.append({
                    "hash": curr,
                    "parent": parent_sha1,
                    "author": author,
                    "message": "\n".join(message_lines)
                })
                curr = parent_sha1

            data = {
                "branch": current_branch,
                "latest_commit": current_sha1,
                "files": files,
                "commits": commits
            }
            self.wfile.write(json.dumps(data).encode())
        else:
            # serve static files
            super().do_GET()

def run(port=8080):
    web_dir = pathlib.Path(__file__).parent.resolve()
    # Save the original cwd
    original_cwd = os.getcwd()
    
    # We must start the server from the visualizer directory so it can serve index.html
    os.chdir(web_dir)
    try:
        # We need to allow reuse address so we don't get port conflicts if we restart
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), TinyGitHandler) as httpd:
            print(f"Serving TinyGit visualizer at http://localhost:{port}")
            print("Press Ctrl+C to stop.")
            # Since get_repo_path relies on CWD to find .tinygit, we need to temporarily
            # change directory back to repo root when fulfilling requests, or just rely on 
            # get_repo_path being able to find it if we started the CLI from the repo root.
            # Wait, get_repo_path uses Path(".").resolve(). If we change to web_dir, it will look from visualizer/.
            # Since visualizer/ is inside the repo, get_repo_path will search upwards and find the root! This works beautifully.
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        os.chdir(original_cwd)

if __name__ == "__main__":
    run()
