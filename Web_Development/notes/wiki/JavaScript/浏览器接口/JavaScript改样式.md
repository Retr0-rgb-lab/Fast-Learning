---
tags: [WD, DOM操作, classList, camelCase, getComputedStyle]
domain: [Web 应用开发, JavaScript 浏览器接口]
course: COMP3421
lecture: L06
---

# JavaScript改样式 · Changing Styles from JavaScript

> **一句话**：从 JS 改外观有三条路——内联的 `style` 属性、`classList` 加减类名、读 `getComputedStyle`；课件明确说**伸手去用 `classList` 通常更好**，因为样式该留在 CSS 里。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。本篇对应 §7 *The DOM & the BOM* 里的 "Changing Styles from JavaScript" 一页。

## 一、四条课件要点

| 要点 | 展开 |
|---|---|
| **Inline, per element** | 赋值给 `element.style` 上一个**驼峰写法的属性**，作用范围就是这一个元素 |
| **Reaching for a `classList` is usually better** | `add`、`remove`、`toggle` 能让样式**留在它该在的地方 —— CSS 里** |
| **Camel case in JavaScript** | `font-size` → `fontSize`；`background-color` → `backgroundColor` |
| **Read the computed value** | `getComputedStyle(el)` 给出**浏览器实际应用的**那个值 |

## 二、驼峰转换

CSS 里带连字符的属性名，搬到 JS 的 `style` 对象上要改成**驼峰（camelCase）**：

| CSS 属性名 | `element.style` 上的写法 |
|---|---|
| `font-size` | `fontSize` |
| `background-color` | `backgroundColor` |
| `color` | `color`（本来就是单词，不变） |
| `margin-top` | `marginTop` |

规律很简单：**连字符 `-` 去掉，后一个词首字母大写**。

```js
const box = document.querySelector("#box");
box.style.fontSize  = "20px";       // CSS: font-size: 20px
box.style.backgroundColor = "#0E3F8C";  // CSS: background-color: #0E3F8C
```

> 驼峰这个约定不止出现在这里。整个 JS 里带连字符的地方基本都不能直接当标识符用，变量名、函数名要连字符就得写成别的形式——[[语句与标识符]] 讲的就是标识符能由哪些字符组成。

## 三、内联：作用范围就是这一个元素

```js
box.style.fontSize = "20px";
```

这一句等于给这个元素的 HTML 标签手写上 `style="font-size: 20px"`，也就是 [[样式声明与内联]] 里的那条内联声明。它有三个后果：

| 后果 | 说明 |
|---|---|
| 只作用于这一个元素 | 同类的其他元素一个都不变 |
| 优先级高 | 内联声明**赢过**样式表里同属性的规则（[[层叠与优先级]] 的来源顺序第一条） |
| 样式离开了 CSS 文件 | 颜色值、尺寸写在 JS 里，改视觉要找两个地方 |

这正是课件说 `classList` **usually better** 的原因。

## 四、`classList`：把样式留在 CSS 里

`classList` 不是直接写样式，而是**增删类名**——类名有什么效果，由 CSS 文件里那条规则决定。

```js
const box = document.querySelector("#box");
box.classList.add("highlight");     // 加上类名 → CSS 里 .highlight 的样式生效
box.classList.remove("old");         // 去掉类名 → 对应样式不再生效
box.classList.toggle("active");      // 有就去掉，没有就加上
```

三个成员分工：

| 成员 | 做什么 | 什么时候用 |
|---|---|---|
| `add(name)` | 加上一个类名 | 让某个状态开始生效 |
| `remove(name)` | 去掉一个类名 | 让某个状态结束 |
| `toggle(name)` | 有则去、无则加 | 一个按钮开关两种状态 |

配套的 CSS 长这样：

```css
.highlight {
  background-color: #FFC107;   /* 课程调色板里的 Gold */
}
```

两边的分工因此很清楚：**JS 管"什么时候切到某个状态"，CSS 管"这个状态长什么样"**。颜色值、间距这些仍然只有一处定义（[[CSS变量]] 可以让同一批值在多个规则间复用）。

对照一下同一件事的两种写法：

```js
box.style.backgroundColor = "#FFC107";       // 样式写死在 JS 里
box.classList.add("highlight");              // 样式写死在 CSS 里
```

后者改颜色只要动 CSS，前者要动 JS——而且那个十六进制值在 JS 里只出现一次，别处想用同一个金色就得再抄一遍。

## 五、`getComputedStyle`：读浏览器实际应用的值

要读某个属性**最终**是什么，赋值给 `style` 是不够的——那里只存你手动写过的值。读实际生效的值用 `getComputedStyle(el)`：

```js
const box = document.querySelector("#box");
box.classList.add("highlight");
getComputedStyle(box).color;   // 浏览器实际应用的 color
```

这里的关键是 **actually applied**：元素上可能没有任何内联声明，颜色来自样式表里的某条规则、甚至来自 [[继承]] 从父级流下来的值，而 `box.style.color` 在这些情况下都是空的字符串。`getComputedStyle` 返回的是**浏览器算完的结果**，不管这个结果当初是怎么来的。

课件示例的四行放在一起，正好是三条路各走一遍：

```js
const box = document.querySelector("#box");
box.style.fontSize = "20px";   // 路 1：内联
box.classList.add("highlight"); // 路 2：类名
box.classList.remove("old");    // 路 2：去类名
getComputedStyle(box).color;    // 路 3：读实际值
```

## 六、本库统一写法

`demo` 指「示例站」`main` 区域里的 `<div id="demo"></div>`，课堂演示的结果输出框（设定见 [[课程场景与阅读约定]]）。所有例子仍按「先 `querySelector` 拿到节点 → 检查不是 `null` → 再改属性」写，完整版本见 [[修改元素]]：

```js
const box = document.querySelector("#demo");
if (box) {
  box.classList.add("urgent");
  getComputedStyle(box).color;
}
```

## 关联

- 上一级 → [[修改元素]]（`element.style` 只是改外观的四条路之一，另三条在这里）
- 样式从哪来 → [[样式声明与内联]]（`style` 属性这种放法为什么是 CSS 的最差放法）
- 优先级 → [[层叠与优先级]]（内联声明赢过样式表规则，这就是"同一个 `color` 两处写了听谁的"）
- 值的复用 → [[CSS变量]]（样式留在 CSS 里之后，同一个颜色还能在多处共享同一个定义）
- 值的来源 → [[继承]]（`getComputedStyle` 读到的值可能来自父级，这就是为什么 `style` 上读到空串不代表它没有颜色）