import subprocess


def run_cmd(cmd, shell=True, debug=False, print_output=False, raise_on_failure=True):
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    if debug:
        print("Running command: {}".format(result.args))
        if result.stderr != "":
            pretty_print_output(result.stderr.strip(), append="STDERR:  ")
        if result.stdout != "":
            pretty_print_output(result.stdout.strip(), append="STDOUT:  ")
    if print_output:
        if result.stderr != "":
            pretty_print_output(result.stderr.strip(), append="STDERR:  ")
        if result.stdout != "":
            pretty_print_output(result.stdout.strip())
    if raise_on_failure and result.returncode != 0:
        raise RuntimeError(
            "Command failed. Dumping command args, stderr, and "
            "stdout:\n\n{}\n{}\n{}".format(result.args, result.stderr, result.stdout)
        )
    return result


def pretty_print_output(output, indent=4, append=""):
    for line in output.split("\n"):
        print("{}{}{}".format(" " * indent, append, line))
