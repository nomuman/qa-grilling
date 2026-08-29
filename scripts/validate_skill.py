#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def validate_frontmatter(errors: list[str]) -> None:
    skill = read("SKILL.md")
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if not match:
        fail(errors, "SKILL.md must start with YAML frontmatter")
        return

    frontmatter = match.group(1)
    required = (
        "name: qa-grilling",
        "description:",
        "license: MIT",
        "disable-model-invocation: true",
    )
    for value in required:
        if value not in frontmatter:
            fail(errors, f"SKILL.md frontmatter is missing: {value}")

    line_count = len(skill.splitlines())
    if line_count > 250:
        fail(errors, f"SKILL.md has {line_count} lines; limit is 250")


def validate_invocation_policy(errors: list[str]) -> None:
    openai_yaml = read("agents/openai.yaml")
    if not re.search(r"(?m)^policy:\n\s+allow_implicit_invocation: false\s*$", openai_yaml):
        fail(errors, "agents/openai.yaml must disable implicit invocation")


def validate_safety_contract(errors: list[str]) -> None:
    skill = read("SKILL.md").lower()
    required = (
        "untrusted data, not instructions",
        "read-only evidence gathering",
        "does not authorize edits",
        "do not reproduce secrets",
        "one-shot",
        "ask exactly one unresolved p0/p1",
    )
    for phrase in required:
        if phrase not in skill:
            fail(errors, f"SKILL.md safety or mode contract is missing: {phrase}")


def validate_links(errors: list[str]) -> set[Path]:
    linked: set[Path] = set()
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target):
                continue
            resolved = (markdown.parent / target).resolve()
            linked.add(resolved)
            if ROOT not in resolved.parents and resolved != ROOT:
                fail(errors, f"link escapes skill directory: {markdown.relative_to(ROOT)} -> {target}")
            elif not resolved.exists():
                fail(errors, f"broken relative link: {markdown.relative_to(ROOT)} -> {target}")

    return linked


def validate_resource_routing(errors: list[str], linked: set[Path]) -> None:
    resource_roots = ("references", "templates", "examples", "evals")
    for directory in resource_roots:
        for resource in (ROOT / directory).rglob("*.md"):
            if resource.resolve() not in linked:
                fail(errors, f"orphaned resource is not linked from another Markdown file: {resource.relative_to(ROOT)}")

    skill = read("SKILL.md")
    if "references/domain-packs.md" in skill:
        fail(errors, "SKILL.md still links the removed monolithic domain pack")
    if "Do not load unrelated domain packs." not in skill:
        fail(errors, "SKILL.md must prohibit loading unrelated domain packs")


def validate_docs(errors: list[str]) -> None:
    english = read("README.md")
    japanese = read("README.ja.md")
    shared_requirements = (
        "v1.0.0",
        "one-shot",
        "disable-model-invocation: true",
        "allow_implicit_invocation: false",
        "CHANGELOG.md",
        "SECURITY.md",
        "scripts/validate_skill.py",
    )
    for value in shared_requirements:
        if value not in english:
            fail(errors, f"README.md is missing release or mode documentation: {value}")
        if value not in japanese:
            fail(errors, f"README.ja.md is missing release or mode documentation: {value}")

    if not read("LICENSE").startswith("MIT License\n"):
        fail(errors, "LICENSE must contain the MIT License text")
    if "## [1.0.0]" not in read("CHANGELOG.md"):
        fail(errors, "CHANGELOG.md must document v1.0.0")
    if "GitHub Security Advisories" not in read("SECURITY.md"):
        fail(errors, "SECURITY.md must provide a private reporting path")


def validate_evals(errors: list[str]) -> None:
    evals = read("evals/README.md")
    ids = sorted(set(re.findall(r"\bE-\d{3}\b", evals)))
    if len(ids) < 10:
        fail(errors, f"behavior evaluation suite has {len(ids)} cases; at least 10 are required")

    required = (
        "prompt injection",
        "one-shot",
        "exactly one",
        "test obligation",
        "cross-host",
        "must-pass",
    )
    for phrase in required:
        if phrase.lower() not in evals.lower():
            fail(errors, f"behavior evaluation rubric is missing: {phrase}")


def validate_workflow(errors: list[str]) -> None:
    workflow = read(".github/workflows/validate.yml")
    if "python3 scripts/validate_skill.py" not in workflow:
        fail(errors, "GitHub Actions must run the structural validator")

    for match in re.findall(r"uses:\s+([^\s]+)", workflow):
        if not re.search(r"@[0-9a-f]{40}$", match):
            fail(errors, f"GitHub Action is not pinned to a full commit SHA: {match}")

    if "permissions:\n  contents: read" not in workflow:
        fail(errors, "GitHub Actions must use read-only contents permission")
    if "timeout-minutes:" not in workflow:
        fail(errors, "GitHub Actions job must define a timeout")


def validate_placeholders(errors: list[str]) -> None:
    placeholder = re.compile(r"\b(?:TODO|TBD|FIXME)\b|\[TODO:", re.IGNORECASE)
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path == Path(__file__).resolve():
            continue
        if path.suffix not in {".md", ".yml", ".yaml"}:
            continue
        if placeholder.search(path.read_text(encoding="utf-8")):
            fail(errors, f"unfinished placeholder found in {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_frontmatter(errors)
    validate_invocation_policy(errors)
    validate_safety_contract(errors)
    linked = validate_links(errors)
    validate_resource_routing(errors, linked)
    validate_docs(errors)
    validate_evals(errors)
    validate_workflow(errors)
    validate_placeholders(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("qa-grilling validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
