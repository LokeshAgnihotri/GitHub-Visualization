import requests
import json
from splunk_http_event_collector import http_event_collector
import base64

# GitHub API endpoint
API_ENDPOINT = "https://api.github.com/users/{user}/repos"

# GitHub authentication credentials (replace with your own values)
auth = ("LokeshAgnihotri", "enter your token erhe")

# GitHub username to retrieve repositories for
username = "nischay1234aa"

# Create event collector object
http_event_collector_key = "f6a91647-602a-4309-8ec7-ad5a46e53839"
http_event_collector_host = "si-i-0efad00b65fa4efc2.prd-p-ngvek.splunkcloud.com"
hec = http_event_collector(http_event_collector_key, http_event_collector_host)

# Make API request to get list of repositories for the user
repo_api_url = API_ENDPOINT.format(user=username)
response = requests.get(repo_api_url, auth=auth, verify=True)

if response.status_code == 200:
    # Create a list to store all the repositories and their dependencies
    repositories = []
    
    # Iterate through each repository
    for repo in response.json():
        # Create a dictionary to store the repository name and its dependencies
        repository = {"name": repo["name"], "dependencies": []}
        
        # Make API request to get the contents of the requirements.txt file for the repository
        contents_api_url = f"{repo['url']}/contents/requirements.txt"
        response = requests.get(contents_api_url, auth=auth, verify=True)
        
        # If the request is successful and the file exists, parse the dependencies and add them to the repository dictionary
        if response.status_code == 200:
            contents = response.json()
            content = contents['content']
            decoded_content = base64.b64decode(content).decode('utf-8')
            dependencies = decoded_content.split('\n')
            for dependency in dependencies:
                if dependency:
                    name, version = dependency.strip().split('==')
                    repository["dependencies"].append({"name": name, "version": version})
        
        # Append the repository dictionary to the repositories list
        repositories.append(repository)
    
    # Create a payload dictionary to send the repositories list as a JSON object
    payload = {"index": "main", "sourcetype": "github_repositories", "source": "github", "host": "my_host", "event": repositories}
    
    # Send the payload to Splunk using HTTP Event Collector
    hec.batchEvent(payload)
    hec.flushBatch()
else:
    print("Error getting repositories for user: ", response.status_code)
