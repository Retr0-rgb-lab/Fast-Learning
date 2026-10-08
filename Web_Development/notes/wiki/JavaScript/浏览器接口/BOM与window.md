---
tags: [WD, 浏览器对象, BOM, window, 全局对象]
domain: [Web 应用开发, JavaScript 浏览器接口]
course: COMP3421
lecture: L06
---

# BOM与window · The BOM & the window Object

> **一句话**：BOM（浏览器对象模型）**没有标准却处处通用**，它最顶上那个成员就是 `window` —— 它是全局对象，全局变量是它的属性，全局函数是它的方法。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。本篇对应 §7 *The DOM & the BOM* 里的 "The Browser Object Model" 与 "The window Object" 两页。

## 一、BOM 是什么

| 课件的说法 | 展开 |
|---|---|
| **No standard, but universal** | 没有标准，但**各家浏览器实现的成员几乎一样**，所以还是被叫做 BOM |
| **window is the top** | 全局变量变成 `window` 的属性，全局函数变成它的方法 |
| **Where the page is** | 页面在哪：`location` 管地址，`history` 管用户去过哪 |
| **What the machine is** | 机器是什么：`screen` 管显示器，`navigator` 管浏览器自己 |
| **Time and storage** | 时间和存储：`setTimeout` / `setInterval`，`alert` / `confirm`，`document.cookie` |

**没有标准但通用**这四个字是理解 BOM 的关键。DOM 有 W3C / WHATWG 的正式规范，条目可以逐条对照；BOM 没有，各浏览器都是各写各的，但因为都照着对方的样子实现，最后几乎处处一致。代价是**没有规范能保证它在所有浏览器上行为完全相同**，课件用 *almost the same* 这个词就是在说这件事。

> 同一个"很多浏览器对象"的名字却分两半：`window`、`screen`、`history`、`navigator` 属于 BOM，而 `document` 属于 DOM。`document.cookie` 看起来像 DOM，其实是 BOM 的存储能力——它挂在 DOM 的根对象上。

## 二、`window` 是全局对象

课件第四句展开成两句：**The global object — A global variable is a property of `window`; `document` is one too**。

```js
var answer = 42;              // 全局变量
window.answer;                // 42 —— 它就是 window 的一个属性

function greet() { }          // 全局函数
window.greet;                 // 函数 —— 它就是 window 的一个方法

window.document;              // document 也是它的属性
```

这三行说明了一件反直觉但很重要的事：**`document`、`window`、`alert` 这些名字，在 JS 里并不需要"从某个对象上取"，它们本身就是全局名字**。这与 [[变量与声明]] 里讲的全局作用域是同一件事的两面——从声明的角度看是"变量"，从对象的角度看是"属性"，它们是同一份东西。

## 三、不需要写 `window.` 前缀

课件第二句：**No `window.` prefix needed — Global members can be written bare; `window.` is optional**。

```js
window.innerWidth;      // 写着 window.
innerWidth;             // 不写也一样 —— 课件说前缀是 optional

window.document.getElementById("header");
document.getElementById("header");   // 完全等价
```

课件示例里的最后一行直接证明了这件事：

```js
document === window.document;   // true
```

**同一个对象，两个名字。** 什么时候写 `window.`？

| 场合 | 为什么写 |
|---|---|
| 讲"这是浏览器提供的全局"时 | 明确来源，不会和下面「小心名字」一节的情况搞混 |
| 变量名可能被别的脚本占用时 | `window.foo` 明确指向全局那个 |
| 代码里没别的歧义时 | 不用写，两种写法课件说等价 |

## 四、视口尺寸

课件第三句：**The viewport size — `innerWidth` and `innerHeight`, in pixels, and they change as the window is resized**。

```js
window.innerWidth;     // 视口宽度，像素
window.innerHeight;    // 视口高度，像素
```

关键是最后半句：**它们是活的，窗口一变它们就变**。因为 [[DOM树]] 讲的整棵页面是活的，`window` 上的这些数字也一样——不是打开页面时拍下的快照，是随时可以重新读的当前值。

```js
function reportSize() {
  console.log(window.innerWidth + " × " + window.innerHeight);
}
window.addEventListener("resize", reportSize);   // 事件怎么挂，见 事件监听器
```

⚠️ 注意 `innerWidth` 指的是**视口**，也就是你看到内容的那块区域，不含浏览器自身的标签栏、地址栏。而 [[screen与location]] 里的 `screen.width` 是整块显示器屏幕——两个数不是一回事。

## 五、小心名字（Careful with the name）

课件第四句：**A global of your own called `window` would shadow it — do not**。

```js
// 不要这么写
var window = { myThing: 1 };   // 自己声明了一个叫 window 的全局
```

一旦你自己声明了 `window` 这个名字，它就**遮蔽（shadow）**了浏览器那个全局对象。此后脚本里的 `window` 指你的那个普通对象，`window.document` 直接是 `undefined`。

同样的道理适用于别的大写开头但不是浏览器提供的名字——[[变量与声明]] 讲过标识符的大小写敏感，`Window`（带大写）是 DOM 接口名，`window`（小写）是那个全局对象，别混。

## 六、课件示例

```js
window.document.getElementById("header");   // window → document → 查找
window.innerWidth;                          // viewport width
window.innerHeight;                         // viewport height
document === window.document;                // true
```

第一行值得单独看一眼：`window.document.getElementById("header")` 和 `document.getElementById("header")` 是同一件事的两种写法，本质都是 [[查找元素]] 里的方法。

## 关联

- 同一个 `document` → [[DOM树]]（`window.document` 就是那棵树的根，DOM 与 BOM 在这一点上交汇）
- 兄弟对象 → [[screen与location]]（`screen` / `location` / `history` / `navigator` 都在 `window` 下面一级）
- 同源的能力 → [[定时器与Cookie]]（`setTimeout` / `setInterval` / `document.cookie` 都是挂在 `window` 这一层的全局成员）
- 全局作用域 → [[变量与声明]]（"全局变量"和"`window` 的属性"是同一份东西的两种说法）
- 事件挂载 → [[事件监听器]]（上面的 `addEventListener("resize", …)` 展开在那一页）
- 全局名字的谨慎 → [[错误处理]]（遮蔽之后报出来的是一个 `undefined` 上的属性错误，不一定一眼看得出真因）