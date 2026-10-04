---
tags: [WD, HTML标记, DOM, 开发者工具, DevTools]
course: COMP3421
lecture: L02
---

# DOM与开发者工具 · The DOM & DevTools

> **一句话**：浏览器把 HTML 解析成一棵**活的（live）内存树**就是 DOM——它是 HTML 与 JavaScript 之间的桥，而 **Elements 面板和 Console 就是 Week 2 唯一真正需要的两个工具**。

课件原文见 [Lecture_02_HTML.pptx](<../../raw/Lecture_02_HTML.pptx>)。本篇覆盖课件的 "What Is the DOM?"、"HTML Becomes a Tree"、"DOM Nodes"、"Opening DevTools"、"The Elements Panel" 和 "The Console" 六部分。

## 一、DOM 是什么

课件的中心句：**The DOM is the bridge between HTML and JavaScript**（DOM 是 HTML 与 JavaScript 之间的桥）。

| 课件的说法 | 展开 |
|---|---|
| **Document Object Model** | 浏览器对你的页面建起的**内存中的树**（in-memory tree） |
| **HTML becomes objects** | **每个元素变成一个节点**，你可以够到它 |
| **Live** | **改了它，页面立刻更新** |
| **JS's playground** | **Week 6**：JavaScript 在这棵树上走 |

```javascript
document.querySelector('h1').textContent = 'Hi';
```

这一行是上面四句话的完整演示：

1. `document` 是入口；
2. `querySelector('h1')` 按选择器**够到那个元素节点**；
3. `.textContent = 'Hi'` 改它的文本节点；
4. 页面**立刻**变了——因为树是活的。

> [!note] "live" 是这个工具最值钱的地方
> 你在 Elements 面板里的任何改动都**立刻反映在页面上**，不需要保存、不需要刷新文件。这让它成为"改一个标签看看会怎样"的实验台——[[元素与标签语法]] 那一页的 Week 2 lab 说"写一个页面，然后把它弄坏，看 DevTools 抱怨"，指的就是这里。

## 二、同一页，两个视角

课件把同一个页面并排画了两遍：左边是**源码**，右边是**DOM 树**。

**SOURCE (`index.html`)**

```html
<html>
  <head>…</head>
  <body>
    <h1>Title</h1>
    <ul>
      <li>One</li>
      <li>Two</li>
    </ul>
  </body>
</html>
```

**DOM TREE**

```
html
  head
  body
    h1
    ul
      li
      li
```

课件的说明：**Parent → child → grandchild: the DOM is exactly this tree, live**（父 → 子 → 孙：DOM 就是这棵树，而且它是活的）。

对照两张图，能看出两件事：

- **`<head>` 在树里。** 源码里的 `<head>…</head>` 也是一个节点，尽管页面上看不见它。
- **`</li>` 这种结束标签在树里没有对应节点。** 树里只列 `li`，而且**列了两个**——一个对应 `<li>One</li>`，一个对应 `<li>Two</li>`。

> [!tip] 缩进即层级
> 课件从一开始就在讲"缩进让树对人可见"（见 [[元素与标签语法]]）。DOM 树不过是把那份缩进换了一种画法。**你在源码里保持缩进良好，在 Elements 面板里看到的树就是整齐的。**

## 三、节点家族

| 课件的说法 | 展开 |
|---|---|
| **Element nodes** | **每一个标签变成一个元素节点** |
| **Text nodes** | **元素里面的文字，是它自己的节点** |
| **Parent / child / sibling** | 这棵树用的是**家族树的词汇** |
| `document` | **根**——从 JavaScript 出发的**入口点** |

```javascript
document.body.children[0].textContent
```

这句可以逐段读，正好把上表走了一遍：

| 片段 | 对应哪条 |
|---|---|
| `document` | **根** / 入口点 |
| `.body` | 从根走到 `body` 节点 |
| `.children[0]` | 它的**子**节点里的第一个（`[0]` 是从 0 开始数） |
| `.textContent` | 读那个子节点里的**文本节点**内容 |

> [!important] 文字是独立的节点
> `Text nodes — the text inside an element is its own node` 这条在 Week 2 只需知道有这回事，但它是很多新手困惑的来源：为什么"改一下那个文字"不能靠标签名取到？因为**文字不是标签，它自己没有名字**。文本节点要通过它**父元素**的 `.textContent` 访问。
>
> 另外，元素节点和文本节点混在一起，也是"源码里的空白和换行有时会在树里变成空白文本节点"的根源——那和 [[文本语义]] 里的"空白折叠"是两件事：折叠发生在**渲染**时，节点仍然存在。

