import json
import requests

# GitHub API endpoint for getting repositories
REPO_API_ENDPOINT = "https://api.github.com/users/{}/repos"

# List of dependency file names to search for
DEPENDENCY_FILENAMES = ["requirements.txt", "package.json", "Gemfile.lock"]

# GitHub username to retrieve repositories for
username = "LokeshAgnihotri"

# GitHub authentication credentials (replace with your own values)
auth = ("LokeshAgnihotri", "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")

# Dictionary to store dependencies for all repositories
all_dependencies = {}

# Make API request to get list of repositories for the user
repo_api_url = REPO_API_ENDPOINT.format(username)
response = requests.get(repo_api_url, auth=auth)

if response.status_code == 200:
    # Iterate through each repository
    for repo in response.json():
        print("Processing repository: ", repo["name"])
        
        # Initialize list to store dependencies for this repository
        dependencies = []
        
        # Make API request to get contents of repository
        contents_api_url = "{}/contents".format(repo["url"])
        response = requests.get(contents_api_url, auth=auth)
        
        if response.status_code == 200:
            # Iterate through each file in the repository
            for file in response.json():
                # Check if file is a dependency file
                if file["name"] in DEPENDENCY_FILENAMES:
                    # Make API request to get contents of dependency file
                    file_api_url = file["url"]
                    response = requests.get(file_api_url, auth=auth)
                    
                    if response.status_code == 200:
                        # Process dependency file contents (e.g. extract dependencies)
                        # Here you can store or process the dependencies as needed
                        dependencies.append({
                            "file_name": file["name"],
                            "content": response.content.decode("utf-8")
                        })
                    else:
                        print("Error getting file contents: ", response.status_code)
        else:
            print("Error getting repository contents: ", response.status_code)
        
        # Add dependencies to dictionary for all repositories
        all_dependencies[repo["name"]] = dependencies
    
    # Write dependencies for all repositories to single JSON file
    output_filename = "all_dependencies.json"
    with open(output_filename, "w") as f:
        json.dump(all_dependencies, f, indent=2)
else:
    print("Error getting repositories for user: ", response.status_code)
