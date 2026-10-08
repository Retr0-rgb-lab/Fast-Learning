---
tags: [WD, JavaScript概览, 行为层, 脚本语言, 浏览器引擎]
domain: [Web 应用开发, JavaScript 语言基础]
course: COMP3421
lecture: L06
---

# JavaScript是什么 · What Is JavaScript

> **一句话**：JavaScript 是网页的**行为层**——HTML 给内容、CSS 给外观、JavaScript 给行为；它由浏览器里的**引擎**直接解释执行，浏览器和服务器（Node.js）跑的是同一门语言。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。§1 *Introduction* 的 "What Is JavaScript?" 与 "JavaScript Can Change the Page" 两页。

## 一、前端三门语言里的第三门

一门网页课的前两周都在讲前两门。JavaScript 是补上第三层的：

| 层 | 语言 | 负责什么 | 改变页面时你在改什么 |
|---|---|---|---|
| 内容 | **HTML** | 页面上有什么 | 标签、文本、结构 |
| 外观 | **CSS** | 它长什么样 | 颜色、间距、字体、布局 |
| 行为 | **JavaScript** | 它会做什么 | 内容、属性、外观（运行时改） |

前两层是**写死在文档里**的；JavaScript 是**在页面已经画出来之后**改的。这是三者的根本差别：HTML 和 CSS 是"送到浏览器就定下来的"，JavaScript 是在用户已经看着页面的时候才跑的。

## 二、它跑在哪：浏览器和服务器两处

**浏览器里**（本课的重点）——每个浏览器自带一个 JavaScript **引擎**（engine），负责读源码并执行：

| 引擎 | 用在哪个浏览器 |
|---|---|
| **V8** | Chrome |
| **SpiderMonkey** | Firefox |
| **JavaScriptCore** | Safari |

**服务器上**——**Node.js** 把同一门语言搬到浏览器外面执行，所以**一门语言覆盖整条技术栈**：前端的表单校验和后端的接口可以用同一种语法写。代价是服务端那些主题要到 Week 10–13 才有课件，位置见 [[课程路线图]]。

> [!note] 引擎（engine）是什么
> 引擎是**标准的实现者**。标准说"`+` 可以把两个数字加起来"，真正做加法的是引擎里的机器码。[[JavaScript与ECMAScript]] 专门讲"标准"和"品牌"的分工。

**解释执行，不是编译**——引擎**直接读源码、直接跑**，中间没有"先编译成另一种语言"这一步。这是 JavaScript 和 Java、C# 这类需要编译的语言最常被拿来对比的一点。代价是同样逻辑跑起来比编译型语言慢，收益是不需要任何构建步骤：改完源码刷新页面即可。

## 三、它能改变页面的三件事

课件把"JavaScript 能改什么"收成三条，每条都对应一类属性：

| 改什么 | 做法 | 课件的说法 |
|---|---|---|
| **内容** | 找到元素，给它的 `innerHTML` 一个新字符串 | *Change the content* |
| **属性** | 改元素的属性——图片、链接、输入框的状态都存在属性里 | *Change an attribute* |
| **外观** | 给 `element.style` 的某个属性赋值，页面**立刻重绘** | *Change the look* |

三条路在课件里都长这个样子：

```js
// 改内容
document.getElementById("demo")
.innerHTML = "Hello JavaScript";

// 改外观（课件配的注释是：一个按钮改掉自己段落的样式）
document.getElementById("demo")
.style.fontSize = "35px";
```

> **关于 `demo`**：课件所有演示例子都把结果写进同一个 `document.getElementById("demo")`，但没有给它正式设定。本库约定它是"示例站"（一张假想的课程主页）`main` 区里的一个 `<div id="demo"></div>`，作为**课堂演示的结果输出框**。正式功能页面上不会用这个 id 名。写法细节见 [[课程场景与阅读约定]]。
>
> 真实项目里写 DOM 代码，顺序是「**先查 → 确认不是 `null` → 再改属性**」，理由和写法见 [[修改元素]]。

## 四、三条路其实是同一个想法

课件最后把这三条收成一句：**"All three are one idea"——在树里够到某个节点，然后改它的一个属性。**

这个"同一个想法"是后面二十多页的地基：

- 够到节点 = `document.getElementById` / `querySelector`（见 [[查找元素]]）
- 节点是一棵树 = [[DOM树]]，树是浏览器解析 HTML 的产物（见 [[DOM与开发者工具]]）
- 改属性 = 属性名分 JS 名（`fontSize`）和 HTML 名（`font-size`）两套写法

分清楚"够到节点"和"改属性"这两步，后面讲 [[JavaScript改样式]] 时才说得清"改外观"为什么单独算一条路。

> [!warning] 三条路都从"够到那个节点"开始
> 课件把三件事收成同一个想法，是因为**它们的第一步是同一步**——先在树里找到那个元素。找不到就谈不上改：JavaScript 改不了"不存在的东西"，也没有属性可以赋给一个没找到的节点。课件在例子旁标注的 `open in editor → editor.html?example=js-basics/change-style` 就是让读者现场跑一遍看结果。写法上的完整顺序（先查、确认不是 `null`、再改）见 [[修改元素]]。

## 关联

- 前一层 → [[HTML是什么]]（"HTML 管结构不管外观"这句话，是"JS 是第三层"能成立的前提）
- 运行时的那棵树 → [[DOM与开发者工具]]（"改一个属性"必须先有那棵活的树，DevTools 看的也是它）
- 名字与标准 → [[JavaScript与ECMAScript]]（"引擎实现标准"这句话在这里第一次出现）
- 名字去哪了 → [[脚本放在哪里]]（引擎要读到源码，源码得先存在于某个地方）
- 结果去哪了 → [[四种输出方式]]（"改内容"和"输出"其实是同一个动作）
- 课程位置 → [[课程路线图]]（Week 6 是从"静态页面"跨到"能动的页面"的那一周）
