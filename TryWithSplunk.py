import json
import requests

# Splunk configuration (replace with your own values)
SPLUNK_URL = "https://LOKESHAGNIHOTRI:8089/services/collector/event"
SPLUNK_TOKEN = "82af2f39-06c4-468f-825c-32f67e499d49"

# GitHub API endpoints
REPO_API_ENDPOINT = "https://api.github.com/users/{user}/repos"
DEPENDENCIES_API_ENDPOINT = "https://api.github.com/repos/{owner}/{repo}/dependency-graph"

# GitHub authentication credentials (replace with your own values)
auth = ("LokeshAgnihotri", "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")

# GitHub user information
user = "ignashub"

def get_dependencies(owner, repo):
    """
    Recursively retrieves the full dependency tree for a given repository.
    """
    # Make API request to get list of dependencies for the repository
    dependencies_api_url = DEPENDENCIES_API_ENDPOINT.format(owner=owner, repo=repo)
    response = requests.get(dependencies_api_url, auth=auth, verify=True)

    if response.status_code == 200:
        # Extract dependencies from API response
        dependencies = []
        for package in response.json()["dependencies"]:
            dependencies.append({
                "name": package["package"]["name"],
                "version": package["package"]["version"],
                "type": package["package"]["type"],
                "url": package["package"]["repository"]["url"],
                "dependencies": get_dependencies(package["package"]["repository"]["owner"]["login"], package["package"]["repository"]["name"])
            })

        return dependencies
    else:
        print("Error getting repository dependencies: ", response.status_code)
        return []

# Make API request to get list of repositories for the user
repo_api_url = REPO_API_ENDPOINT.format(user=user)
response = requests.get(repo_api_url, auth=auth, verify=True)

if response.status_code == 200:
    # Create empty dictionary to store all dependencies
    all_dependencies = {}

    # Iterate through each repository
    for repo in response.json():
        print("Processing repository: ", repo["name"])

        # Get full dependency tree for the repository
        dependencies = get_dependencies(repo["owner"]["login"], repo["name"])

        # Add dependencies to the dictionary
        if dependencies:
            all_dependencies[repo["name"]] = dependencies

    # Convert dictionary of dependencies to JSON
    dependencies_json = json.dumps(all_dependencies)

    # Send JSON to Splunk
    headers = {"Authorization": f"Splunk {SPLUNK_TOKEN}"}
    data = {"event": dependencies_json}
    response = requests.post(SPLUNK_URL, headers=headers, json=data, verify=True)

    if response.status_code == 200:
        print("Success!")
    else:
        print("Error sending JSON to Splunk: ", response.status_code)

else:
    print("Error getting repositories for user: ", response.status_code)