## 四、打开 DevTools

| 方式 | 课件的说法 |
|---|---|
| **Right-click → Inspect**（右键 → 检查） | **直接跳到那个元素** |
| **`F12`** | 在 **Chrome 和 Edge** 里打开面板 |
| **`Cmd+Opt+I`** | **Mac** 的快捷键 |
| **Elements tab** | 看到**活的 DOM** 和**已应用的 CSS** |

课件的定位：**The fastest way to a live view of any page**（通往任何页面活视图的最快途径）。

注意 **Inspect 那一行的价值**：不是"打开工具然后在树里翻找"，而是**直接选中你右键的那个元素**。排查"这个区域的框到底是哪个"时，这一步省掉大半时间。

## 五、Elements 面板

| 能力 | 课件的说法 |
|---|---|
| **Live DOM** | 那棵树，**完全按浏览器看到的样子** |
| **Edit HTML** | **双击**即可改文字、标签、属性 |
| **Add / delete nodes** | **右键**即可增删元素 |
| **Styles panel** | 查看并修改**你点中的那个元素**的 CSS |

课件的操作提示：**Edit the page live — then refresh to reset**（在现场改页面——然后**刷新即可还原**）。

这一句是本节的安全网：**Elements 面板里的改动不会写回你的文件**，一刷新就没了。所以可以放心大胆地拆。

> [!note] "浏览器看到的样子"这个措辞
> Live DOM 那一格写的是 **exactly as the browser sees it**（完全按浏览器看到的样子）。这句话提醒一件事：**你写的和你以为浏览器理解的可能不是一回事**。标签没闭合、嵌套错位这类问题（[[元素与标签语法]] 里的三条常见错误），在这里一眼就能看出来——因为浏览器会"替你纠正"，而 Elements 面板显示的是**纠正之后**的结果。

## 六、Console

| 能力 | 课件的说法 |
|---|---|
| **Interactive JavaScript** | **输入命令，立刻执行** |
| **Inspect the page** | **窥探**任意元素的内容 |
| **Errors land here** | **出错的代码会报到控制台** |
| `console.log` | 调试时**打印值** |

课件给的三段实际操作：

```javascript
> document.title
"My First Page"
> document.querySelector('h1').textContent
"Hello, COMP3421!"
> console.log('hello web')
hello web
```

> 尖括号 `>` 是**命令提示符**——看到它就知道可以输入了。直接输入 `document.title` 回车，浏览器会把它**求值并显示结果**（上面那两段显示的是求值结果 `"My First Page"` 和 `"Hello, COMP3421!"`）；输入 `console.log('hello web')` 则打印出 `hello web`。

注意这两段正好对应本库两份笔记里的骨架：`<title>My First Page</title>` 和 `<h1>Hello, COMP3421!</h1>`——**在 [[元素与标签语法]] 里写下的代码，可以在这里直接查出来。**

课件的结论：**Week 6: this console becomes your JavaScript playground**（Week 6：这个控制台会变成你的 JavaScript 游乐场）。

> [!note] JavaScript 部分的覆盖范围
> 本库目前**没有 JavaScript 笔记**——课件只到 Week 5，Week 6–8 的 JS 内容在 `notes/raw/` 里还没有文件（见 [[课程场景与阅读约定]] 的覆盖范围一节）。本篇里所有 `document.…` 的片段都只按课件原样出现，**不展开讲解 JavaScript 语法**。课件自己把 JavaScript 标为 Week 6。

## 关联

- → [[HTML是什么]]（DOM 是这份标记被浏览器解析后的结果；同一份 HTML 的两种存在形式）
- → [[元素与标签语法]]（DOM 节点就是元素；缩进树是 DOM 树的雏形）
- → [[容器与语义化]]（在 Elements 面板里看到的 `header` / `nav` / `main` / `footer`，正是那一篇的 landmark）
- → [[图像映射]]（跨目录 — "浏览器会替你纠正"的检查习惯，在 `<area>` 坐标写错时同样有用）
- → [[CSS引入方式]]（跨目录 — Styles 面板显示的就是那三种引入方式共同作用后的结果）
- → [[课程路线图]]（跨目录 — Week 6 是 JavaScript 与 DOM 编程，本篇是它唯一的预告）
