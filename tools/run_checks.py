"""Run self-contained checks without installing a plugin or calling a service."""
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def main():
    commands = [
        [sys.executable, "-B", str(ROOT / "tools/check_distribution.py")],
        [sys.executable, "-B", "-m", "unittest", "discover", "-s",
         str(ROOT / "plugins/monax-open-workflow/tests"), "-p", "test_*.py", "-v"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"})
        if result.returncode:
            return result.returncode
    print("Package checks passed. Host runtime and user acceptance remain unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
