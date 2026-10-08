---
tags: [WD, DOM操作, DOM, 树结构, document]
domain: [Web 应用开发, JavaScript 浏览器接口]
course: COMP3421
lecture: L06
---

# DOM树 · The DOM Tree

> **一句话**：浏览器把你写的每个标签变成一个节点、嵌套变成分支，建成一棵以 `document` 为根的**活的树**——CSS 在这棵树上选择，JavaScript 在这棵树上修改。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。本篇对应 §7 *The DOM & the BOM* 里的 "The Document Object Model"（The Document Object Model / DOM 三要素）。

## 一、浏览器把标签变成一棵树

课件的原话是 **The browser builds a tree — Every tag becomes a node; nesting becomes the branches**（浏览器建起一棵树：每个标签变成一个节点，嵌套变成分支）。

拿「示例站」的一小段骨架来看（课程主页的结构约定见 [[课程场景与阅读约定]]）：

```html
<body>
  <header id="site-header">
    <h1>COMP3421 Web Application Design and Development</h1>
  </header>
  <main>
    <div id="demo"></div>
  </main>
  <footer>PolyU · Department of Computing</footer>
</body>
```

浏览器读完这段源码之后，内存里留下的是这样一棵树：

```text
document
└── html
    └── body
        ├── header#site-header
        │   └── h1          ← 文本：COMP3421 Web Application Design and Development
        ├── main
        │   └── div#demo    ← Week 6 课堂演示的结果输出框
        └── footer
```

对照关系很简单：**标签 = 节点，标签的嵌套 = 树的分支**。`h1` 是 `header` 的子节点，`header` 是 `body` 的子节点，一路往上 `body` 的祖先是 `html`，`html` 的祖先是 `document`。

## 二、`document` 是根，是你唯一的入口

课件第二句：**`document` is the root — your way in to everything on the page**（`document` 是根，是通往页面上任何东西的入口）。

| 节点 | 在树中的位置 | 你能对它做什么 |
|---|---|---|
| `document` | 根，**整棵树的入口** | 查找、创建元素；它本身就是 `window` 的一个属性 |
| `html` | `document` 的唯一子节点 | 拿到它就等于拿到整页 |
| `body` | `html` 的子节点，页面上肉眼能看到的东西都在它下面 | 找到它基本等于找到整页可见内容 |
| `div#demo` | `body` 的后代，示例站的结果输出框 | Week 6 的例子几乎都往它里面写 |

```js
document.querySelector("body");   // 从根出发，一步够到 body
```

> **为什么只能从根进**：树是活的，浏览器随时在增删节点，你没法提前记住某个节点的位置。唯一稳定的入口就是根——这也是为什么每个 DOM 例子都以 `document.…` 开头。

## 三、每个节点都是一个对象

课件第三句：**Every node is an object — It has properties to read and methods to call**（每个节点都是对象：有属性可读，有方法可调）。

"节点"这个词听起来像数据，其实是个**普通对象**：你从它身上读属性、给它赋属性、调用它的方法。下面这些成员都是课件在别处明确用到的：

| 角色 | 成员 | 说明 |
|---|---|---|
| 读属性 | `el.innerHTML` | 读回元素里的标记 |
| 读属性 | `el.textContent` | 读回纯文本 |
| 读属性 | `el.style` | 读到该元素的内联样式对象 |
| 写属性 | `el.innerHTML = "…"` | 写入新的内容 |
| 调方法 | `el.setAttribute("class", "urgent")` | 改属性 |
| 调方法 | `el.remove()` | 把自己从树上摘掉 |

```js
const demo = document.querySelector("#demo");
demo.setAttribute("class", "urgent");
demo.textContent = "Week 6";
demo.innerHTML;          // "Week 6"
```

这正是 [[对象与属性]] 里那套「对象 = 属性 + 方法」在页面上的应用：节点不是特例，只是恰好有一个很大的属性清单。

## 四、活的：改一下就重画，不用刷新

课件第四句：**Live and mutable — Change a node and the browser repaints — no reload**（活且可变：改一个节点，浏览器重画，不需要重新加载）。

```js
const demo = document.querySelector("#demo");
demo.textContent = "before";
demo.textContent = "after";   // 页面此刻已经变了，没有 F5
```

三个词拆开看：

- **live（活）**：内存里这棵树和你眼前这页是**同一份东西**，不是拷贝。浏览器不会在你改脚本之后还保留一份旧页面。
- **mutable（可变）**：每个节点都开放写入。
- **repaint（重画）**：改动会立刻落到像素上。

这条性质是 DOM 一切好用的理由，也是 [[DOM与开发者工具]] 里 Elements 面板能当场改页面、立刻见效的原因——那不是模拟器，是同一棵树。

## 五、HTML、CSS 和 JavaScript 在这里汇合

课件最后一句是整页的重点：**HTML, CSS and JavaScript meet here — The same tree is what CSS selects and what your script edits**（同一棵树，CSS 在上面选择，你的脚本在上面编辑）。

课件用「课程调色板」做了一组并排对照（颜色取值来自 [[颜色表示法]]）：

| 谁 | 面对的树 | 写法 | 对应成员 |
|---|---|---|---|
| CSS | 同一棵 | `header { color: #0E3F8C; }` | 选择器 → 节点 |
| JavaScript | 同一棵 | `document.querySelector("header")` | 选择器 → 节点 |

所以同一个字符串 `"header"` 在 CSS 里是一个选择器，在 JavaScript 里是选择器的参数。[[简单选择器]] 讲的是 CSS 怎么挑节点，[[查找元素]] 讲的是 JavaScript 怎么挑到同一个节点——**挑的是同一批节点，只是入口不同**。

## 六、自己走一遍

在页面控制台里依次执行，能直观看到第四节的"活"：

```js
document.querySelector("#demo").textContent = "hello";
document.querySelector("#demo").setAttribute("class", "urgent");
document.querySelector("#demo").innerHTML = "<b>bold</b>";
```

⚠️ 真实代码里这几句必须按本库统一写法来（先查、确认不是 `null`、再改），理由见 [[修改元素]]。

## 关联

- 承接 → [[DOM与开发者工具]]（Week 2 已经介绍过这棵活的树和 Elements 面板；这里是同一棵树的**脚本视角**）
- 同一棵树 → [[简单选择器]]（CSS 的 `p` 选择的就是这棵树上的 `p` 节点，脚本能拿到它靠的是同一套匹配规则）
- 祖先关系 → [[组合选择器]]（后代 `A B` 之所以成立，是因为嵌套在树上就是祖先关系；反过来脚本也靠祖先关系向上找）
- 下一步 → [[查找元素]]（既然 `document` 是根，接下来就是怎么从根走到某一个节点）
- 写法约定 → [[修改元素]]（「先查 `null` 再改属性」这条本库统一写法在那一页展开）
- 前提 → [[课程场景与阅读约定]]（`demo` 元素与「示例站」的设定都出自这一页）