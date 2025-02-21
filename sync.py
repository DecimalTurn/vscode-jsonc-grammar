import requests
import os

def run_update(commit_message):

    # Let's run the git commands to update the file

    os.system("git config --global user.email '41898282+github-actions[bot]@users.noreply.github.com'")
    os.system("git config --global user.name 'github-actions[bot]'")

    os.system("git add JSONC.tmLanguage.json")
    os.system("git add retries.txt")
    os.system("git add disabled.txt")
    os.system(f"git commit -m '{commit_message}'")
    os.system("git push")

def create_github_issue(slug, title, body, labels=None):

    token = os.getenv('GITHUB_TOKEN')

    url = f"https://api.github.com/repos/{slug}/issues"
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}'
    }
    data = {
        'title': title,
        'body': body,
        'labels': labels if labels else []  # Use the provided labels or an empty list if none are given
    }
    
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"🟢 Issue created successfully: {response.json()['html_url']}")
        return response.json()['number']
    else:
        print(f"🔴 Failed to create issue. Status code: {response.status_code}")
        print(response.json())


# Let's check if the program is disabled
retries_limit = 3

# If the disable.txt file exists and contains the word "True", exit the program
if os.path.exists("disabled.txt"):
    with open('disabled.txt') as file:
        if file.readline().strip() == "True":
            print("The program is disabled. Exiting")
            exit(0)

url = "https://raw.githubusercontent.com/microsoft/vscode/main/extensions/json/syntaxes/JSONC.tmLanguage.json"
response = requests.get(url)


# If the request returned an error, let's stop the script and return the error. Also create an issue on the repository
if not response.ok:
    print(f"🔴 Error: {response.status_code}")
    print(response.text)
    
    # Increase the retries count in retries.txt
    retries = 0
    with open('retries.txt', 'r+') as file:
        retries = int(file.readline().strip())
        print(f"This was retry number {retries}")
        retries += 1
        file.seek(0)
        file.write(str(retries))
        file.truncate()
    
    if retries == retries_limit + 1:
        print("Retries exceeded. Disabling the program")
        with open('disabled.txt', 'w') as file:
            file.write("True")
        create_github_issue(os.getenv('GITHUB_REPOSITORY'), "Failed to fetch JSONC.tmLanguage.json", response.text, ["bug"])
    elif retries > retries_limit + 1:
        # This should never happen, but just in case
        print("Retries exceeded. Disabling the program")
        with open('disabled.txt', 'w') as file:
            file.write("True")
    else:
        print("Retrying later...")
    
    run_update("Updating retry counter")
    exit(0)

else:
    print("🟢 Request successful")
    with open('retries.txt', 'w') as file:
        file.write("0")

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

run_update("Updating JSONC.tmLanguage.json")