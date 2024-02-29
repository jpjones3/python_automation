###################################################################################
##
## gh-create-branch.py
##
## Create a branch using the GitHub REST API
##
## - You will need to add your personal access token to this
##       Your token should have fine grained permissions of read/write for Contents
##
###################################################################################
import requests

# Define your GitHub personal access token and repository details
token = 'YOUR_TOKEN_HERE'
owner = 'jpjones3'
repo = 'python_automation'

# Define the base URL for GitHub's API
base_url = f'https://api.github.com/repos/{owner}/{repo}/'

# Define the branch names for the new branch and the branch you want to base the new branch off of
branch_name = 'new_branch'
base_branch = 'main'

# Define the request headers including the Authorization header with your access token
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Get the latest commit SHA of the base branch
url = base_url + f'git/ref/heads/{base_branch}'
response = requests.get(url, headers=headers)
response_json = response.json()
latest_commit_sha = response_json['object']['sha']

# Create a new branch using the latest commit SHA of the base branch
url = base_url + 'git/refs'
payload = {
    "ref": f"refs/heads/{branch_name}",
    "sha": latest_commit_sha
}
response = requests.post(url, headers=headers, json=payload)

# Check the response status
if response.status_code == 201:
    print(f"Branch '{branch_name}' created successfully.")
else:
    print(f"Failed to create branch. Status code: {response.status_code}, Response: {response.text}")
