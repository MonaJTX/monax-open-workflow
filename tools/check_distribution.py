"""Offline inventory, UTF-8, link and heuristic privacy checks for this package."""
import argparse
import json
import re
import stat
import sys
from pathlib import Path
from urllib.parse import unquote

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
INVENTORY = "distribution-files.json"
ALLOWED_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml"}
SPECIAL_NAMES = {"LICENSE", ".gitignore"}
EXCLUDED_PARTS = {".git", "__pycache__", ".venv", "node_modules", "build", "releases", "demo-project"}
PATTERNS = {
    "absolute drive path": re.compile(r"(?<![A-Za-z])[A-Za-z]:[/\\]"),
    "personal home path": re.compile(r"(?:/Users/|/home/)[A-Za-z0-9_.-]+"),
    "email address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential-like token": re.compile(r"\b(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_-]{20,}"),
    "credential URL": re.compile(r"https?://[^\s)]+[?&](?:token|access_token|secret|signature)=[^\s)]+", re.I),
}


def safe_file(root, name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError("Invalid inventory path")
    rel = Path(name)
    if rel.is_absolute() or ".." in rel.parts or any(p in EXCLUDED_PARTS for p in rel.parts):
        raise ValueError("Unsafe inventory path: " + name)
    path = root / rel
    for part in (path, *path.parents):
        if part == root.parent:
            break
        attrs = getattr(part.lstat(), "st_file_attributes", 0) if part.exists() else 0
        if part.is_symlink() or attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            raise ValueError("Linked distribution path: " + name)
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError("Missing or escaped inventory file: " + name)
    return path


def inventory(root):
    value = json.loads(safe_file(root, INVENTORY).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("Invalid distribution inventory")
    names = value.get("files")
    if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
        raise ValueError("Invalid files list")
    if len(names) != len(set(names)) or INVENTORY not in names:
        raise ValueError("Duplicate files or inventory missing from itself")
    return names


def check(root=ROOT):
    root = Path(root).resolve()
    issues = []
    try:
        names = inventory(root)
    except (OSError, ValueError, TypeError) as error:
        return {"success": False, "files": 0, "issues": [str(error)]}
    listed = set(names)
    for name in names:
        try:
            path = safe_file(root, name)
            if path.suffix not in ALLOWED_SUFFIXES and path.name not in SPECIAL_NAMES:
                issues.append(name + ": unapproved file type")
            if path.name.startswith(".env"):
                issues.append(name + ": environment file is not distributable")
            body = path.read_text(encoding="utf-8")
            for label, pattern in PATTERNS.items():
                if pattern.search(body):
                    issues.append(name + ": " + label)  # Do not echo potential secrets.
            if path.suffix == ".json":
                json.loads(body)
            if path.suffix == ".md":
                for link in re.findall(r"\]\(([^)\s]+)\)", body):
                    if link.startswith(("https://", "http://", "#")):
                        continue
                    local = unquote(link.split("#", 1)[0])
                    target = (path.parent / local).resolve()
                    if not target.is_relative_to(root) or target.relative_to(root).as_posix() not in listed:
                        issues.append(name + ": unlisted or external local link: " + local)
                    elif not target.is_file():
                        issues.append(name + ": missing link: " + local)
        except (OSError, ValueError, TypeError) as error:
            issues.append(name + ": " + str(error))
    # Report unexpected public source files; local build/demo/cache output is never exported.
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.is_file() and rel.as_posix() not in listed:
            issues.append(rel.as_posix() + ": not in explicit inventory")
    return {"success": not issues, "files": len(names), "issues": issues,
            "privacy_scope": "Heuristic scan plus explicit inventory; human review still required"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result["success"] else 1)
