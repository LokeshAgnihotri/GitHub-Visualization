import time
import requests
import json
import argparse
from splunk_http_event_collector import http_event_collector
import base64

# GitHub API endpoint
API_ENDPOINT = "https://api.github.com/users/{user}/repos"

# GitHub authentication credentials (replace with your own values)
auth = ("LokeshAgnihotri", "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")

# Create event collector object
http_event_collector_key = "f6a91647-602a-4309-8ec7-ad5a46e53839"
http_event_collector_host = "si-i-0efad00b65fa4efc2.prd-p-ngvek.splunkcloud.com"
hec = http_event_collector(http_event_collector_key, http_event_collector_host)

# Define argparse options
parser = argparse.ArgumentParser(description="Retrieve a list of GitHub repositories and their dependencies for a given user")
parser.add_argument("username", type=str, help="The GitHub username to retrieve repositories for")

# Parse command line arguments
args = parser.parse_args()

# Make API request to get list of repositories for the user
repo_api_url = API_ENDPOINT.format(user=args.username)
response = requests.get(repo_api_url, auth=auth, verify=True)

if response.status_code == 200:
    # Iterate through each repository
    for repo in response.json():
        # Create a dictionary to store the repository name and its dependencies
        repository = {"repository_name": repo["name"], "dependencies": []}
        
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
                    repository["dependencies"].append({"dependency_name": name, "dependency_version": version})
        
        # Create a dictionary with a key named "repository" that contains the repository and its dependencies
        data = {"repository": repository}
    
        # Convert the dictionary to a JSON object
        json_data = json.dumps(data)
    
        # Send the JSON object to Splunk using HTTP Event Collector
        payload = {
            "index": "main", 
            "sourcetype": "github_repository", 
            "source": "github", 
            "host": "my_host", 
            "event": json_data,
            "time": int(time.time())
        }
    
        hec.batchEvent(payload)
        hec.flushBatch()
else:
    print("Error getting repositories for user: ", response.status_code)
