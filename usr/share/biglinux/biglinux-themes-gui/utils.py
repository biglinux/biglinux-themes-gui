"""
Utils module for BigLinux Themes GUI.
Contains utility functions for running shell commands and processing data.
"""

import subprocess
import os
from typing import List


def get_current_dir() -> str:
    """Get the directory of the current script."""
    return os.path.dirname(os.path.abspath(__file__))


def run_shell_command(command: str) -> str:
    """Run a shell command and return its output as a string."""
    print(f"Executing command: {command}")
    result = subprocess.run(
        command,
        shell=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(f"Command failed with return code: {result.returncode}")
        print(f"Error output: {result.stderr}")

    output = result.stdout.strip()
    if len(output) > 100:
        print(f"Command output (truncated): {output[:100]}...")
    else:
        print(f"Command output: {output}")

    return output


def run_shell_script(script_name: str, *args) -> str:
    """Run a shell script in the current directory with arguments."""
    script_path = os.path.join(get_current_dir(), script_name)
    args_str = " ".join(str(arg) for arg in args)
    command = f"{script_path} {args_str}"
    print(f"Running script: {script_name} with args: {args_str}")
    return run_shell_command(command)


def get_list_from_script(script_name: str) -> List[str]:
    """Run a script and return its output as a list of strings."""
    output = run_shell_script(script_name)
    return [line for line in output.split("\n") if line.strip()]


def get_current_desktop() -> str:
    """Get the current desktop configuration."""
    return run_shell_script("actual-desktop.sh")


def get_current_theme() -> str:
    """Get the current theme."""
    return run_shell_script("actual-theme.sh")


def get_desktop_list() -> List[str]:
    """Get list of available desktop configurations."""
    return get_list_from_script("list-desktops.sh")


def get_theme_list() -> List[str]:
    """Get list of available themes."""
    return get_list_from_script("list-themes.sh")


def check_desktop_used(desktop: str) -> bool:
    """Check if a desktop has been used before."""
    # The correct way to call the script is to pass desktop as an argument, not with a question mark
    result = run_shell_script("used-desktop.sh", desktop)
    return result.strip() != "false"


def apply_desktop(desktop: str, clean: str = "") -> None:
    """Apply a desktop configuration, optionally with clean flag."""
    run_shell_script("apply-desktop.sh", desktop, clean)


def apply_theme(theme: str) -> None:
    """Apply a theme."""
    run_shell_script("apply-theme.sh", theme)
