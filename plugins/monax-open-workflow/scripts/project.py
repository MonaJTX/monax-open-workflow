"""Project-only onboarding and structural checks. No network or host config writes."""
import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PLUGIN = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
MARKER = "<!-- monax-open-workflow:v1 -->"
RULE_NAMES = ("catalog.json", "context.md", "memory.md", "boundaries.md",
              "development.md", "design-review.md", "game-development.md",
              "game-methods.md", "ai-video.md", "ai-video-directing.md",
              "ai-video-prompts.md", "ai-video-production.md", "verification.md")
TEMPLATE_NAMES = ("video-brief.md", "shot-package.md", "production-ledger.md")
OWNERS = {"identity": "PROJECT_CONTEXT/project_identity.md",
          "phase": "PROJECT_CONTEXT/current_phase.md",
          "architecture": "PROJECT_CONTEXT/architecture_coding_rules.md",
          "memory": "PROJECT_CONTEXT/memory_notes.md"}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def guarded(path):
    """Reject symlinks/junctions before resolving, including existing parents."""
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        attributes = getattr(part.lstat(), "st_file_attributes", 0) if part.exists() else 0
        if part.is_symlink() or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            raise ValueError("Linked paths are unsupported: " + str(part))
    return path


def project_root(value):
    root = guarded(value)
    if not root.is_dir() or root == Path(root.anchor):
        raise ValueError("Use an existing project directory, not a drive/filesystem root")
    return root


