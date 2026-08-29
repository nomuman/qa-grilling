from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("qa_grilling_validator", REPOSITORY / "scripts" / "validate_skill.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "skill"
        shutil.copytree(REPOSITORY, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.root = self.root.resolve()
        self.original_root = VALIDATOR.ROOT
        VALIDATOR.ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.ROOT = self.original_root
        self.temporary.cleanup()

    def run_validator(self) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = VALIDATOR.main()
        return result, output.getvalue()

    def replace(self, relative: str, before: str, after: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(before, text)
        path.write_text(text.replace(before, after, 1), encoding="utf-8")

    def test_valid_repository_passes(self) -> None:
        result, output = self.run_validator()
        self.assertEqual(0, result, output)

    def test_implicit_invocation_is_rejected(self) -> None:
        self.replace("agents/openai.yaml", "allow_implicit_invocation: false", "allow_implicit_invocation: true")
        result, output = self.run_validator()
        self.assertEqual(1, result)
        self.assertIn("disable implicit invocation", output)

    def test_broken_link_is_rejected(self) -> None:
        (self.root / "references" / "domains" / "agent-skills.md").unlink()
        result, output = self.run_validator()
        self.assertEqual(1, result)
        self.assertIn("broken relative link", output)

    def test_orphaned_reference_is_rejected(self) -> None:
        (self.root / "references" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
        result, output = self.run_validator()
        self.assertEqual(1, result)
        self.assertIn("orphaned resource", output)

    def test_unpinned_action_is_rejected(self) -> None:
        workflow = self.root / ".github" / "workflows" / "validate.yml"
        text = workflow.read_text(encoding="utf-8")
        text = text.replace("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", "actions/checkout@v7")
        workflow.write_text(text, encoding="utf-8")
        result, output = self.run_validator()
        self.assertEqual(1, result)
        self.assertIn("not pinned to a full commit SHA", output)

    def test_private_case_study_path_is_rejected(self) -> None:
        path = self.root / "case-studies" / "self-review-v1.0.0.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n/Users/example/private\n", encoding="utf-8")
        result, output = self.run_validator()
        self.assertEqual(1, result)
        self.assertIn("public case study contains private", output)


if __name__ == "__main__":
    unittest.main()
