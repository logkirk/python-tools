from src.git.git import git_reset_to_origin, git_clean_recurse_force, git_fetch_all

BRANCHES_TO_RESET = []

if not BRANCHES_TO_RESET:
    raise RuntimeError("No branches to reset provided.")

print("Operations to be executed:")
print("Reset all following branches to remote and clean working tree:")
for branch in BRANCHES_TO_RESET:
    print('        Reset branch "{}" to remote'.format(branch))
print()
input("Press ENTER to confirm these actions and continue...")

git_fetch_all()

for branch in BRANCHES_TO_RESET:
    git_reset_to_origin(branch)
    git_clean_recurse_force()