def local(root, relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("Invalid project-relative path")
    parts = Path(relative).parts
    if Path(relative).is_absolute() or ":" in relative or ".." in parts:
        raise ValueError("Path must remain inside this project")
    target = guarded(root / relative)
    if not target.is_relative_to(root):
        raise ValueError("Path escaped project")
    return target


def planned_files():
    files = {".monax-workflow/rules/" + name: (PLUGIN / "rules" / name).read_bytes()
             for name in RULE_NAMES}
    hashes = {name: digest(files[".monax-workflow/rules/" + name]) for name in RULE_NAMES}
    for name in TEMPLATE_NAMES:
        files[".monax-workflow/templates/" + name] = (PLUGIN / "templates" / name).read_bytes()
    template_hashes = {name: digest(files[".monax-workflow/templates/" + name]) for name in TEMPLATE_NAMES}
    files[".monax-workflow/project.json"] = json_bytes({
        "schema_version": 1, "package": "monax-open-workflow", "package_version": VERSION,
        "rule_hashes": hashes, "template_hashes": template_hashes})
    files["AGENTS.md"] = (MARKER + "\n# MonaX Project Entry\n\n"
        "先读 `.monax-workflow/rules/context.md`。项目回答和改动前，从 `PROJECT_CONTEXT/README.md` "
        "检索匹配长期约束；集合项目继续到所选子项目索引并读取规则正文。\n\n"
        "只按任务读取 `.monax-workflow/rules` 的对应 owner，不全量加载历史或规则。"
        "具体授权由用户请求与有效会话决定；本入口不授予插件安装、宿主配置或额外写入权限。\n"
    ).encode("utf-8")
    files["PROJECT_CONTEXT/README.md"] = ("# Project Context Index\n\n"
        "索引只提供任务→长期规则/状态 owner 指针，不复制正文。\n\n"
        "| 任务 | Owner |\n| --- | --- |\n"
        "| 项目身份与目标 | [project_identity.md](project_identity.md) |\n"
        "| 当前阶段与接续 | [current_phase.md](current_phase.md) |\n"
        "| 架构、资源与编码约束 | [architecture_coding_rules.md](architecture_coding_rules.md) |\n"
        "| 长期决定、问题与验收 | [memory_notes.md](memory_notes.md) |\n"
        "| 规则激活与缺口 | [workflow_activation_profile.json](workflow_activation_profile.json) |\n"
    ).encode("utf-8")
    files[OWNERS["identity"]] = ("# Project Identity\n\n"
        "- 项目名称：TODO 从当前项目核验\n- 项目类型与工具实际版本：TODO\n"
        "- 目标平台或交付规格：TODO\n- 当前目标与需求 owner：TODO\n"
    ).encode("utf-8")
    files[OWNERS["phase"]] = ("# Current Phase\n\n"
        "- 当前阶段与目标：TODO\n- 已完成及证据：TODO\n"
        "- 剩余工作、阻断和下一步：TODO\n- 日期/版本与失效条件：TODO\n"
    ).encode("utf-8")
    files[OWNERS["architecture"]] = ("# Architecture and Coding Constraints\n\n"
        "- 运行入口或生产路线与 owner：TODO\n- 配置、素材与版本来源：TODO\n"
        "- 必须保留的接口/数据/视觉边界：TODO\n- 实际构建或交付验证方式：TODO\n"
    ).encode("utf-8")
    files[OWNERS["memory"]] = ("# Durable Project Memory\n\n"
        "按现行结论、适用对象、证据 owner、日期/版本、失效条件记录。"
        "旧问题状态、验证层级和用户验收分别维护；没有发生的决定不预填。\n\n"
        "分发状态：Local Private / None，直到实际核验 Git 跟踪或交付渠道后更新。\n"
    ).encode("utf-8")
    catalog = json.loads(files[".monax-workflow/rules/catalog.json"])
    files["PROJECT_CONTEXT/workflow_activation_profile.json"] = json_bytes({
        "schema_version": 1, "active_rules": list(catalog["rules"]),
        "conditional_rules": list(catalog["conditional_rules"]),
        "project_owners": OWNERS, "blocking_items": ["TODO 核验并填写项目身份、阶段和架构"]})
    return files


def initialize(root, apply=False):
    files = planned_files()
    # Check all targets before any write. Existing files belong to their owner.
    conflicts = []
    for name in files:
        target = local(root, name)
        if target.exists():
            conflicts.append(name)
        for parent in target.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                conflicts.append(str(parent.relative_to(root)))
    result = {"status": "Conflict" if conflicts else "Planned",
              "created": [], "planned": list(files), "conflicts": sorted(set(conflicts))}
    if conflicts or not apply:
        return result
    created = []
    directories = []
    try:
        for name, data in files.items():
            target = local(root, name)
            missing = []
            parent = target.parent
            while parent != root and not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                guarded(directory)
                directory.mkdir()  # Do not claim directories another process created.
                directories.append(directory)
            # Exclusive creation prevents racing writes from overwriting existing files.
            with target.open("xb") as stream:
                created.append((target, data))
                stream.write(data)
        result.update(status="Created", created=[str(p.relative_to(root)) for p, _ in created])
        return result
    except Exception as error:
        # Preserve partial results for review. No automatic deletion races other writers.
        return {**result, "status": "Failed", "error": str(error),
                "residuals": [str(p.relative_to(root)) for p, _ in created],
                "created_directories": [str(p.relative_to(root)) for p in directories]}


def read_json(root, relative):
    value = json.loads(local(root, relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object: " + relative)
    return value


def check(root):
    issues = []
    pending = []
    try:
        marker = read_json(root, ".monax-workflow/project.json")
        if marker.get("schema_version") != 1 or marker.get("package") != "monax-open-workflow":
            issues.append("Invalid project marker")
        if marker.get("package_version") != VERSION:
            issues.append("Version mismatch; review migration before updating")
        hashes = marker.get("rule_hashes", {})
        if not isinstance(hashes, dict) or set(hashes) != set(RULE_NAMES):
            issues.append("Incomplete rule hashes")
        else:
            for name in RULE_NAMES:
                if digest(local(root, ".monax-workflow/rules/" + name).read_bytes()) != hashes[name]:
                    issues.append("Rule drift: " + name)
        catalog = json.loads((PLUGIN / "rules/catalog.json").read_text(encoding="utf-8"))
        template_hashes = marker.get("template_hashes", {})
        if not isinstance(template_hashes, dict) or set(template_hashes) != set(TEMPLATE_NAMES):
            issues.append("Incomplete template hashes")
        else:
            for name in TEMPLATE_NAMES:
                if digest(local(root, ".monax-workflow/templates/" + name).read_bytes()) != template_hashes[name]:
                    issues.append("Template drift: " + name)
        entry = local(root, "AGENTS.md").read_text(encoding="utf-8")
        for pointer in (MARKER, ".monax-workflow/rules/context.md", "PROJECT_CONTEXT/README.md"):
            if pointer not in entry:
                issues.append("Entry missing: " + pointer)
        index = local(root, "PROJECT_CONTEXT/README.md").read_text(encoding="utf-8")
        profile = read_json(root, "PROJECT_CONTEXT/workflow_activation_profile.json")
        if profile.get("schema_version") != 1:
            issues.append("Invalid activation schema")
        for key in ("active_rules", "conditional_rules"):
            values = profile.get(key)
            allowed = set(catalog["rules" if key == "active_rules" else "conditional_rules"])
            if not isinstance(values, list) or any(not isinstance(x, str) for x in values):
                issues.append("Invalid " + key)
            elif len(values) != len(set(values)) or set(values) != allowed:
                issues.append("Unknown, duplicate or missing rule IDs: " + key)
        owners = profile.get("project_owners", {})
        if not isinstance(owners, dict) or set(owners) != set(OWNERS):
            issues.append("Project owner roles missing or unknown")
        else:
            if any(not isinstance(value, str) for value in owners.values()):
                raise ValueError("Project owner paths must be strings")
            if len(set(owners.values())) != len(owners):
                issues.append("Duplicate project owners")
            for role, name in owners.items():
                if not isinstance(name, str) or not name.startswith("PROJECT_CONTEXT/") or not name.endswith(".md"):
                    issues.append("Owner must be a project Markdown file: " + role)
                    continue
                content = local(root, name).read_text(encoding="utf-8")
                if Path(name).name not in index and name not in index:
                    issues.append("Index does not discover owner: " + name)
                # Presence is structural evidence; semantics still require a human/agent review.
                meaningful = [line for line in content.splitlines()
                              if line.strip() and not line.lstrip().startswith("#")]
                if not meaningful or re.search(r"\bTODO\b|\bTBD\b|待填写|待核验", content, re.I):
                    pending.append("Unresolved project facts: " + name)
        blockers = profile.get("blocking_items")
        if not isinstance(blockers, list) or any(not isinstance(x, str) or not x.strip() for x in blockers):
            issues.append("Invalid blocking_items")
        else:
            pending.extend(blockers)
    except (OSError, ValueError, TypeError) as error:
        issues.append(str(error))
    return {"status": "Blocked" if issues else "NeedsProjectFacts" if pending else "Ready",
            "ready": not issues and not pending, "issues": issues, "pending": pending,
            "runtime": "Unverified", "user_acceptance": "Unknown",
            "scope": "Structural only; not behavior, media quality, rights or platform validation"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "check"))
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    try:
        root = project_root(args.project_root)
        if (args.action == "check" and args.apply) or (args.action == "init" and args.require_ready):
            raise ValueError("--apply only applies to init; --require-ready only applies to check")
        result = initialize(root, args.apply) if args.action == "init" else check(root)
        code = 1 if result["status"] in ("Conflict", "Failed", "Blocked") else 0
        if args.require_ready and not result.get("ready"):
            code = 1
    except (OSError, ValueError) as error:
        result, code = {"status": "Blocked", "error": str(error)}, 1
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
