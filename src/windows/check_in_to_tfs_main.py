import shutil
import os
import argparse
from shutil import rmtree
from tempfile import gettempdir
from pathlib import Path
from stat import S_IWUSR

from src.command import run_cmd

WORKING_DIR = Path(gettempdir(), "workspace")
TFS_DIR = Path(WORKING_DIR, "TempTfsWorkspace")
TFS_SERVER_DIR = r"$/path/to/dir"
BITBUCKET_DIR = Path(WORKING_DIR, "TempBitbucketWorkspace")
COLLECTION_URL = r""
WORKSPACE_NAME = "TempWorkspace"
EXCLUDED_ITEMS = [".git", ".gitignore"]
BITBUCKET_WORKSPACE_NAME = ""
BITBUCKET_REPO_NAME = ""
DEPENDENCIES = {
    "Visual Studio": "tf.exe",
    "Team Foundation Server Power Tools": "tfpt.exe",
}


def onerror(func, path, excinfo):
    if excinfo[0] is FileNotFoundError:
        # Ignore FileNotFoundError
        return
    elif not os.access(path, os.W_OK):
        # Retry with correct permissions
        os.chmod(path, S_IWUSR)
        func(path)
    else:
        # Something unexpected happened and the dir could not be removed, so quit
        print(excinfo)
        exit(1)  # Must use exit since exceptions can't be raised in this func


def commit_changes():
    msg = input("Enter a commit message: ")
    run_cmd(
        ["tf", "checkin", "/recursive", "/noprompt", "/comment:" + msg, TFS_DIR],
        print_output=True,
    )


def clean_up():
    rmtree(WORKING_DIR, onerror=onerror)
    run_cmd(
        ["tf", "workfold", "/unmap", "/workspace:" + WORKSPACE_NAME, TFS_DIR],
        raise_on_failure=False,
    )
    run_cmd(
        [
            "tf",
            "workspace",
            "/delete",
            "/noprompt",
            "/collection:" + COLLECTION_URL,
            WORKSPACE_NAME,
        ],
        raise_on_failure=False,
    )


def verify_dependencies():
    for friendly_name, executable in DEPENDENCIES.items():
        verify_dependency(executable, friendly_name)


def verify_dependency(executable, friendly_name):
    try:
        run_cmd(["where", executable])
    except RuntimeError as e:
        raise RuntimeError(
            "{} not found in your path. Please install {} and add the install "
            "directory to your path.".format(executable, friendly_name)
        ) from e


# Parse program args
parser = argparse.ArgumentParser(description="Transfers code from Bitbucket to TFS.")
parser.add_argument(
    "--debug", action="store_true", help="enables debug logging to the console"
)
args = parser.parse_args()

verify_dependencies()

# Remove any leftover stuff from last time
print("Preparing workspace...")
clean_up()

# Get destination repo from TFS
print("Getting destination repository from TFS...")
os.mkdir(WORKING_DIR)
os.mkdir(TFS_DIR)
run_cmd(
    [
        "tf",
        "workspace",
        "/new",
        "/noprompt",
        WORKSPACE_NAME,
        "/collection:" + COLLECTION_URL,
    ]
)
run_cmd(
    [
        "tf",
        "workfold",
        "/workspace:" + WORKSPACE_NAME,
        TFS_SERVER_DIR,
        TFS_DIR,
    ]
)
run_cmd(["tf", "get", "/noprompt", "/all", "/recursive", TFS_DIR], shell=True)

# Get source repo from Bitbucket
print("Getting source repository from Bitbucket...")
bitbucket_username = input(
    "Enter your Bitbucket username (can be found at "
    "https://bitbucket.org/account/settings/): "
)
repo_url = "https://{}@bitbucket.org/{}/{}.git".format(
    bitbucket_username, BITBUCKET_WORKSPACE_NAME, BITBUCKET_REPO_NAME
)
run_cmd(["git", "clone", "-q", repo_url, BITBUCKET_DIR])

# Copy files from Bitbucket directory (source repo) to TFS directory (destination repo)
print(
    "Copying files from Bitbucket directory (source repo) to TFS directory "
    "(destination repo)..."
)
for dirpath, _, filenames in os.walk(TFS_DIR):
    os.chmod(dirpath, S_IWUSR)
    for file in filenames:
        os.chmod(Path(dirpath, file), S_IWUSR)

for item in (item for item in os.listdir(BITBUCKET_DIR) if item not in EXCLUDED_ITEMS):
    tfs_item_path = Path(TFS_DIR, item)
    bitbucket_item_path = Path(BITBUCKET_DIR, item)
    if os.path.isfile(bitbucket_item_path):
        shutil.copy(src=bitbucket_item_path, dst=tfs_item_path)
    else:
        if item in os.listdir(TFS_DIR):
            rmtree(tfs_item_path, onerror=onerror)
        shutil.copytree(src=bitbucket_item_path, dst=tfs_item_path)

# Prepare files in source repo for check-in
print("Staging files for check-in...")
run_cmd(["tf", "add", "/recursive", Path(TFS_DIR, "*")])
run_cmd(["tfpt", "online", "/noprompt", "/deletes", "/recursive", TFS_DIR])
run_cmd(["tfpt", "uu", "/noprompt", "/noget", "/recursive", TFS_DIR])

# Prompt user to confirm changes and commit
run_cmd(["tf", "status", "/recursive", TFS_DIR], print_output=True)
print()
ans = ""
while ans != "y" and ans != "n":
    ans = input(
        "Review the staged changes shown above for accuracy. "
        "Ready to check in these changes to TFS? [(y)es/(n)o] "
    ).lower()
    if ans == "y":
        commit_changes()
    elif ans == "n":
        print("No changes committed.")
    else:
        print("Your input was invalid.")

# Clean up
print("Cleaning up...")
clean_up()
print("Done.")
