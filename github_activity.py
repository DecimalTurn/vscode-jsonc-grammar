import datetime
import subprocess
import sys
import os

FILENAME = "Last_activity.txt"

def update_last_activity_file():
    today = datetime.date.today().isoformat()
    file_exists = os.path.isfile(FILENAME)

    try:
        with open(FILENAME, "w") as f:
            f.write(today + "\n")
        action = "Created" if not file_exists else "Updated"
        print(f"{action} {FILENAME} with date: {today}")
    except Exception as e:
        print(f"Failed to write to {FILENAME}: {e}")
        sys.exit(1)

def git_commit_and_push():
    try:
        subprocess.run(["git", "add", FILENAME], check=True)
        subprocess.run(["git", "commit", "-m", "Update Last_activity.txt with current date"], check=True)
        subprocess.run(["git", "push", "origin"], check=True)
        print("Changes pushed to origin successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_last_activity_file()
    git_commit_and_push()
