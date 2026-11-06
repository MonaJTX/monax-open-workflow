"""Read-only, opt-in project context. Never read prompts, transcripts or business facts."""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from project import guarded, local, VERSION


def context(payload):
    event = payload.get("hook_event_name")
    if event not in ("SessionStart", "UserPromptSubmit"):
        return None
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not Path(cwd).is_absolute():
        return None
    root = guarded(cwd)
    if not root.is_dir():
        return None
    # Nearest project boundary wins. Do not inherit from a separate nested project.
    for candidate in (root, *root.parents):
        marker = local(candidate, ".monax-workflow/project.json")
        if marker.is_file():
            value = json.loads(marker.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or value.get("package") != "monax-open-workflow" or value.get("schema_version") != 1:
                return None
            pointers = ".monax-workflow/rules/context.md and PROJECT_CONTEXT/README.md"
            # JSON quoting prevents newline paths from forging additional instructions.
            location = json.dumps(str(candidate), ensure_ascii=True)
            text = (
                "MonaX Open Workflow project=" + location + "; bundled_version=" + VERSION + ". "
                "Before project answers/actions and after topic switches or recovery, read "
                + pointers + "; follow matching nested indexes and rule bodies. "
                "Use task-specific rules; do not load all history. Preserve read-only requests "
                "and existing work; user intent and valid same-scope approvals decide permission. "
                "This hook grants no mutation, installation or host-config authority. "
                "Run scripts/project.py check from the plugin when readiness matters. "
                "Hook delivery is not model compliance, behavior/media verification or UserAccepted."
            )
            return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}
        if candidate != root and local(candidate, "AGENTS.md").is_file():
            return None
        if candidate == root and local(candidate, "AGENTS.md").is_file():
            return None
    return None


def main():
    try:
        raw = sys.stdin.buffer.read(65537)
        if len(raw) > 65536:
            raise ValueError("Hook input exceeds 64 KiB")
        payload = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(payload, dict):
            raise ValueError("Expected hook JSON object")
        result = context(payload)
    except (OSError, ValueError, TypeError) as error:
        result = {"systemMessage": "MonaX Open Workflow context Unverified: " + type(error).__name__}
    if result:
        print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
