---
name: ray-xiaofan-illustrations
description: 生成 Ray / 小反风格的中文正文配图。用于用户要求为中文文章、帖子、博客、Notion 文档、工作流文档、方法论、流程、结构、状态、隐喻或观点生成“怪诞”“小反”“小黑旧称”“手绘”“正文配图”“文章插图”“配图建议”“shot list”“去标题/改图”等任务；也用于 Ray 博客配图的临时目录暂存、排版确认、图床上传前交付清单和最终链接替换工作流。默认使用小反 IP：白色未闭合空心椭圆身体、开口处固定黑色箭头、体内红斜线、纯白手绘、少量红橙蓝批注。
---

# Ray 小反怪诞正文配图（v0.4.0）

## 核心定位

为中文文章设计和生成 16:9 横版正文配图。目标不是做商业插画、PPT 信息图或可爱卡通，而是把文章里的关键判断、流程、结构、状态或隐喻，变成一张清爽、怪诞、有创意、可读但不说明书的手绘解释图。

默认视觉 IP 是“小反”：白色未闭合空心椭圆身体，黑色手绘外轮廓，轮廓在头顶或头侧上方留一个开口，开口处直接长出一个固定黑色箭头；两个黑点眼、细手脚、空表情；身体内部固定一条红色斜线。箭头不是可移动装饰物，而是小反身体轮廓的一部分。小反必须参与画面的核心动作，不能只是站在旁边当装饰。

