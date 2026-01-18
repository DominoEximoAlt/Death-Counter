import subprocess
from pathlib import Path

def get_git_version():
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return tag.lstrip("v")
    except Exception:
        return "0.0.0"

version = get_git_version()

path = Path("deathcounter/utils/version.py")
path.write_text(f'__version__ = "{version}"\n')

print(f"Version set to {version}")
