"""Exercise independent distribution, domain resources and example behavior."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
import zipfile

sys.dont_write_bytecode = True
PLUGIN = Path(__file__).resolve().parents[1]
PACKAGE = PLUGIN.parents[1]
sys.path.insert(0, str(PACKAGE / "tools"))
sys.path.insert(0, str(PLUGIN / "scripts"))
import check_distribution
import project


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.base = Path(os.environ.get("MONAX_WORKFLOW_TEST_TMP") or tempfile.gettempdir()).resolve()
        self.area = self.base / ("monax-distribution-test-" + uuid.uuid4().hex)
        self.area.mkdir()

    def tearDown(self):
        self.assertEqual(self.area.resolve().parent, self.base)
        self.assertTrue(self.area.name.startswith("monax-distribution-test-"))
        shutil.rmtree(self.area)

    def copy_package(self):
        dest = self.area / "portable package"
        dest.mkdir()
        for name in check_distribution.inventory(PACKAGE):
            target = dest / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((PACKAGE / name).read_bytes())
        return dest

    def test_inventory_and_links(self):
        result = check_distribution.check(PACKAGE)
        self.assertTrue(result["success"], result["issues"])

    def test_templates_travel_with_project_and_drift_is_visible(self):
        root = self.area / "project"
        root.mkdir()
        self.assertEqual(project.initialize(root, True)["status"], "Created")
        for name in project.TEMPLATE_NAMES:
            self.assertTrue((root / ".monax-workflow/templates" / name).is_file())
        template = root / ".monax-workflow/templates/video-brief.md"
        template.write_text("Changed template", encoding="utf-8")
        result = project.check(root)
        self.assertEqual(result["status"], "Blocked")
        self.assertTrue(any("Template drift" in x for x in result["issues"]))

    def test_invalid_owner_type_returns_blocked(self):
        root = self.area / "project"
        root.mkdir()
        project.initialize(root, True)
        path = root / "PROJECT_CONTEXT/workflow_activation_profile.json"
        profile = json.loads(path.read_text(encoding="utf-8"))
        profile["project_owners"]["identity"] = ["invalid"]
        path.write_bytes(project.json_bytes(profile))
        self.assertEqual(project.check(root)["status"], "Blocked")

    def test_declared_rule_owners_and_versions(self):
        catalog = json.loads((PLUGIN / "rules/catalog.json").read_text(encoding="utf-8"))
        for group in ("rules", "conditional_rules"):
            for name in catalog[group].values():
                self.assertIn(name, project.RULE_NAMES)
                self.assertTrue((PLUGIN / "rules" / name).is_file())
        for manifest in ("plugin.json", ".codex-plugin/plugin.json"):
            value = json.loads((PLUGIN / manifest).read_text(encoding="utf-8"))
            self.assertEqual(value["version"], project.VERSION)

    def test_game_example_calls_config_and_rejects_duplicate(self):
        spec = importlib.util.spec_from_file_location("fictional_reward_demo", PACKAGE / "examples/game/reward_demo.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        service = module.RewardService(module.RewardConfig(tokens_per_level=7))
        button = module.RewardButton(service)
        self.assertEqual(button.on_click("one", False), 0)
        self.assertEqual(button.on_click("one", True), 7)
        self.assertEqual(button.on_click("one", True), 0)
        self.assertEqual(button.on_click("two", True), 7)
        self.assertEqual(service.balance, 14)

    def test_unknown_file_and_privacy_pattern_fail_closed(self):
        copied = self.copy_package()
        (copied / "unexpected.txt").write_text("unreviewed", encoding="utf-8")
        self.assertFalse(check_distribution.check(copied)["success"])
        (copied / "unexpected.txt").unlink()
        # Construct an artificial path instead of embedding a real machine path.
        (copied / "README.md").write_text("Z" + ":/" + "PrivateUser/work", encoding="utf-8")
        result = check_distribution.check(copied)
        self.assertTrue(any("absolute drive path" in item for item in result["issues"]))

    def test_release_is_allowlisted_and_refuses_overwrite(self):
        copied = self.copy_package()
        ignored = copied / "demo-project"
        ignored.mkdir()
        (ignored / "private.txt").write_text("MUST_NOT_SHIP", encoding="utf-8")
        out = self.area / "release"
        command = [sys.executable, "-B", str(copied / "tools/package_release.py"), "--output", str(out)]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        paths = json.loads(result.stdout)
        manifest = json.loads(Path(paths["manifest"]).read_text(encoding="utf-8"))
        archive = Path(paths["archive"])
        before = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertEqual(before, manifest["archive_sha256"])
        with zipfile.ZipFile(archive) as bundle:
            names = bundle.namelist()
            self.assertEqual(len(names), len(check_distribution.inventory(copied)))
            self.assertFalse(any("private.txt" in n or "/.git/" in n for n in names))
            for name, expected in manifest["files"].items():
                self.assertEqual(hashlib.sha256(bundle.read(archive.stem + "/" + name)).hexdigest(), expected)
        again = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(again.returncode, 0)
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
