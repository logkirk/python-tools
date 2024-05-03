from src.git.git import git_rebase, git_merge, git_fetch_all

MAIN_FEATURE_BRANCH = ""
DEVELOPMENT_BRANCH = "development"

BRANCHES_TO_MERGE = []
BRANCHES_TO_REBASE = []

if not MAIN_FEATURE_BRANCH:
    raise RuntimeError("Main feature branch not provided.")
if not DEVELOPMENT_BRANCH:
    raise RuntimeError("Development branch not provided.")

print("Operations to be executed:")
print("Merge development into main feature branch:")
print('        Merge "{}" into "{}"'.format(DEVELOPMENT_BRANCH, MAIN_FEATURE_BRANCH))
if BRANCHES_TO_MERGE:
    print("Merge main feature branch into PR feature branches:")
    for branch in BRANCHES_TO_MERGE:
        print('        Merge "{}" into "{}"'.format(MAIN_FEATURE_BRANCH, branch))
if BRANCHES_TO_REBASE:
    print("Rebase current feature branch onto main feature branch:")
    for branch in BRANCHES_TO_REBASE:
        print('        Rebase "{}" onto "{}"'.format(branch, MAIN_FEATURE_BRANCH))
    print()
input("Press ENTER to confirm these actions and continue...")

git_fetch_all()
git_merge(source=DEVELOPMENT_BRANCH, target=MAIN_FEATURE_BRANCH)

for branch in BRANCHES_TO_MERGE:
    git_merge(source=MAIN_FEATURE_BRANCH, target=branch)

for branch in BRANCHES_TO_REBASE:
    git_rebase(a=branch, b=MAIN_FEATURE_BRANCH)
