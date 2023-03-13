import requests

auth = ("lokeshAgnihotri", "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")

response = requests.get("https://api.github.com/user", auth=auth)

print(response.status_code)