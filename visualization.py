import os
import subprocess

# Clone the repository to a local directory
subprocess.run(["git", "clone", "https://github.com/acheong08/EdgeGPT.git"])
# Navigate to the repository directory
os.chdir("EdgeGPT")
print(os.listdir())

# # Install pydeps
# subprocess.run(["pip", "install", "pydeps"])

# # Analyze the dependencies using pydeps
subprocess.run(["pydeps", "."])
