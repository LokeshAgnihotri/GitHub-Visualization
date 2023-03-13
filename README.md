# Project: Github Dependency Visualization in Splunk

This project is aimed at providing a visualization of the Github dependencies for all repositories of a particular Github user. The project makes use of the Github API to retrieve the dependencies and the Splunk tool for visualization.

## Requirements

- Python 3.x installed on your system.
- `pip` package manager.
- A Github account with repositories.
- Splunk Enterprise installed on your system.

## Installation

1. Clone this repository: 
$ git clone https://github.com/<username>/<repository-name>.git
2. Navigate to the cloned directory:
$ cd <repository-name>
3. Install the necessary dependencies:
$ pip install -r requirements.txt

## Configuration

1. Generate a Github token to access the Github API. You can create a token from your Github account settings page.

2. Create a `config.py` file and add your Github token:

```python
GITHUB_TOKEN = '<your-github-token>'
Open config.py file and add the Github username:
GITHUB_USERNAME = '<github-username>'
$ python github_dependencies.py
The script will retrieve all the repositories for the specified Github user and their dependencies. The output will be stored in dependencies.json.

The dependencies.json file will be sent to Splunk automatically.

Once the file is received by Splunk, you can create a dashboard to visualize the dependencies. Splunk has a wide variety of visualization options to choose from.
With this project, you can easily retrieve and visualize the Github dependencies for a particular Github user. This can be useful for managing large codebases and identifying potential issues with dependencies. 


