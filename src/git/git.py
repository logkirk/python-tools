from src.command import run_cmd


def git_fetch_all():
    print("Fetching all branches from origin...")
    run_cmd(["git", "fetch", "origin"])


def git_checkout(branch):
    print("Checking out branch {}...".format(branch))
    run_cmd(["git", "checkout", branch])


def git_merge(source, target, confirm=True):
    """Merges source into target."""
    print("Merging branch {} into {}...".format(source, target))
    if confirm:
        input("Press ENTER to proceed...")
    git_checkout(target)
    run_cmd(["git", "merge", source], print_output=True)


def git_rebase(a, b, confirm=True):
    """Rebases branch a onto branch b."""
    print("Rebasing branch {} onto {}...".format(a, b))
    if confirm:
        input("Press ENTER to proceed...")
    git_checkout(a)
    run_cmd(["git", "rebase", b])


def git_reset_to_origin(branch, confirm=True):
    remote = "origin/{}".format(branch)
    print("Resetting branch {} to {}...".format(branch, remote))
    if confirm:
        input("Press ENTER to proceed...")
    git_checkout(branch)
    run_cmd(["git", "reset", "--hard", remote])


def git_clean_recurse_force(confirm=True):
    print("Cleaning up working tree recursively...")
    if confirm:
        run_cmd(["git", "clean", "-d", "--force", "--dry-run"], print_output=True)
        input("Press ENTER to proceed...")
    run_cmd(["git", "clean", "-d", "--force"])


def git_push(branch):
    print("Pushing branch {} to origin...".format(branch))
    git_checkout(branch)
    run_cmd(["git", "push", "origin"], print_output=True)


def git_force_push(branch):
    print("Force pushing {} to origin...".format(branch))
    input(
        "WARNING! This action may unintentionally overwrite changes on the remote. "
        "Press ENTER to proceed..."
    )
    git_checkout(branch)
    run_cmd(["git", "push", "--force-with-lease", "origin"], print_output=True)
