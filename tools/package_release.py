"""Build a deterministic allowlisted ZIP and hash manifest; never upload or overwrite."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode = True
from check_distribution import ROOT, check, inventory, safe_file


def build(output):
    result = check(ROOT)
    if not result["success"]:
        raise ValueError("Distribution checks failed: " + "; ".join(result["issues"]))
    plugin = json.loads((ROOT / "plugins/monax-open-workflow/plugin.json").read_text(encoding="utf-8"))
    stem = "monax-open-workflow-" + plugin["version"]
    output = Path(output).absolute()
    for path in (output, *output.parents):
        if path.is_symlink() or (path.exists() and getattr(path.lstat(), "st_file_attributes", 0) & 1024):
            raise ValueError("Linked output path is unsupported")
    archive = output / (stem + ".zip")
    manifest = output / (stem + ".manifest.json")
    if archive.exists() or manifest.exists():
        raise ValueError("Release already exists; choose another output directory or version")
    # Load payload before archive creation; hashes cover the exact exported bytes.
    payload = {name: safe_file(ROOT, name).read_bytes() for name in sorted(inventory(ROOT))}
    output.mkdir(parents=True, exist_ok=True)
    hashes = {}
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in payload.items():
            info = zipfile.ZipInfo(stem + "/" + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
            hashes[name] = hashlib.sha256(data).hexdigest()
    with manifest.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump({"schema_version": 1, "version": plugin["version"], "archive": archive.name,
                   "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                   "files": hashes}, stream, ensure_ascii=True, indent=2)
        stream.write("\n")
    return {"archive": str(archive), "manifest": str(manifest), "file_count": len(payload)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.output), ensure_ascii=True, indent=2))
    except (OSError, ValueError) as error:
        print(json.dumps({"error": str(error), "note": "Review any partial output; no automatic deletion."}, ensure_ascii=True))
        raise SystemExit(1)
