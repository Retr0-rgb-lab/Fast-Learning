---
tags: [WD, CSS选择器与层叠, 引入方式, 外链, 内联样式]
course: COMP3421
lecture: L04
---

# CSS引入方式 · Three Ways to Add CSS

> **一句话**：行内 `style` 之所以是"最后手段"，是因为它带来**重复、改一处要改多处、样式和内容混在一起、无法复用、无法覆盖**五个问题——解法是同一条声明的三个住处，**外链是默认，内嵌是例外，行内是最后手段**。

课件原文见 [Lecture_04_CSS.pptx](<../../raw/Lecture_04_CSS.pptx>)。本篇覆盖 Week 4 的 "Why CSS?" 一节：行内样式的五个问题、CSS 之前 `<font>` 与间隔 gif 的土办法、9×4=36 的算术，以及三种引入方式。

## 一、行内样式的五个问题

| 问题 | 含义 |
|---|---|
| **Repeat everything** | 同一条样式被抄到每一个元素上 |
| **Change everywhere** | 改一处样式，就得改每一个标签 |
| **Style mixed with content** | HTML 里塞满样式噪音，难以阅读 |
| **No reuse** | 一条样式无法在多个元素、多个页面之间共享 |
| **Hard to override** | **只有 `!important` 能覆盖行内样式** |

最后一条是硬伤：行内样式贴着元素本身，比任何选择器都靠近元素，常规规则压不住它。这条在本篇讲不出解法，因为解法在 [[层叠与优先级]]。

## 二、一次真实的代价

课件给的那条标题样式有**九条声明**：

```html
<h1 style="color:#1E4FA8; font-family:Arial,sans-serif;
font-size:28px; font-weight:700;
line-height:1.25; margin:0 0 12px;
padding:8px 16px; background:#EEF3FB;
border-left:4px solid #1E4FA8;">
Courses
</h1>
```

同样的属性要挂在四个标题上：

```html
<h1 style="…">    Courses
<h1 style="…">    Research
<h1 style="…">    Teaching
<h1 style="…">    Contact
```

课件的算式：**9 × 4 headings = 36 copies——改一次颜色，要改四处。**

这就是"change everywhere"的实体：一行颜色从 `#1E4FA8` 换成 `#1A3F8C`，36 份副本里漏掉任何一份，页面上就多出一个颜色不一样的标题。

## 三、CSS 之前的土办法

课件留了一个"每种效果配一个表现标签"的年代方案：

```html
<font color="blue"><b>Courses</b></font>   <br><br>   <img src="spacer.gif" width="1">
```

看这三样东西分别在干什么：`<font>` 负责**颜色**（甚至不只颜色）、`<b>` 负责**粗体**、最后那个 `spacer.gif` 是一张 1 像素宽的透明图，专门用来**撑出空隙**。

一种效果一个标签，一种间距一张图。这个例子要说明的不是怀旧，而是**"样式是内容"这个困境的极端形态**——要让两段文字隔开一点距离，唯一的办法是往文档里塞一张图片。

## 四、转机：选择器

课件给的四步过渡，是从"贴着元素"到"点得着元素"：

| 步骤 | 动作 |
|---|---|
| Pull the style out | 把声明搬进 `<style>` 块或 `.css` 文件 |
| Select the elements | 用**选择器**说明这条规则管哪些元素 |
| Write once, reuse | **一条规则**给每一个匹配的元素上样式 |
| class is the hook | `class="note"` 配 `.note { … }`——**这就是可复用的那一对** |

```css
h1.title { color: blue; }
```

四条规则，八个字符，替掉上面那 36 份副本。选择器怎么分类，见 [[规则结构与选择器分类]]；`class` 这个钩子本身的性质，见 [[简单选择器]]。

## 五、**一条声明，三个住处**

课件强调这三种写法的**声明部分完全一样**，差别只在"金线"——声明放在哪儿。

### 1. External：独立 `.css` 文件，用 `<link>` 拉进来

```html
<!-- index.html -->
<link rel="stylesheet"
      href="style.css">
```
```css
/* style.css */
h1 { color: #1E4FA8; }
```

- **作用范围**：所有 `<link>` 了它的页面
- **定位**：**默认做法**——写一次，到处复用

### 2. Internal：页面 `<head>` 里的 `<style>` 块

```html
<head>
  <style>
    h1 { color: #1E4FA8; }
  </style>
</head>
```

- **作用范围**：只有这一个页面
- **定位**：单页够用，但**跨页面无法复用**

### 3. Inline：每个元素身上的 `style` 属性

```html
<h1 style="color: #1E4FA8;">
  Hello
</h1>
<p style="color: #1E4FA8;">
  And here too
</p>
```

- **作用范围**：一个元素
- **定位**：**最后手段**——重复，且难覆盖

### 三者对照

| 方式 | 住址 | 作用范围 | 复用 | 定位 |
|---|---|---|---|---|
| External | `style.css` | 所有链接它的页面 | 最好 | **默认** |
| Internal | `<head>` 里的 `<style>` | 这一个页面 | 不能跨页 | 单页例外 |
| Inline | 元素上的 `style` | 一个元素 | 不能 | **最后手段** |

> [!important] 这张表就是层叠的第一条规则
> 越"靠近元素"越强：inline 压过 `<style>`，`<style>` 压过外链文件。这三者的强弱顺序在 [[层叠与优先级]] 里是 Rule 1。

## 六、易错点

- 把 `<link>` 写进 `<body>`——它属于 `<head>`。
- 一个页面里反复 `<link>` 同一个文件，或者为了"保险"把外链和内嵌写两遍同样的话——后者触发的是层叠，见 [[层叠与优先级]]。
- 用行内样式做"临时覆盖"然后忘了删：它会让后来的所有常规规则失效，直到被 `!important` 压过。

## 关联

- 上一级语法 → [[样式声明与内联]]（`style` 属性里的 `property: value;` 句型）
- 三种方式的强弱顺序 → [[层叠与优先级]]（外链 < 内嵌 < 行内，即 Rule 1）
- `class="note"` 这个钩子 → [[简单选择器]]（可复用的 class vs 唯一的 id）
- 规则放进文件之后长什么样 → [[规则结构与选择器分类]]（rule-set 的形状）
- `<link>` 本身是个 HTML 属性 → [[属性]]（外链靠 `rel` 和 `href` 两个属性驱动）
