---
name: manage-skills-hub
description: Manage and use Ray Skills Hub, a GitHub-based Codex skills catalog. Use when the user asks to browse available team skills, install a skill from this hub, add or update a skill, prepare a release, maintain CATALOG.yaml/README.md, migrate a local skill into the hub, or record third-party/upstream provenance.
---

# Manage Skills Hub

## Overview

Use this skill to operate the Ray Skills Hub with the smallest reliable workflow. The hub is a GitHub repository where each Codex skill remains a normal skill folder, and `CATALOG.yaml` plus `README.md` provide the human and machine index.

## Repository Shape

Expected layout:

```text
README.md
CATALOG.yaml
skills/
  team/<skill-name>/
    SKILL.md
    agents/openai.yaml
    references/
    assets/
third_party/
work/
```

Only `SKILL.md` is required for a skill. Keep optional folders only when they are used.

## Common Tasks

### Browse Skills

Read `CATALOG.yaml` first, then `README.md` if the user needs a human-facing summary. Report skill id, path, version, maturity, owner, and whether it is recommended.

### Install a Skill

Prefer the built-in `$skill-installer` flow with a stable GitHub path:

```bash
scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/team/<skill-name>
```

After installation, tell the user to restart Codex.

### Add or Update a Team Skill

1. Put the skill under `skills/team/<skill-name>/`.
2. Ensure folder name equals `SKILL.md` frontmatter `name`.
3. Keep `SKILL.md` concise; move long material to `references/`.
4. Update `CATALOG.yaml` and the skills table in `README.md`.
5. Validate YAML, paths, and name consistency before finishing.

### Third-Party or Upstream Skills

Do not trust a moving upstream branch as production input. Record upstream repo, commit/ref, license, importer, and review status. Keep third-party material isolated until reviewed.

### Release

For a release, update hub `version`, skill entry versions, and README install examples. If the user asks to push, confirm the Git repo has a remote and use normal git commit/tag/push flow.

## Validation

Run targeted checks:

```bash
ruby -ryaml -e 'cat=YAML.load_file("CATALOG.yaml"); cat["skills"].each { |s| abort("missing #{s["path"]}") unless File.directory?(s["path"]) }'
```

If PyYAML is available, also run:

```bash
python3 /Users/ray/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/team/<skill-name>
```
