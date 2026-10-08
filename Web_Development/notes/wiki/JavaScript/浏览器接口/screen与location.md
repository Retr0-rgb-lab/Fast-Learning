---
tags: [WD, 浏览器对象, screen, location, history, navigator]
domain: [Web 应用开发, JavaScript 浏览器接口]
course: COMP3421
lecture: L06
---

# screen与location · screen, location, history & navigator

> **一句话**：这四个对象都在 `window` 下面，分工按 **"页面在哪"和"机器是什么"** 划开——**读它们是安全的，用 `location.assign()` 把用户导航走需要理由**。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。本篇对应 §7 *The DOM & the BOM* 里的 "screen, location, history, navigator" 一页。

## 一、四个对象与它们的成员

| Object | Useful members |
|---|---|
| `screen` | `width`, `height`, `availWidth`, `availHeight`, `colorDepth` |
| `location` | `href`, `hostname`, `pathname`, `protocol`, `assign()` |
| `history` | `back()`, `forward()`, `length` |
| `navigator` | `userAgent`, `platform`, `language`, `geolocation` |

课件在表下面单独写了一句作为本篇的判准：**Reading them is safe. Navigating the user with `location.assign()` needs a reason.**（读它们是安全的；用 `location.assign()` 把用户导航走需要理由。）

## 二、四个对象各回答什么问题

`screen` 和 `location` 这两个名字很容易混，分清楚的标准是**问的是谁**：

| 对象 | 问的是 | 举例 |
|---|---|---|
| `screen` | 这块**显示器**是什么样 | 屏幕多宽、多高、能显示多少色 |
| `location` | 这个**页面**在哪 | 当前 URL 的主机、路径、协议 |
| `history` | 用户**来过哪** | 能退回去吗、能前进吗、共几步 |
| `navigator` | **浏览器**自己是什么样 | 什么浏览器、什么系统、什么语言 |

课件自己给的归类是 **Where the page is**（`location`、`history`）和 **What the machine is**（`screen`、`navigator`）——两组按"信息属于页面还是属于机器"分开。

## 三、`screen`：显示器

| 成员 | 含义 |
|---|---|
| `screen.width` | 屏幕总宽度 |
| `screen.height` | 屏幕总高度 |
| `screen.availWidth` | 可用宽度（扣掉任务栏、侧边栏这类系统占位） |
| `screen.availHeight` | 可用高度（同上） |
| `screen.colorDepth` | 每像素多少位 |

```js
screen.width;        // 屏幕总宽
screen.availWidth;   // 可用宽，可能比上面小
screen.colorDepth;   // 每像素位数
```

`avail*` 两个成员的存在就说明了 `width` / `height` 并不等于"你能看到的全部"——系统自己占掉的那部分被单独量了出来。

> ⚠️ 屏幕尺寸**不等于**浏览器窗口尺寸。[[BOM与window]] 里的 `window.innerWidth` / `innerHeight` 是**视口**（你能看到内容的那块），`screen.width` 是**显示器**（整块屏）。一个 2560 宽的显示器上，浏览器窗口可能只占 1200。做响应式适配时关心的是视口，不是屏幕——那套做法在 [[响应式与媒体查询]]。

## 四、`location`：当前地址

| 成员 | 含义 |
|---|---|
| `location.href` | 完整 URL |
| `location.hostname` | 主机名 |
| `location.pathname` | 路径部分 |
| `location.protocol` | 协议（`https:` / `http:`） |
| `location.assign()` | **跳到另一个地址** |

拿「示例站」的一个地址当例子逐个拆开：

```js
// 假设当前地址是 https://tagsysx.github.io/comp3421/editor.html
location.protocol;    // "https:"
location.hostname;    // "tagsysx.github.io"
location.pathname;    // "/comp3421/editor.html"
location.href;        // "https://tagsysx.github.io/comp3421/editor.html"
```

`protocol` / `hostname` / `pathname` 拆出来的正是 URL 的组成部分，跟 [[链接与图像]] 里 `href` 的那几种形态一一对应——**同一个地址，从文档那侧看是 `href` 的值，从脚本这侧看是这三个属性**。

### `assign()` 是写操作

```js
location.assign("https://example.com/");   // 浏览器导航到这个地址
```

这是本篇唯一需要"理由"的动作：它把**用户当前所在的页面换掉了**，而且 `history` 那边留着后退记录、可以回来（见下一节）。常见且正当的用途是登录后跳回、支付后回跳；而用户正在填的表单、他打开的其它标签页上下文，都会因此中断。读 `href` 没有这个问题——所以课件才把"读"和"导航"分开说。

## 五、`history`：用户去过哪

| 成员 | 含义 |
|---|---|
| `history.back()` | 后退一步 |
| `history.forward()` | 前进一步 |
| `history.length` | 历史记录的条目数 |

```js
history.length;   // 历史里一共几条
```

它回答的是"能不能退回去"，跟 `location` 回答的"现在在哪"是两件事：地址是当前**一个点**，`history` 是用户走过的**一条线**。

## 六、`navigator`：浏览器自己

| 成员 | 含义 |
|---|---|
| `navigator.userAgent` | 用户代理串，描述浏览器与系统 |
| `navigator.platform` | 平台 |
| `navigator.language` | 语言 |
| `navigator.geolocation` | 地理位置接口 |

```js
navigator.language;   // 例如 "en-GB"
navigator.platform;   // 例如 "MacIntel"
```

这些是**关于浏览器本身**的事实，和屏幕无关、和地址无关。课件只列出了成员名，没有展开 `geolocation` 的用法；`userAgent` 字符串的具体形态同样不在这一页范围内——用 `navigator.language` 判断语言比解析 `userAgent` 字符串更直接。

## 七、访问方式

四个对象都是 `window` 的属性，`window.` 前缀按课件说是可省的：

```js
location.href;          // 裸写
window.screen.width;    // 写全
navigator.language;     // 裸写
```

`window` 本身的来龙去脉见 [[BOM与window]]。这些值随时可以重读——和视口尺寸一样，它们是活的当前状态，不是打开页面时的快照。

## 关联

- 父对象 → [[BOM与window]]（四个对象都挂在 `window` 下；前缀为什么可省在那里）
- URL 的另一半 → [[链接与图像]]（`location.href` 就是 `<a href>` 里那个地址，`protocol` / `hostname` / `pathname` 是它的三个组成部分）
- 屏幕 ≠ 视口 → [[响应式与媒体查询]]（做适配关心的是 `window.innerWidth`，不是 `screen.width`）
- 写页面的另一条路 → [[DOM树]]（脚本改的是页面里的东西，BOM 读的是页面所在的环境）
- 典型场景 → [[表单与输入]]（表单 `action` 就是一处 `location`，提交之后脚本也常读 `location` 上的参数）