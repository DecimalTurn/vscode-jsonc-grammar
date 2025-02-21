import requests
import os

url = "https://raw.githubusercontent.com/microsoft/vscode/main/extensions/json/syntaxes/JSONC.tmLanguage.json"
response = requests.get(url)

# Let's use the hash of the file content to check if we need to update it
remote_hash = hash(response.text)
print(f"Remote Hash: {remote_hash}")

# Let's read the local file
with open("JSONC.tmLanguage.json", "r") as file:
    local_data = file.read()
    local_hash = hash(local_data)
    print(f"Local Hash: {local_hash}")

    if remote_hash != local_hash:
        print("Files are different. Updating local file")
        with open("JSONC.tmLanguage.json", "w") as file:
            file.write(response.text)
    else:
        print("Files are the same. No need to update")

# Let's run the git commands to update the file

os.system("git config --global user.email '41898282+github-actions[bot]@users.noreply.github.com'")
os.system("git config --global user.name 'github-actions[bot]'")

os.system("git add JSONC.tmLanguage.json")
os.system("git commit -m 'Updated JSONC.tmLanguage.json'")
os.system("git push")