帽子、衣服、道具可以作为场景扮演层出现，但不能改变小反的本体特征：白色未闭合空心椭圆身体、开口处固定黑色箭头、体内红斜线。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/style-dna.md`：风格 DNA、颜色、文字、禁忌。
- `references/xiaofan-ip.md`：小反 IP 的形象、性格、动作库和禁忌。
- `references/xiaohei-ip.md`：旧称兼容说明，除非处理历史素材，不要按旧小黑形象生成。
- `references/composition-patterns.md`：结构类型、原创隐喻方法和反复刻规则。
- `references/prompt-template.md`：单张生图提示词模板。
- `references/qa-checklist.md`：生成后检查和迭代规则。
- `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v4.png`：小反 v0.2.0 动作参考表，默认优先用于角色识别、动作密度和批注尺度校准。
- `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v3.png`：小反 v0.1.0 旧版动作参考，只作历史对照，不要覆盖，不要拼进最终图。
- `assets/examples/*.png`：v0.2.0 风格校准示例资产，用来判断留白、角色参与方式、隐喻浓度和批注密度；只能校准方向，不能照抄构图。

v0.4.0 起，生成小反之前必须先视觉检查 `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v4.png` 和至少 2-3 张 `assets/examples/*.png`。不要只靠文本描述指挥角色形象；先把小反的未闭合空心椭圆、开口箭头、红斜线和动作比例看准，再写 prompt。

## 多张连续生成的角色锁定

连续生成多张时，最容易发生角色漂移：第一张还是小反，后面逐渐变成普通白色小人、闭合胶囊、独立箭头头饰、红色箭头或可爱吉祥物。批量生成必须使用角色锁定流程。

### 批量生成规则

1. 把每张图当作独立单张生成，不要让模型“延续上一张图的风格”。
2. 每张图生成前都重新查看 `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v4.png`，并把它当作唯一角色身份基准。
3. 如果当前工具支持参考图或 image-to-image，每一张都必须附上 `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v4.png` 作为角色参考；不要用上一张生成图当角色参考。
4. 如果当前工具只支持纯文本 prompt，每一张 prompt 都必须完整重复“角色锁定短块”，不要用“同上 / 保持一致 / 继续小反风格”等省略写法。
5. 场景、道具、动作可以变化；小反本体不能变化。衣服、帽子和遮挡物要少用，且不能遮住开口箭头、红斜线和空心身体。
6. 一张图里如果出现多个小反，先保证主小反标准；副小反尽量减少，避免模型把角色群像平均成别的形象。
7. 任何一张开始漂移，后续不要沿用它。回到 v4 参考表重新生成这一张。

### 角色锁定短块

连续生成时，每张 prompt 都必须逐字或近似包含：

```text
Character identity lock:
Use the same recurring character identity as the 小反 v4 reference sheet. 小反 is a white hollow unclosed vertical oval/capsule body with a black hand-drawn outline. The outline has exactly one opening near the top or upper side, and the open contour itself ends as a fixed black arrow tip. The arrow is part of the body outline, not a separate icon, not a floating mark, not headwear, not a prop. Keep exactly two tiny black dot eyes, thin black stick arms/legs, blank serious deadpan expression, and exactly one short vivid red diagonal slash inside the body. Do not close the oval. Do not add a separate arrow. Do not move the arrow to the feet, lower body, ground, tail, tools, labels, or background. Do not turn the red slash into an arrow. Do not make the character cute, mascot-like, black-filled, or a generic white blob.
```

## 工作流

### 1. 消化正文

先读用户给的正文、链接、Notion 页面、Markdown 文件或截图内容。提炼：

- 核心观点是什么
- 哪些段落承担认知转折
- 哪些内容适合用图解释
- 哪些地方只适合文字，不需要图

不要平均配图。优先选择“认知锚点”，例如：核心判断、两个断点、输入输出闭环、分流、前后对比、一鱼多吃、承接路径、常见坑、角色状态变化。

### 2. 先出配图策略

如果用户只是说“分析怎么配图 / 思考哪些地方需要配图”，先给 shot list。每张图写清楚：

- 放在哪个段落后
- 图的主题
- 核心意思
- 结构类型
- 小反在图里做什么
- 建议元素
- 建议中文或英文短标注词

默认 4-8 张。文章很短时 1-3 张；长文也不要轻易超过 9 张。够用就好，避免把正文做成画册。

### 3. 单张生成

如果用户明确要求“生成 / 输出 / 做图 / 帮我生成”，不要停下来等确认；用内置 `image_gen` 每张单独生成。不要把多张图拼在一张里。

生成前强制做视觉校准：

1. 查看 `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v4.png`。
2. 查看至少 2-3 张 `assets/examples/*.png`，优先选择与当前主题结构接近的样张。
3. 在 prompt 中明确要求：小反是未闭合空心椭圆，箭头是开口处的轮廓末端，不是头顶独立图标，也不能移动到脚边、身体下方、地面或道具上。

每张图只讲一个核心结构。提示词必须包含：

- 16:9 横版中文正文配图
- 纯白背景
- 黑色手绘线稿
- 少量红色/橙色/蓝色中文或英文手写批注
- 大量留白
- 小反作为核心动作主体
- 小反保持白色未闭合空心椭圆身体、开口处固定黑色箭头、体内红斜线；不要把箭头画成独立符号，也不要画到脚边、身体下侧、地面或道具上
- 可以在画面中写简短中文或英文标注、气泡词、标签和按钮文案；生图模型能处理文字时，不要强制留空说明框
- 禁止 PPT、商业插画、幼稚可爱、复杂架构、左上角类型标题

不要复刻过往案例。案例只提供风格密度和角色参与方式，不能直接复用“传送带断点 / 小黑拉线 / 素材鱼 / 盖章工具箱 / 常见坑路径”等已有构图，除非用户明确要求复刻某张图。每次都要从当前文章重新发明一个奇怪但成立的隐喻。

### 4. 检查与迭代

生成后检查 `references/qa-checklist.md`。如果出现以下问题，优先重生成或局部编辑：

- 小反只是装饰
- 画面太满
- 太像流程图/PPT
- 文字太多或错字严重
- 需要文字的位置被空白气泡或空白说明框占位
- 左上角出现“常见坑/流程图/系统架构图”等标题
- 画风太可爱、幼稚、死板
- 背景不是干净白底

### 5. 保存交付

如果当前任务就是维护本 skill 自身资产，可直接写入：

```text
assets/xiaofan/
assets/examples/
```

其中：

- `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v4.png` 是 v0.2.0 默认动作校准表。
- `assets/examples/` 是新版风格校准样张集合，文件名固定时可以替换内容，但替换前要确认仍满足 v0.2.0 风格约束。
- `assets/xiaofan/xiaofan-white-redline-head-arrow-sheet-v3.png` 保留为旧基线，不删除，不覆盖。

如果是 Ray 的博客文章，默认不要把生成图直接当成最终站内资产写进正文。先进入临时暂存流程：

```text
static/_draft-images/<article-slug>/
```

仅当不需要 Hugo 本地预览时，可以用系统临时目录：

```text
${TMPDIR}/ray-blog-illustrations/<article-slug>/
```

Ray 确认排版和选图后，再批量上传到图床，最后把 Markdown 里的临时链接替换为 `https://imgbed.anluoying.com/...`。

暂存阶段按顺序命名：

```text
01-topic-name.png
02-topic-name.png
```

交付时给一个简短 upload manifest：

- 本地临时路径
- 建议 alt 文案
- 建议插入段落
- 是否推荐保留

如果用户明确要求使用仓库内正式资产，或当前不是 Ray 博客工作流，才把最终图复制到：

```text
assets/<article-slug>-illustrations/
```

按顺序命名：

```text
01-topic-name.png
02-topic-name.png
```

保留原始生成文件，不要覆盖已有资产，除非用户明确要求替换。

## 输出口径

生成前的策略输出要短而准。生成后的交付要包含：

- 生成了几张
- 每张图的用途
- 临时保存路径或正式保存路径
- 等待图床上传替换的清单
- 哪些图最稳，哪些图是可选

不要长篇解释风格理论；让图自己说话。
