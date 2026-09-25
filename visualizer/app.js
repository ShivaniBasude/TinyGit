document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/repo')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.body.innerHTML = `<h2>Error: ${data.error}</h2>`;
                return;
            }
            renderRepo(data);
        })
        .catch(err => {
            console.error(err);
            document.body.innerHTML = `<h2>Error connecting to TinyGit server.</h2>`;
        });
});

let repoCommits = [];

function renderRepo(data) {
    document.getElementById('current-branch').textContent = data.branch;
    document.getElementById('latest-commit').textContent = data.latest_commit ? data.latest_commit.substring(0, 7) : 'None';

    const fileList = document.getElementById('file-list');
    if (data.files && data.files.length > 0) {
        data.files.forEach(file => {
            const li = document.createElement('li');
            li.textContent = file;
            fileList.appendChild(li);
        });
    } else {
        fileList.innerHTML = '<li><em>No files tracked</em></li>';
    }

    repoCommits = data.commits || [];
    const commitGraph = document.getElementById('commit-graph');
    
    if (repoCommits.length === 0) {
        commitGraph.innerHTML = '<p>No commits yet.</p>';
        return;
    }

    repoCommits.forEach(commit => {
        const node = document.createElement('div');
        node.className = 'commit-node';
        
        const shortHash = commit.hash.substring(0, 7);
        const firstLineMsg = commit.message.split('\n')[0];
        
        // Extract name and date if formatted properly
        let authorDisplay = commit.author;
        const authorParts = commit.author.lastIndexOf(' ');
        if (authorParts !== -1) {
             authorDisplay = commit.author.substring(0, authorParts) + ' on ' + commit.author.substring(authorParts + 1);
        }

        node.innerHTML = `
            <div class="commit-header">
                <span class="commit-hash">${shortHash}</span>
                <span class="commit-author">${authorDisplay}</span>
            </div>
            <p class="commit-msg">${firstLineMsg}</p>
        `;
        
        node.addEventListener('click', () => showCommitDetails(commit));
        commitGraph.appendChild(node);
    });
}

function showCommitDetails(commit) {
    const details = document.getElementById('commit-details');
    details.classList.remove('hidden');
    
    document.getElementById('detail-hash').textContent = commit.hash;
    document.getElementById('detail-author').textContent = commit.author;
    document.getElementById('detail-message').textContent = commit.message;
}
