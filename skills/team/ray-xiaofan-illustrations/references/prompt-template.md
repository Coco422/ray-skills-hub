# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse but readable red/orange/blue handwritten Chinese or English annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Reference discipline before generation:
Visually inspect the provided 小反 v4 action reference sheet and 2-3 example illustrations before writing this prompt. Follow the visual identity from the references more strongly than any generic character interpretation.

Batch consistency rule:
If generating multiple images, treat this image as a fresh standalone generation. Do not continue from the previous generated image. Re-anchor to the 小反 v4 reference sheet for every image. If image references are supported, use the 小反 v4 reference sheet for every generation and never use a previous generated image as the identity reference.

Character identity lock:
Use the same recurring character identity as the 小反 v4 reference sheet. 小反 is a white hollow unclosed vertical oval/capsule body with a black hand-drawn outline. The outline has exactly one opening near the top or upper side, and the open contour itself ends as a fixed black arrow tip. The arrow is part of the body outline, not a separate icon, not a floating mark, not headwear, not a prop. Keep exactly two tiny black dot eyes, thin black stick arms/legs, blank serious deadpan expression, and exactly one short vivid red diagonal slash inside the body. Do not close the oval. Do not add a separate arrow. Do not move the arrow to the feet, lower body, ground, tail, tools, labels, or background. Do not turn the red slash into an arrow. Do not make the character cute, mascot-like, black-filled, or a generic white blob.

Recurring IP character required:
小反, a small white hollow unclosed vertical oval/capsule recurring worker character with a bold irregular black hand-drawn outline, two tiny black dot eyes, thin stick arms/legs, and a blank serious expression. The body outline has one opening near the top or upper side; the open contour ends as a fixed black arrow tip. This arrow is part of the body contour, not a separate icon, not a floating mark, not headwear, not a prop. Never move the arrow to the feet, lower body, ground, tail, tools, labels, or background. The body contains exactly one short vivid red diagonal stroke; the red stroke is not an arrow. 小反 must perform the core conceptual action, not decorate the scene. Hats, clothes, and tools may appear as temporary role props, but the white unclosed hollow oval body, internal red slash, and contour-opening arrow must remain recognizable. Make 小反 serious, deadpan, and slightly bizarre, not cute.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：小反在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Short handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Use short readable Chinese or English labels directly where useful. If drawing speech bubbles, captions, buttons, callout boxes, or label containers, put short text inside them. Do not leave empty speech bubbles, blank captions, blank buttons, or empty explanation boxes.

Color use:
Black for main line art, 小反 outline, eyes, limbs, and the fixed contour-opening arrow. Orange for main flow/path/arrows. Red for 小反's internal diagonal stroke and sparse key warnings/problems/results. Blue only for secondary notes or feedback/system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short readable handwritten Chinese or English labels. Do not create blank text containers. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

## 连续多张生成提示

连续生成时，不要在第 2 张以后写“保持上一张的小反形象”或“same character as before”。这会让模型继承上一张里的错误和漂移。每张都要重新粘贴 `Character identity lock`，并重新绑定小反 v4 参考表。

如果某一张的小反已经漂移，不要用那张图继续编辑下一张；回到 v4 参考表和本模板重新生成。

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强怪诞感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make 小反 more central to the conceptual action. 小反 should be doing the strange work that explains the idea, not standing beside the diagram. Preserve 小反 as a white hollow unclosed vertical oval/capsule character with one body-contour opening that ends as a fixed black arrow tip, plus one internal red diagonal stroke. The black arrow must remain part of the contour opening; do not draw it as a separate icon or move it to the feet, lower body, ground, tools, labels, or background. Keep it clean, sparse, hand-drawn, and not cute. Use short readable Chinese or English labels where useful; do not create empty speech bubbles, blank captions, or blank explanation boxes.
```
