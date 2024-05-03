from src.git.git import git_fetch_all, git_push, git_force_push

BRANCHES_TO_PUSH = []
BRANCHES_TO_FORCE_PUSH = []

if not BRANCHES_TO_PUSH and not BRANCHES_TO_FORCE_PUSH:
    raise RuntimeError("No branches to push or force push provided.")

print("Operations to be executed:")
if BRANCHES_TO_PUSH:
    print("Push the following branches to origin:")
    for branch in BRANCHES_TO_PUSH:
        print("        {}".format(branch))
if BRANCHES_TO_FORCE_PUSH:
    print("Force push the following branches to origin:")
    for branch in BRANCHES_TO_FORCE_PUSH:
        print("        {}".format(branch))
print()
input("Press ENTER to confirm these actions and continue...")

git_fetch_all()

for branch in BRANCHES_TO_PUSH:
    git_push(branch)

for branch in BRANCHES_TO_FORCE_PUSH:
    git_force_push(branch)
