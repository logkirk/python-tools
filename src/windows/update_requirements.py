import ctypes
import sys
import os
from pathlib import Path
from subprocess import run

PROXY = ""
REQUIREMENTS_FILE_NAME = "requirements.txt"


def handle_input(prompt, allowed_inputs):
    while True:
        ans = input(prompt + " ({})".format("/".join(allowed_inputs)))
        if ans in allowed_inputs:
            return ans
        else:
            print("\nYour input was invalid.\n")


# Check for admin permissions
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    raise PermissionError("Relaunch script as admin.")

project_root = Path(__file__).resolve().parents[1]
requirements_path = Path(project_root, REQUIREMENTS_FILE_NAME)

# Check for virtual environment
python_path = None
if "venv" in os.listdir(project_root):
    # Virtual environment detected
    virtual_env_path = Path(project_root, "venv", "Scripts", "python.exe")
    ans = handle_input(
        "Virtual environment detected:\n{}\n\nIs this the Python environment you want "
        "to use?".format(virtual_env_path),
        ["y", "n"],
    )
    print()
    if ans == "y":
        # Use virtual environment Python
        python_path = virtual_env_path
        command = '"{}" -m pip install -r "{}" --proxy={}'.format(
            python_path, requirements_path, PROXY
        )

if python_path is None:
    # Either virtual environment was not detected or user chose not to use it
    python_path = Path(sys.executable)
    command = 'pip install -r "{}" --proxy={}'.format(requirements_path, PROXY)
    ans = handle_input(
        "Current runtime Python environment:\n{}\n\nIs this the Python environment "
        "you want to use?".format(python_path),
        ["y", "n"],
    )
    print()
    if ans == "n":
        # User has exhausted all available Python choices
        raise RuntimeError("No suitable Python environment found.")

# Do pip install
requirements_path = Path(project_root, REQUIREMENTS_FILE_NAME)
print("Running command: {}\n".format(command))
result = run(command, shell=True, capture_output=True, text=True)

# Print command output
for out in [result.stdout, result.stderr]:
    if out != "":
        print(out)

if result.returncode != 0:
    raise RuntimeError("Requirements update failed.")
else:
    print("Requirements update done.")
