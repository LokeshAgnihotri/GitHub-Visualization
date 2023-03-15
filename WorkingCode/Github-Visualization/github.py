import json
import requests

# Github API endpoint
API_ENDPOINT = "https://api.github.com"

# Github user to fetch dependencies for
GITHUB_USER = "thebjorn                                      "

# Personal access token to access Github API
ACCESS_TOKEN = "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"

# Dictionary to store the dependencies data
dependencies_data = {}

# Function to recursively fetch dependencies for a given repository
def get_dependencies(repository, depth):
    # Check if repository has already been processed
    if repository in dependencies_data:
        return

    # Fetch the repository data from Github API
    response = requests.get(f"{API_ENDPOINT}/repos/{GITHUB_USER}/{repository}", headers={"Authorization": f"token {ACCESS_TOKEN}"})
    if response.status_code != 200:
        print(f"Error fetching repository {repository}: {response.json()['message']}")
        return

    # Add the repository to the dependencies data
    dependencies_data[repository] = {"dependencies": [], "depth": depth}

    # Fetch the dependency data for the repository
    dependency_response = requests.get(response.json()["dependencies_url"], headers={"Authorization": f"token {ACCESS_TOKEN}"})
    if dependency_response.status_code == 200:
        for dependency in dependency_response.json():
            # Add the dependency to the repository's dependencies
            dependencies_data[repository]["dependencies"].append(dependency["name"])
            # Recursively fetch dependencies for the dependency
            get_dependencies(dependency["name"], depth + 1)

# Fetch dependencies for each repository in the user's repositories
response = requests.get(f"{API_ENDPOINT}/users/{GITHUB_USER}/repos", headers={"Authorization": f"token {ACCESS_TOKEN}"})
if response.status_code == 200:
    for repository in response.json():
        get_dependencies(repository["name"], 0)

# Save the dependencies data to a JSON file
with open(f"{GITHUB_USER}_dependencies.json", "w") as file:
    json.dump(dependencies_data, file)
