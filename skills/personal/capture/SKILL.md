---
name: capture
description: |
  一键采集网页或 PDF，自动完成 AI 处理和人工审核流程。
  当用户提供 URL 或 PDF 路径时触发，例如 /capture URL 或 /capture PDF路径。
  适用于："帮我保存这篇文章"、"采集这个链接"、"收藏这个"、粘贴 URL。
  执行后自动进入 review 模式，等待用户确认分类和补充想法。
---

# Capture - 采集、自动处理与审核

一键完成：采集（含图片）→ AI 处理 → 人工审核。

## 输入判断

- **URL**（http/https 开头）→ 网页采集
- **本地文件**（.pdf 结尾）→ PDF 采集

## 流程

### Step 1: 采集内容

使用 Playwright 脚本，支持微信公众号等 JS 渲染页面，自动下载文章图片：

```bash
CAPTURE_SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/capture"
if [ ! -d "$CAPTURE_SKILL_DIR" ]; then
  CAPTURE_SKILL_DIR="$HOME/.claude/skills/capture"
fi
uv run python "$CAPTURE_SKILL_DIR/scripts/fetch_url.py" "https://example.com/article" --wait 3 --images --output "00Inbox/urls/YYYY-MM-DD-简短描述.md"
```

- `--wait 3` — 等待 3 秒确保页面加载完成
- `--images` — 自动下载文章图片到 `{文件名}_images/` 目录
- `-o <path>` — 输出文件路径

### Step 2: 保存到 Inbox

文件：`00Inbox/urls/YYYY-MM-DD-简短描述.md`
图片：`00Inbox/urls/YYYY-MM-DD-简短描述_images/`

Frontmatter：
```yaml
---
url: "原始链接"
captured: YYYY-MM-DD
title: "文章标题"
author: "作者"
images_dir: "YYYY-MM-DD-简短描述_images"
status: pending
---
```

### Step 3: AI 自动处理

读取内容后，生成结构化笔记到 `00AI-Workspace/review/YYYY-MM-DD-简短描述.md`：

```markdown
---
title: "文章标题"
source: "原始链接"
captured: YYYY-MM-DD
ai_processed: true
ai_actions: [extract, summarize]
human_reviewed: false
category: ""
category_suggestion: "tech-reports|practice-logs|insights"
tags: []
---

# 文章标题

## 原文摘要

（200-300字摘要）

## 核心要点

- 要点1
- 要点2
- 要点3

## 技术细节（如有）

（关键命令、配置、实现）

## 文章图片

（从 images_dir 引用，格式：![描述](相对路径)）

## 我的想法

> 此区域需要人工填写。

## AI 处理记录

- 处理时间: YYYY-MM-DD
- AI 参与程度: 生成初稿，待人工 review

## 原始链接

- 来源: [标题](url)
- 原文快照: [[00Inbox/urls/YYYY-MM-DD-简短描述.md]]
- 文章图片: [[00Inbox/urls/YYYY-MM-DD-简短描述_images/]]
```

### Step 4: 自动进入 Review 交互

展示笔记摘要，询问用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 文章标题

📋 AI 摘要：xxx
🏷️ 建议分类：tech-reports | practice-logs | insights
🖼️ 图片：N 张已下载

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请确认：
1. 分类：tech-reports / practice-logs / insights
2. 你的想法：（这几句话也好）
   - 对你有什么价值？
   - 如何应用？
   - 需要深入研究吗？
```

### Step 5: 执行归档

用户确认后：

1. 更新 frontmatter：
   ```yaml
   human_reviewed: true
   reviewed_date: YYYY-MM-DD
   category: "确认的分类"
   tags: [用户标签]
   ```

2. 移动文件到 `03Resources/对应目录/`
   - 笔记移动到 `03Resources/{category}/`
   - 图片目录同步移动

3. **移动废弃文件到回收站**（替代删除）：
   - 移动 `00AI-Workspace/queue/` 中对应任务文件到 `00Trash/`
   - 移动 `00AI-Workspace/review/` 中已归档笔记到 `00Trash/`

### Step 6: 完成反馈

告知归档位置，提示可继续采集下一篇。

## 回收站说明

- 回收站位置：`00Trash/`
- 所有过程产物（queue 任务、review 笔记）归档后移动到回收站
- 不会执行 rm 删除操作
- 人工定期清理 `00Trash/` 中的废弃文件

## 分类建议

- `tech-reports` — 新技术报告、模型发布、开源项目
- `practice-logs` — 部署、踩坑、实验、调优记录
- `insights` — 观点、方法论、收藏资源、提示词

## 关键原则

- 保留原始链接（第一优先级）
- AI 痕迹必须明确标记
- 翻译内容标注"AI 翻译，未经人工审校"
- 引导用户补充"我的想法"，这是知识沉淀的核心
