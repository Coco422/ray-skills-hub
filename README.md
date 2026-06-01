# Ray Skills Hub

一个极简 GitHub-based Codex skills hub，用来管理 Ray 和团队共享的 skills，也为后续第三方推荐 skills 留出目录和元数据约定。

## Skills

| Skill | Source | Version | Maturity | Recommended | Path |
| --- | --- | --- | --- | --- | --- |
| `manage-skills-hub` | team | `v0.1.0` | stable | yes | `skills/team/manage-skills-hub` |
| `ray-xiaofan-illustrations` | team | `v0.1.0` | beta | yes | `skills/team/ray-xiaofan-illustrations` |

## Quick Start

- 管理这个 hub、查看可用 skills、添加/更新 skill、准备发版：用 `$manage-skills-hub`。
- 生成 Ray / 小反风格中文正文配图：用 `$ray-xiaofan-illustrations`。

## Install

安装时使用 Codex 自带的 `$skill-installer`，从 GitHub repo/path 安装：

```bash
scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/team/manage-skills-hub

scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/team/ray-xiaofan-illustrations
```

也可以固定到 release/tag：

```bash
scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/<repo>/tree/v0.1.0/skills/team/manage-skills-hub

scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/<repo>/tree/v0.1.0/skills/team/ray-xiaofan-illustrations
```

安装后重启 Codex，让新 skill 被重新发现。

## Catalog

`CATALOG.yaml` 是机器可读索引。新增 skill 时保持三件事一致：

- `id` 等于 `SKILL.md` frontmatter 里的 `name`
- `path` 指向真实 skill 目录
- `version` 标注当前 hub 收录版本

## Third Party

第三方 skill 先放入 `third_party/` 或独立实验目录，记录上游 URL、commit、license 和审阅人；确认可维护后再移入 `skills/team/`。
