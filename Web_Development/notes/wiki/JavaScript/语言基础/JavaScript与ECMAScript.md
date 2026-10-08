---
tags: [WD, JavaScript概览, ECMAScript, 版本历史, 标准化]
domain: [Web 应用开发, JavaScript 语言基础]
course: COMP3421
lecture: L06
---

# JavaScript与ECMAScript · JavaScript and ECMAScript

> **一句话**：`JavaScript` 是**商标名**、`ECMAScript` 是**标准名**，两者指的是同一门语言；而真正写进代码、交给引擎执行的**永远只有符合 ECMAScript 标准的那部分**。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。§1 *Introduction* 的 "JavaScript and ECMAScript" 与 "JavaScript Version History" 两页。

## 一、为什么有两个名字

JavaScript 诞生时 Netscape 是**公司**，不能拿公司名当语言标准名。于是 1997 年由 **ECMA International**（一个标准组织）把语言本身标准化，标准名叫 **ECMAScript**，同一个标准同时也是 **ISO/IEC 16262**。商标归 Netscape（后被 Mozilla 接手），标准归 ECMA——这就是"两个名字、一门语言"的由来。

| 名字 | 它是什么 | 谁拥有 | 出现在哪里 |
|---|---|---|---|
| **JavaScript** | 商标名（brand） | Netscape / Mozilla | 日常口语、MDN 词条、书名 |
| **ECMAScript** | 语言标准（standard） | ECMA International（兼 ISO/IEC 16262） | 版本号、规范文档、`ES6` 这种简称 |

> [!note] 两个名字都对
> 说"JavaScript 6"是口语习惯，规范场合要写 **ES2015**（或 ECMAScript 2015）。但反过来用 ECMAScript 指这门语言做项目也完全没问题——**两个名字没有对错之分，只有场合之分**。

## 二、版本年表

课件给出的表，左边是年份，中间是发布名，右边是**第一个能跑它的浏览器**：

| 年份 | 发布名 | 首个浏览器 |
|---|---|---|
| **1996** | JavaScript 1.0 | Netscape 2 |
| **1997** | **ECMAScript 1** | Internet Explorer 4 |
| 1999 | ECMAScript 3 | Internet Explorer 5 |
| 2000 | JavaScript 1.5 | Netscape 6 |
| **2011** | **ECMAScript 5** | Internet Explorer 9 |
| 2012 | — | Chrome 23, Safari 6 |
| **2015** | **ECMAScript 2015（ES6）** | 全部浏览器，部分支持 |

表里三行值得停下来看：

- **1996 → 1997**：从"某家浏览器的东西"变成"国际标准"，只隔了一年。
- **2000 → 2011**：中间**十一年没有任何新版**。所以 ES5 之前的那套写法被称为 **ES3 时代**的写法。
- **2015**：课件在这一行旁边写 *all browsers, partly*——"各浏览器都支持了一部分"。

## 三、ES6 = ES2015，以及"一年一版"

**`ES6` 只是 `ES2015` 的昵称**（the nickname of ES2015），两者指同一个版本。写 `ES6` 是因为它相对 ES5 变化太大，需要一个"第六版"的叫法；标准后来改用**年份**命名，于是同一个东西有了两个名字。

课件的时间线是：**1997 之后**几乎每年都有新版本，**2015 年起正式变成一年一版**——ES2015、ES2016、ES2017……一路数下来。课件在时间线下面给了这一句定性：

> *After 2015 the standard ships one edition per year — ES6 was the last big jump.*
> （2015 之后标准一年一版——ES6 是最后一次大跳跃。）

这句话解释了一个常见现象：**ES5 → ES6 是一个断崖**（比如 `let` / `const` 这两个新声明方式就是这一版带来的，ES5 只有 `var`，见 [[变量与声明]]），而 ES6 之后每年只是小步增量。写本课代码时"新语法突然变多"的感觉，源头就是这一次断崖。

> [!warning] `ES5 = 2009` 是常见误记
> 课件的表里 **ECMAScript 5 是 2011**（首个浏览器 Internet Explorer 9）。见到"ES5 是 2009"的说法要留意：2011 是这张表给出的年份，本笔记以课件为准。
## 四、引擎决定你实际能用什么

标准由 ECMA 定，**但引擎是逐个浏览器各自实现的**。课件因此加了一句务实的提醒：*The engine decides*——每个浏览器按自己的节奏加功能，**要用最新特性之前先确认它在你面向的浏览器里已经落地**。

这条限制在本课的直接后果是：**只写所有目标浏览器都支持的语法**。写法上的对应建议是——新代码里优先 `const`、其次 `let`，`var` 只留给必须维护的旧代码（理由见 [[变量与声明]]）；比较一律用 `===` 而不是 `==`（理由见 [[比较与typeof]]）。

## 关联

- 语言本体 → [[JavaScript是什么]]（"引擎实现标准"这句话就是从那篇的行为层讲过来的）
- 源码放哪 → [[脚本放在哪里]]（讲"引擎按自己的节奏"之前，得先有源码可读）
- 断崖的产物 → [[变量与声明]]（`let` / `const` 都是 ES6 带来的，ES5 只有 `var`）
- 断崖的另一头 → [[类型系统]]（ES6 之后现代引擎又补了 `symbol` 和 `bigint` 两种）
- 断崖的底部 → [[作用域与严格模式]]（`var` 泄漏出块、"use strict" 都是 ES5 时代就在修的账）
- 服务器那一侧 → [[课程路线图]]（Node.js 跑的是同一门语言、同一份标准，但要到 Week 10 才有课件）
