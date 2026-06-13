# Ray Skills Hub

一个极简 GitHub-based skills hub，用来管理 Ray 和团队共享的 skills（兼容 Claude Code 和 Codex），也为后续第三方推荐 skills 留出目录和元数据约定。

## Skills

### Team

| Skill | Source | Version | Maturity | Recommended | Path |
| --- | --- | --- | --- | --- | --- |
| `hv-analysis` | team | `v0.2.0` | stable | yes | `skills/team/hv-analysis` |
| `manage-skills-hub` | team | `v0.4.0` | stable | yes | `skills/team/manage-skills-hub` |
| `neat-freak` | team | `v0.2.0` | stable | yes | `skills/team/neat-freak` |
| `project-daily-summary` | team | `v0.2.0` | stable | yes | `skills/team/project-daily-summary` |
| `ray-xiaofan-illustrations` | team | `v0.4.0` | beta | yes | `skills/team/ray-xiaofan-illustrations` |

### Personal

| Skill | Source | Version | Maturity | Recommended | Path |
| --- | --- | --- | --- | --- | --- |
| `ray-writer` | personal | `v0.2.0` | stable | yes | `skills/personal/ray-writer` |
| `capture` | personal | `v0.1.0` | beta | yes | `skills/personal/capture` |
| `codex-mac-patch` | personal | `v0.1.0` | beta | yes | `skills/personal/codex-mac-patch` |

## Quick Start

- 管理这个 hub、查看可用 skills、添加/更新 skill、准备发版：用 `$manage-skills-hub`。
- 生成 Ray / 小反风格中文正文配图：用 `$ray-xiaofan-illustrations`。
- 做项目级日报：用 `$project-daily-summary`。
- 做会话收尾知识整理：用 `$neat-freak`。
- 做横纵分析法深度研究：用 `$hv-analysis`。
- 写 Ray 博客文章：用 `$ray-writer`。
- 一键采集网页或 PDF：用 `$capture`。
- Codex Desktop macOS 解限补丁：用 `$codex-mac-patch`。

## Website

这个仓库内置一个 Astro 静态站，用 `CATALOG.yaml` 和各个 `SKILL.md` 生成可视化 skills hub：

- 首页展示 skill 卡片、搜索、source/tag 筛选
- 每个 skill 详情页展示完整 `SKILL.md`
- 卡片和详情页都支持一键复制 raw `SKILL.md` 链接与安装命令

本地开发：

```bash
npm install
npm run dev
```

构建与校验：

```bash
npm run validate
npm run build
npm audit --omit=dev
```

GitHub Pages 部署由 `.github/workflows/pages.yml` 完成。默认自定义域名是：

```text
https://skills.521980.xyz/
```

如果改接其他自定义域名，把 GitHub Pages 的 custom domain 配好后，在 Pages workflow 里设置：

```yaml
env:
  SITE_URL: https://你的域名
  SITE_BASE: /
```

## Install

### Claude Code

```bash
# 克隆 hub 仓库
gh repo clone Coco422/ray-skills-hub /tmp/ray-skills-hub

# 拷贝到全局 skills 目录
cp -r /tmp/ray-skills-hub/skills/team/manage-skills-hub ~/.claude/skills/
cp -r /tmp/ray-skills-hub/skills/personal/ray-writer ~/.claude/skills/
cp -r /tmp/ray-skills-hub/skills/personal/capture ~/.claude/skills/

# 或拷贝到项目级 skills 目录
cp -r /tmp/ray-skills-hub/skills/personal/capture <your-project>/.claude/skills/
```

安装后重启 Claude Code 会话，或执行 `/skills` 重新加载。

### Codex

使用 `$skill-installer` 从 GitHub repo/path 安装：

```bash
scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/team/manage-skills-hub

scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/team/ray-xiaofan-illustrations

scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/personal/ray-writer

scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/personal/capture

scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/personal/codex-mac-patch
```

也可以固定到 release/tag：

```bash
scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/<repo>/tree/v0.4.0/skills/team/manage-skills-hub
```

安装后重启 Codex，让新 skill 被重新发现。

## Catalog

`CATALOG.yaml` 是机器可读索引。新增 skill 时保持三件事一致：

- `id` 等于 `SKILL.md` frontmatter 里的 `name`
- `path` 指向真实 skill 目录
- `version` 标注当前 hub 收录版本

## Collaborate

协作者新增或更新 skill 时走 PR，不直接改主仓库：

1. Fork `Coco422/ray-skills-hub` 到自己的 GitHub 账号。
2. 从 fork 新建分支，例如 `feat/add-my-skill` 或 `fix/update-skill-name`。
3. 把团队 skill 放到 `skills/team/<skill-name>/`；Ray 个人 skill 放到 `skills/personal/<skill-name>/`。目录名必须等于 `SKILL.md` frontmatter 里的 `name`。
4. 更新 `CATALOG.yaml` 和 README 的 Skills 表。
5. 本地验证 YAML、路径、frontmatter name 一致。
6. Push 到自己的 fork，并向 `Coco422/ray-skills-hub:main` 发 PR。
7. 在 PR 描述里写清 skill 用途、触发场景、来源/授权、是否需要 assets，以及建议安装路径。

Ray 会让 agent 处理 PR review、校验、整理和合并。

### Branch Rules

`main` 会配置 GitHub ruleset：协作者不能直接 push，必须开 PR，并且 `validate-catalog` 检查通过后才能合并。Ray / repo admin 仍可在 bootstrap 或紧急维护时绕过规则；正常维护也优先走 PR。

## Third Party

第三方 skill 先放入 `third_party/` 或独立实验目录，记录上游 URL、commit、license 和审阅人；确认可维护后再移入 `skills/team/`。
