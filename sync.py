import requests
import os

def run_update():

    # Let's run the git commands to update the file

    os.system("git config --global user.email '41898282+github-actions[bot]@users.noreply.github.com'")
    os.system("git config --global user.name 'github-actions[bot]'")

    os.system("git add JSONC.tmLanguage.json")
    os.system("git commit -m 'Updated JSONC.tmLanguage.json'")
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
if os.path.exists("disable.txt"):
    with open('disable.txt') as file:
        if file.readline().strip() == "True":
            print("The program is disabled. Exiting")
            exit(0)

url = "https://raw.githubusercontent.com/microsoft/vscode/main/extensions/json/syntaxes/JSONC.tmLanguage.json-test-error"
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
    
    if retries >= retries_limit:
        print("Retries exceeded. Disabling the program")
        with open('disable.txt', 'w') as file:
            file.write("True")
        create_github_issue(os.getenv('GITHUB_REPOSITORY'), "Failed to fetch JSONC.tmLanguage.json", response.text, ["bug"])
        exit(0)

    run_update()

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

run_update()