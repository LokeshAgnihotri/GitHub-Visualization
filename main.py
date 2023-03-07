import os
import subprocess
import PySimpleGUI as sg
from github import Github
from pydeps import pydeps

# Create the PySimpleGUI layout
layout = [
    [sg.Text("Enter the Github username:")],
    [sg.Input(key="-USERNAME-")],
    [sg.Button("Load Repos")],
    [sg.Listbox([], size=(40, 20), key="-REPOS-")],
    [sg.Button("Select Repos"), sg.Button("Clone Repos")],
    [sg.Listbox([], size=(40, 20), key="-SELECTED-")],
    [sg.Button("Analyze Dependencies"), sg.Button("Find Common Dependencies")],
    [sg.Listbox([], size=(40, 20), key="-DEPENDENCIES-")]
]

# Create the PySimpleGUI window
window = sg.Window("Github Repo Dependency Analyzer", layout)

# Event loop to process events and get values from inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Load Repos":
        try:
            # Authenticate with the Github API
            g = Github()
            user = g.get_user(values["-USERNAME-"])
            repos = [repo.name for repo in user.get_repos() if not repo.private]
            # Update the Listbox with the user's public repos
            window["-REPOS-"].update(repos)
        except:
            sg.popup("Error: Invalid username or connection problem")
    if event == "Select Repos":
        selected_repos = values["-REPOS-"]
        # Update the Listbox with the selected repos
        window["-SELECTED-"].update(selected_repos)
    if event == "Clone Repos":
        selected_repos = values["-SELECTED-"]
        for repo_name in selected_repos:
            try:
                # Clone the repo using git
                subprocess.run(["git", "clone", f"https://github.com/{values['-USERNAME-']}/{repo_name}.git"])
            except:
                sg.popup(f"Error: Unable to clone {repo_name}")
    if event == "Analyze Dependencies":
        selected_repos = values["-SELECTED-"]
        dependencies = []
        for repo_name in selected_repos:
            # Analyze the dependencies using pydeps
            pd = pydeps.pydeps()
            pd.analyze(os.path.join(os.getcwd(), repo_name))
            repo_dependencies = pd.list_dependencies()
            dependencies.extend(repo_dependencies)
        # Update the Listbox with the dependencies
        window["-DEPENDENCIES-"].update(dependencies)
    if event == "Find Common Dependencies":
        selected_repos = values["-SELECTED-"]
        dependencies = []
        for repo_name in selected_repos:
            # Analyze the dependencies using pydeps
            pd = pydeps.pydeps()
            pd.analyze(os.path.join(os.getcwd(), repo_name))
            repo_dependencies = pd.list_dependencies()
            dependencies.append(set(repo_dependencies))
        # Find the intersection of the dependencies
        common_dependencies = set.intersection(*dependencies)
        # Update the Listbox with the common dependencies
        window["-DEPENDENCIES-"].update(common_dependencies)

# Close the PySimpleGUI window
window.close()
