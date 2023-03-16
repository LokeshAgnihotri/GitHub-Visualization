import requests
import base64
import json

# GitHub API endpoint
API_ENDPOINT = "https://api.github.com/users/{user}/repos"

# GitHub authentication credentials (replace with your own values)
auth = ("LokeshAgnihotri", "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")

# GitHub username to retrieve repositories for
username = "nischay1234aa"

# Initialize dictionary to store repositories and their dependencies
repositories = {}

# Make API request to get list of repositories for the user
repo_api_url = API_ENDPOINT.format(user=username)
response = requests.get(repo_api_url, auth=auth, verify=True)

if response.status_code == 200:
    # Iterate through each repository
    for repo in response.json():
        print("Retrieving dependencies for repository:", repo["name"])
        # Make API request to get the contents of the requirements.txt file
        requirements_api_url = f'https://api.github.com/repos/{username}/{repo["name"]}/contents/requirements.txt'
        requirements_response = requests.get(requirements_api_url, auth=auth, verify=True)
        if requirements_response.status_code == 200:
            # Extract the dependencies from the requirements.txt file
            requirements_content = requirements_response.json()["content"]
            requirements_decoded = base64.b64decode(requirements_content).decode("utf-8")
            requirements_list = requirements_decoded.split("\n")
            # Add the list of dependencies and their versions to the repository dictionary
            repository = {repo["name"]: [{"name": name, "version": version} for name, version in [r.split("==") for r in requirements_list if r.strip() != ""]]}
            repositories.update(repository)
        else:
            print("Error getting dependencies for repository:", repo["name"])
else:
    print("Error getting repositories for user: ", response.status_code)

# Write the repositories dictionary to a JSON file
with open("repositories.json", "w") as f:
    json.dump(repositories, f)
    print("Repositories and their dependencies saved to repositories.json file.")
