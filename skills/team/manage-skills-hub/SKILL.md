---
name: manage-skills-hub
description: Manage and use Ray Skills Hub, a GitHub-based skills catalog (compatible with Claude Code and Codex). Use when the user asks to browse available team skills, install a skill from this hub, add or update a skill, prepare a release, maintain CATALOG.yaml/README.md, migrate a local skill into the hub, or record third-party/upstream provenance.
---

# Manage Skills Hub v0.4.1

## Overview

Use this skill to operate the Ray Skills Hub with the smallest reliable workflow. The hub is a GitHub repository where each skill remains a normal skill folder, and `CATALOG.yaml` plus `README.md` provide the human and machine index.

## Repository Shape

Expected layout:

```text
README.md
CATALOG.yaml
skills/
  team/<skill-name>/
    SKILL.md
    references/
    assets/
  personal/<skill-name>/
    SKILL.md
third_party/
```

Only `SKILL.md` is required for a skill. Keep optional folders only when they are used.

## Common Tasks

### Browse Skills

Read `CATALOG.yaml` first, then `README.md` if the user needs a human-facing summary. Report skill id, path, version, maturity, owner, and whether it is recommended.

### Install a Skill

#### Claude Code

Copy the skill folder to `~/.claude/skills/<skill-name>/` (global) or `<project>/.claude/skills/<skill-name>/` (project-scoped):

```bash
# Clone the hub repo
gh repo clone Coco422/ray-skills-hub /tmp/ray-skills-hub

# Copy a team or personal skill
cp -r /tmp/ray-skills-hub/skills/team/<skill-name> ~/.claude/skills/
```

Or use the install script (if available):

```bash
python3 scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/team/<skill-name>
```

After installation, restart the Claude Code session (or `/skills` to reload).

#### Codex

Prefer `$skill-installer` for first-time installs:

```bash
scripts/install-skill-from-github.py \
  --repo Coco422/ray-skills-hub \
  --path skills/team/<skill-name>
```

For updating an already-installed skill, compare against a fresh clone of `Coco422/ray-skills-hub`, back up the installed directory, replace it with the matching skill folder, then restart Codex.

### Audit Local Skills

When the user asks to clean, dedupe, or align local skills:

1. Inventory relevant roots: `~/.codex/skills`, `~/.cc-switch/skills`, and `~/.claude/skills` when present.
2. Compare folder names, `SKILL.md` frontmatter names, file hashes, and hub catalog entries.
3. Treat identical copies across roots as intentional unless the user confirms removal; different tools may load different roots.
4. Treat drifted hub skills as update candidates. Back up before replacing any installed directory.
5. Treat `.system` skills and plugin cache skills as managed by Codex/plugins; do not edit them from this hub workflow.
6. Do not delete or archive a local skill directory unless the user confirms the exact candidate list.
7. Validate changed skills with `quick_validate.py` and re-run hub catalog validation when the hub repo changes.

### Add or Update a Team Skill

1. Put team skills under `skills/team/<skill-name>/`; put Ray personal skills under `skills/personal/<skill-name>/`.
2. Ensure folder name equals `SKILL.md` frontmatter `name`.
3. Keep `SKILL.md` concise; move long material to `references/`.
4. Update `CATALOG.yaml` and the skills table in `README.md`.
5. Validate YAML, paths, and name consistency before finishing.

### Collaborator PR Flow

For external collaborators, use this exact flow:

1. Fork `Coco422/ray-skills-hub`.
2. Create a branch in the fork, such as `feat/add-<skill-name>` or `fix/update-<skill-name>`.
3. Add or update files only under the relevant skill directory plus `CATALOG.yaml` and `README.md`. Team skills go under `skills/team/`; Ray personal skills go under `skills/personal/`.
4. Keep historical versions in Git history; the repository tree should contain only the latest accepted version of each skill.
5. Push the branch to the fork and open a PR against `Coco422/ray-skills-hub:main`.
6. Ask the PR author to include purpose, trigger examples, source/license, assets included, and validation run.

When Ray asks an agent to process a PR, review the diff, verify the catalog and skill frontmatter, check assets/provenance, then either request changes or merge.

### Branch Rules

The remote repository should protect `main` with a GitHub ruleset:

- Require pull requests before merging.
- Require the `validate-catalog` status check.
- Block direct pushes for collaborators.
- Allow Ray/repo admins to bypass only for bootstrap or emergency maintenance.

### Third-Party or Upstream Skills

Do not trust a moving upstream branch as production input. Record upstream repo, commit/ref, license, importer, and review status. Keep third-party material isolated until reviewed.

### Release

For a release, update hub `version`, skill entry versions, and README install examples. Do not keep draft folders in the repository. If the user asks to push, confirm the Git repo has a remote and use normal git commit/tag/push flow.

## Validation

Run targeted checks:

```bash
python3 scripts/validate_catalog.py
```
