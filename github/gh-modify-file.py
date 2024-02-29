###################################################################################
##
## gh-modify-file.py
##
## Update a file in the remote branch using the GitHub REST API
##
## - You will need to add your personal access token to this
##       Your token should have fine grained permissions of read/write for Contents
##
###################################################################################
import requests
import base64
import json
import re

# GitHub credentials and repository details
token = 'YOUR_TOKEN_HERE'
repo_owner = 'jpjones3'
repo_name = 'python_automation'
base_branch = 'main'
working_branch = 'my_branch'

# Change details
commit_message = 'Committing change via GitHub API!'
file_path = 'work/env1/main.tf'
pattern = r'version *= *"\d{1,}\.\d{1,}\.\d{1,}"' #regex for pattern to match. This matches version = "x.y.z"
replacement = 'version = "0.3.16"'
 
# Base URL for GitHub's API
base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/'

# Headers for API requests
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

###################################################################################
# Get the tree SHA of the base branch
###################################################################################
commit_url = base_url + f'git/refs/heads/{base_branch}'
response = requests.get(commit_url, headers=headers)
base_commit_sha = response.json()['object']['sha']

###################################################################################
# Get the tree associated with the base commit
###################################################################################
commit_details_url = base_url + f'commits/{base_commit_sha}'
response = requests.get(commit_details_url, headers=headers)
base_commit_data = response.json()
base_tree_sha = base_commit_data['commit']['tree']['sha']

###################################################################################
# Make changes to the file
###################################################################################
file_url = base_url + f'contents/{file_path}?ref={working_branch}'
response = requests.get(file_url, headers=headers)
file_data = response.json()
current_content = base64.b64decode(file_data['content']).decode('utf-8')
new_content = re.sub(pattern, replacement, current_content)

###################################################################################
# Create a new tree
###################################################################################
tree_url = base_url + 'git/trees'
tree_data = {
    "base_tree": base_tree_sha,
    "tree": [
        {
            "path": file_path,
            "mode": "100644",  # File mode
            "type": "blob",     # Blob type
            "content": new_content
        }
    ]
}

response = requests.post(tree_url, headers=headers, json=tree_data)
if response.status_code != 201:
    print(f"Failed to create new tree. Status code: {response.status_code}, Response: {response.text}")
    exit()

new_tree_sha = response.json()['sha']

###################################################################################
# Create a new commit
###################################################################################
print('base_commit_sha:', base_commit_sha)
commit_data = {
    "message": commit_message,
    "tree": new_tree_sha,
    "parents": [base_commit_sha]
}

commit_url = base_url + 'git/commits'
response = requests.post(commit_url, headers=headers, json=commit_data)
if response.status_code != 201:
    print(f"Failed to create commit. Status code: {response.status_code}, Response: {response.text}")
    exit()

new_commit_sha = response.json()['sha']

###################################################################################
# Update the working branch
###################################################################################
push_url = base_url + f'git/refs/heads/{working_branch}'
push_data = {
    "sha": new_commit_sha,
    "force": True  # This indicates a force push
}
response = requests.patch(push_url, headers=headers, json=push_data)
if response.status_code != 200:
    print(f"Failed to push changes. Status code: {response.status_code}, Response: {response.text}")
else:
    print("Changes pushed successfully.")

#NOTE: Below is an alternative to Step to push changes without the force push by pulling the latest changes but this never worked
# Fetch latest changes and merge/pull
#fetch_url = base_url + f'commits'
#response = requests.post(fetch_url, headers=headers)
#if response.status_code != 200:
#    print(f"Failed to fetch changes. Status code: {response.status_code}, Response: {response.text}")
#    exit()

# Push changes
#response = requests.patch(push_url, headers=headers, json=push_data)
#if response.status_code != 200:
#    print(f"Failed to push changes. Status code: {response.status_code}, Response: {response.text}")
#else:
#    print("Changes pushed successfully.")


