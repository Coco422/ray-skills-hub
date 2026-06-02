#!/usr/bin/env python3
"""Validate Ray Skills Hub catalog and skill frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "CATALOG.yaml"
README = ROOT / "README.md"
NAME_RE = re.compile(r"^[a-z0-9-]+$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def read_frontmatter(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        fail(f"{skill_dir} is missing SKILL.md")
    match = FRONTMATTER_RE.match(skill_md.read_text(encoding="utf-8"))
    if not match:
        fail(f"{skill_md} is missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        fail(f"{skill_md} frontmatter must be a YAML object")
    return data


def main() -> int:
    catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    if not isinstance(catalog, dict):
        fail("CATALOG.yaml must be a YAML object")
    skills = catalog.get("skills")
    if not isinstance(skills, list) or not skills:
        fail("CATALOG.yaml must contain a non-empty skills list")

    readme = README.read_text(encoding="utf-8")
    seen: set[str] = set()

    for entry in skills:
        if not isinstance(entry, dict):
            fail("Each catalog skill entry must be a YAML object")
        skill_id = entry.get("id")
        path = entry.get("path")
        if not isinstance(skill_id, str) or not NAME_RE.match(skill_id):
            fail(f"Invalid skill id: {skill_id!r}")
        if skill_id in seen:
            fail(f"Duplicate skill id: {skill_id}")
        seen.add(skill_id)

        if not isinstance(path, str):
            fail(f"{skill_id} has invalid path")
        skill_dir = ROOT / path
        if not skill_dir.is_dir():
            fail(f"{skill_id} path does not exist: {path}")

        frontmatter = read_frontmatter(skill_dir)
        if frontmatter.get("name") != skill_id:
            fail(f"{skill_id} name mismatch with SKILL.md")
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            fail(f"{skill_id} is missing description")
        if len(description) > 1024:
            fail(f"{skill_id} description exceeds 1024 characters")
        if skill_id not in readme:
            fail(f"{skill_id} is missing from README.md")

    print(f"Validated {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
